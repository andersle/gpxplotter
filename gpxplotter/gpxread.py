# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for reading data from GPX files."""
import warnings
from xml.dom import minidom
from math import atan, atan2, radians, tan, sin, cos, sqrt
import dateutil.parser
import numpy as np
from scipy.interpolate import UnivariateSpline
from gpxplotter.common import update_hr_zones, cluster_velocities


EXTRACT = {
    'time': {'key': 'time', 'formatter': dateutil.parser.parse},
    'temp': {'key': 'ns3:atemp', 'formatter': float},
    'hr': {'key': 'ns3:hr', 'formatter': int},
    'cad': {'key': 'ns3:cad', 'formatter': float},
}


def vincenty(point1, point2, tol=10**-12, maxitr=1000):
    """Calculate distance between two lat/lon coordinates.

    This calculation is based on the formula available from
    Wikipedia [1]_.

    Parameters
    ----------
    point1 : tuple of floats
        This is the first coordinate on the form: ``(lat, lon)``.
    point2 : tuple of floats
        This is the second coordinate on the form: ``(lat, lon)``.
    tol : float, optional
        The tolerance from convergence. The default value is
        taken from the wikipedia article.
    maxitr : integer, optional
        The maximum number of iterations to perform.

    References
    ----------
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

    # Iteratively, according to Wikipedia
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


def read_segment(segment):
    """Read raw gpx-data for a segment.

    Parameters
    ----------
    segment : object like :py:class:`xml.dom.minidom.Element`
        The segment we are about to read data from.

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
    if 'hr' in data:
        data['hr'] = np.array(data['hr'], dtype=np.int_)
    return data


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

    This method will calculate approximate velocities by
    finding a spline and its derivative.

    Parameters
    ----------
    distance : array_like
        Distances, measured as a function of time.
    time : array_like
        The accompanying time stamps for the velocities.

    """
    try:
        spline = UnivariateSpline(time, distance, k=3)
        vel = spline.derivative()(time)
        idx = np.where(vel < 0)[0]
        vel[idx] = 0.0
        return vel
    except Exception as error:
        warnings.warn(f'Estimating velocities failed: "{error.args}"')
        return None


def get_velocity(segment):
    """Attempt to estimate the velocity.

    Parameters
    ----------
    segment : dict
        The raw data from the gpx file.

    """
    # Velocity i m / s
    velocity = approximate_velocity(
        segment['distance'],
        segment['elapsed-time']
    )
    if velocity is not None:
        segment['velocity'] = velocity
        segment['Velocity / km/h'] = 3.6 * segment['velocity']
        # Pace in min / km, as float
        idx = np.where(segment['velocity'] > 0)[0]
        segment['pace'] = np.zeros_like(segment['velocity'])
        segment['pace'][idx] = 1.0 / ((60. / 1000) * segment['velocity'][idx])
        # Add velocity levels:
        levels = cluster_velocities(segment['velocity'])
        if levels is not None:
            segment['velocity-level'] = levels


def process_segment(segment, max_heart_rate=187):
    """Add derived properties to the given segment.

    Parameters
    ----------
    segment : dict
        The raw data from the gpx file.
    max_heart_rate : float, optional
        The maximum heart rate, used for the calculation of
        heart rate zones.

    """
    segment['latlon'] = list(zip(segment['lat'], segment['lon']))
    # Process time information:
    if 'time' in segment:
        time_zero = segment['time'][0]
        time_delta = [i - time_zero for i in segment['time']]
        segment['elapsed-time'] = np.array(
                [i.total_seconds() for i in time_delta],
        )
    # Calculate distance:
    segment['distance'] = np.array(
        get_distances(segment['lat'], segment['lon'])
    )
    segment['Distance / km'] = segment['distance'] / 1000.
    # Estimate velocity:
    if 'distance' in segment and 'elapsed-time' in segment:
        get_velocity(segment)
    # Add hr metrics:
    if 'hr' in segment:
        update_hr_zones(segment, max_heart_rate=max_heart_rate)
        if 'elapsed-time' in segment:
            delta_time = (
                segment['elapsed-time'][-1] - segment['elapsed-time'][0]
                )
            segment['average-hr'] = (
                np.trapz(segment['hr'], segment['elapsed-time']) / delta_time
            )
    # Add elevation metrics:
    if 'elevation' in segment:
        ele_diff = np.diff(segment['elevation'])
        segment['elevation-up'] = sum(ele_diff[np.where(ele_diff > 0)[0]])
        segment['elevation-down'] = sum(ele_diff[np.where(ele_diff < 0)[0]])
    # Add alias:
    if 'hr' in segment:
        segment['heart rate'] = segment['hr']


def read_gpx_file(gpxfile, max_heart_rate=187):
    """Read data from a given gpx file.

    Parameters
    ----------
    gpxfile : string
        The file to open and read.
    max_heart_rate : integer (or float)
        The heart rate, used in calculation of heart rate zones.

    Yields
    ------
    out : dict
        A dictionary containing the data read from each track in the
        file.

    """
    gpx = minidom.parse(gpxfile)
    tracks = gpx.getElementsByTagName('trk')
    for track in tracks:
        raw_segments = track.getElementsByTagName('trkseg')
        track_data = {
            'name': _get_gpx_text(track, 'name'),
            'type': _get_gpx_text(track, 'type'),
            'segments': [read_segment(i) for i in raw_segments],
        }
        # Add some more processed data for segments
        for segment in track_data['segments']:
            process_segment(segment, max_heart_rate=max_heart_rate)
        yield track_data
