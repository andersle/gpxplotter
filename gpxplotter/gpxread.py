# -*- coding: utf-8 -*-
# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for reading data from GPX files."""
from xml.dom import minidom
from math import atan, atan2, radians, tan, sin, cos, sqrt
import dateutil.parser
import numpy as np
from scipy.interpolate import UnivariateSpline
from gpxplotter.common import heart_rate_zones


def date_format(string):
    """Conversions for date strings."""
    timeobj = dateutil.parser.parse(string)
    return timeobj


EXTRACT = {
    'time': {'key': 'time', 'formatter': date_format},
    'temp': {'key': 'ns3:atemp', 'formatter': float},
    'hr': {'key': 'ns3:hr', 'formatter': float},
    'cad': {'key': 'ns3:cad', 'formatter': float},
}


def vincenty(point1, point2, tol=10**-12, maxitr=1000):
    """Calculate distance between two lat/lon coordinates.

    Parameters
    ----------
    point1 : tuple of floats
        This is the first coordinate on form: ``(lat, lon)``.
    point2 : tuple of floats
        This is the second coordinate on form: ``(lat, lon)``.
    tol : float, optional
        The tolerance from convergence. The default value is
        taken from the wikipedia article.
    maxitr : integer, optional
        The maximum number of iterations to perform.

    References
    ----------
    This calculation is based on the formula available from wikipedia [1]_.

    .. [1] https://en.wikipedia.org/wiki/Vincenty's_formulae

    """
    # Some WGS-84 parameters:
    major_axis = 6378137.0
    flattening = 1/298.257223563
    minor_axis = 6356752.314245

    lat1, lon1 = point1
    lat2, lon2 = point2

    rlat1 = atan((1 - flattening) * tan(radians(lat1)))
    rlat2 = atan((1 - flattening) * tan(radians(lat2)))

    diff_long = radians(lon2) - radians(lon1)

    # Iteratively, according to wikipedia
    lambd = diff_long

    sin1 = sin(rlat1)
    cos1 = cos(rlat1)

    sin2 = sin(rlat2)
    cos2 = cos(rlat2)

    converged = False
    for _ in range(maxitr):
        sin_sigma = sqrt(
            (cos2 * sin(lambd))**2 +
            (cos1 * sin2 - sin1 * cos2 * cos(lambd))**2
        )
        if sin_sigma == 0.0:
            return 0.0
        cos_sigma = sin1 * sin2 + cos1 * cos2 * cos(lambd)
        sigma = atan2(sin_sigma, cos_sigma)
        sin_alpha = (cos1 * cos2 * sin(lambd)) / sin_sigma
        cos_alpha_sq = 1.0 - sin_alpha**2
        if cos_alpha_sq == 0.0:
            cos_sigma2 = 0.0
        else:
            cos_sigma2 = cos_sigma - ((2.0 * sin1 * sin2) / cos_alpha_sq)
        cvar = ((flattening / 16.) * cos_alpha_sq *
                (4.0 + flattening * (4.0 - 3.0 * cos_alpha_sq)))
        lambd0 = lambd
        lambd = (
            diff_long + (1.0 - cvar) * flattening * sin_alpha * (
                sigma + cvar * sin_sigma * (
                    cos_sigma2 + cvar * (
                        cos_sigma * (-1.0 + 2.0 * cos_sigma2**2)
                    )
                )
            )
        )
        diff = abs(lambd0 - lambd)
        if diff <= tol:
            converged = True
            break
    if not converged:
        raise ValueError("Vincenty's formulae did not converge!")
    uvar_sq = cos_alpha_sq * ((major_axis**2 - minor_axis**2) / minor_axis**2)
    avar = (1. + (uvar_sq / 16384.) *
            (4096. + uvar_sq * (-768. + uvar_sq * (320. - 175. * uvar_sq))))
    bvar = (uvar_sq / 1024.) * (256. + uvar_sq * (-128. + uvar_sq *
                                                  (74. - 47. * uvar_sq)))
    delta_sigma = bvar * sin_sigma * (
        cos_sigma2 + 0.25 * bvar * (
            cos_sigma * (-1.0 + 2.0 * cos_sigma2**2) - (bvar / 6.0) * (
                cos_sigma2 * (
                    (-3.0 + 4.0 * sin_sigma**2) * (-3.0 + 4.0 * cos_sigma2**2)
                )
            )
        )
    )
    dist = minor_axis * avar * (sigma - delta_sigma)
    return dist


def extract_data(point, key, formatter):
    """Extract data from a point.

    Parameters
    ----------
    key : string
        The xml field we are extracting data from.
    formatter : callable
        A method we use to format/convert the data we extract.

    """
    data = point.getElementsByTagName(key)
    for i in data:
        return [formatter(child.data) for child in i.childNodes]


def get_point_data(point):
    """Get basic information from a track point.

    Parameters
    ----------
    point : object like :py:class:`xml.dom.minidom.Element`
        The point on the track we are extracting information from.

    """

    data = {
        'lat': float(point.getAttribute('lat')),
        'lon': float(point.getAttribute('lon')),
    }

    ele = extract_data(point, 'ele', float)
    if ele is not None:
        data['elevation'] = ele

    for key, val in EXTRACT.items():
        value = extract_data(point, val['key'], val['formatter'])
        if value is not None:
            data[key] = value

    return data


def read_segment(segment, maxpulse=187):
    """Read points in a segment and return data for plotting.

    Parameters
    ----------
    segment : object like :py:class:`xml.dom.minidom.Element`
        The sement we are about to read data from.
    maxpulse : integer
        The maximum heart rate to use in calculations of heart rate zones.

    Returns
    -------
    out : dict
        The data read from the segment.

    """
    points = segment.getElementsByTagName('trkpt')

    data = {}
    for point in points:
        point_data = get_point_data(point)
        if any([i is None for i in data]):
            continue
        for key, val in point_data.items():
            if key not in data:
                data[key] = []
            try:
                data[key].extend(val)
            except TypeError:
                data[key].append(val)
    for key, val in data.items():
        if key not in ('time', 'hr'):
            data[key] = np.array(val)
    if 'time' in data:
        data['time-delta'] = [i - data['time'][0] for i in data['time']]
    if 'hr' in data:
        data['hr'] = np.array(data['hr'], dtype=np.int_)
        data['heart rate'] = data['hr']

    data['latlon'] = list(zip(data['lat'], data['lon']))

    hrzone = [heart_rate_zones(i, maxpulse=maxpulse) for i in data['hr']]
    data['hr-zone'] = np.array([i[1] for i in hrzone], dtype=np.int_)
    data['hr-zone-float'] = np.array([i[0] for i in hrzone])
    data['hr-zone-frac'] = np.array([i[2] for i in hrzone])
    return data


def find_regions(yval):
    """Find borders for regions with equal values."""
    regions = []
    region_y = None
    i = None
    for i, ypos in enumerate(yval):
        if region_y is None:
            region_y = ypos
        if ypos != region_y:
            regions.append([i, region_y])
            region_y = ypos
    # for adding the last region
    if i is not None:
        regions.append([i, region_y])
    new_regions = []
    for i, region in enumerate(regions):
        if i == 0:
            reg = [0, region[0], region[1]]
        else:
            reg = [regions[i-1][0], region[0], region[1]]
        new_regions.append(reg)
    return new_regions


def get_distances(lat, lon):
    """Get the spatial distance between time-ordered points.

    Parameters
    ----------
    lat : list of floats
        The latitudes.
    lon : list of floats
        The longitudes.

    Returns
    -------
    dist : list of floats
        The distances in meters.

    """
    dist = []
    for i, (lati, loni) in enumerate(zip(lat, lon)):
        if i == 0:
            dist.append(0)
        else:
            dist.append(
                dist[-1] + vincenty((lati, loni), (lat[i - 1], lon[i - 1]))
            )
    return dist


def _get_gpx_text(track, tagname):
    """Grab text from a given track."""
    tag_txt = []
    tag = track.getElementsByTagName(tagname)
    for i in tag:
        tag_txt.append(
            ''.join(child.data for child in i.childNodes if (child.nodeType ==
                                                             child.TEXT_NODE))
        )
    return tag_txt


def approximate_velocity(distance, time):
    """Calculate approximate velocities.

    This method will calculate approxiate velocities by
    finding a spline and its derivative.

    Parameters
    ----------
    distance : array_like
        Distances measured as a function of time.
    time : array_like
        The accompanying time stamps for the velocities.

    """
    spline = UnivariateSpline(time, distance, k=1)
    return spline.derivative()(time)


def read_gpx_file(gpxfile, maxpulse=187):
    """Read data from a given gpx file.

    Parameters
    ----------
    gpxfile : string
        The file to open and read.
    maxpulse : integer
        The maximum pulse. Used in calculation of heat rate zones.

    Yields
    ------
    out : dict
        A dictionary containing the data read from each track in the
        file.

    """
    gpx = minidom.parse(gpxfile)
    tracks = gpx.getElementsByTagName('trk')
    for track in tracks:
        segments = track.getElementsByTagName('trkseg')
        track_data = {
            'name': _get_gpx_text(track, 'name'),
            'type': _get_gpx_text(track, 'type'),
            'segments': [read_segment(i, maxpulse=maxpulse) for i in segments],
        }
        # Add some more processed data for segments
        for data in track_data['segments']:
            data['hr-regions'] = find_regions(data['hr-zone'])
            data['elapsed-time'] = np.array(
                [i.total_seconds() for i in data['time-delta']],
                dtype=np.int_
            )
            data['distance'] = np.array(
                get_distances(data['lat'], data['lon'])
            )
            data['average-hr'] = (
                np.trapz(data['hr'], data['elapsed-time']) /
                (data['elapsed-time'][-1] - data['elapsed-time'][0])
            )
            ele_diff = np.diff(data['elevation'])
            data['elevation-up'] = ele_diff[np.where(ele_diff > 0)[0]].sum()
            data['elevation-down'] = ele_diff[np.where(ele_diff < 0)[0]].sum()
            data['velocity'] = approximate_velocity(
                data['distance'], data['elapsed-time']
            )
            data['pace'] = 1.0 / ((60. / 1000) * data['velocity'])
        yield track_data
