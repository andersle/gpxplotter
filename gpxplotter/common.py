# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines common methods for gpxplotter."""
import warnings
import numpy as np
from sklearn.cluster import KMeans

# Define heart-rate limits:
HR_LIMITS = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]

# For adding text:
RELABEL = {
    'hr': 'Heart rate / bpm',
    'distance': 'Distance / m',
    'time': 'Time',
    'elapsed-time': 'Elapsed time',
    'elevation': 'Elevation / m',
    'hr-zone-frac': 'Fraction of maximum heart rate',
    'hr-zone-float': 'Heart rate zone',
    'hr-zone': 'Heart rate zone',
    'velocity-level': 'Velocity (slower -> faster)',
}


def heart_rate_zone_limits(max_heart_rate=187, limits=None):
    """Return the limits for the heart rate zones.

    Parameters
    ----------
    max_heart_rate : int (or float)
        The maximum heart rate
    limits : list
        A list of heart rate zone limits as fractions of the
        maximum heart rate. This list is on the
        form `[[min_zone_1, max_zone_1],]`. The default zones
        are:
        `[(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]`

    Returns
    -------
    out : list of list of numbers
        The heart rates defining the different zones.

    """
    if limits is None:
        limits = HR_LIMITS
    return [(max_heart_rate * i[0], max_heart_rate * i[1]) for i in limits]


def format_time_delta(time_delta):
    """Format time deltas as strings on the form hh:mm:ss.

    Parameters
    ----------
    time_delta : array_like
        A time in seconds.

    Returns
    -------
    timel : list of strings
        The ``time_delta`` formatted as hh:mm:ss

    """
    timel = []
    for i in time_delta:
        hours, res = divmod(i, 3600)
        minutes, seconds = divmod(res, 60)
        timel.append(f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}')
    return timel


def find_regions(yval):
    """Find borders for regions with equal values.

    Parameters
    ----------
    yval : array_like
        The values we are to locate regions for.

    Returns
    -------
    new_regions : list of lists of numbers
        The regions where yval is constant. These are on the form
        ``[start_index, end_index, constant_y]`` with the
        interpretation that ``yval=constant-y`` for the index
        range ``[start_index, end_index]``

    """
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


def update_hr_zones(segment, max_heart_rate=187):
    """Find and update heart rate zones for a segment.

    Parameters
    ----------
    segment : dict
        The segment to add zones for.
    max_heart_rate : int (or float)
        The maximum heart rate, used for the calculation of zones.

    """
    if 'hr' in segment:
        limits = heart_rate_zone_limits(max_heart_rate=max_heart_rate)
        bins = [i[0] for i in limits]
        # bins[i-1] <= x < bins[i]
        segment['hr-zone'] = np.digitize(segment['hr'], bins, right=False)
        # Add fractional part:
        zone_float = []
        for hrate, zone in zip(segment['hr'], segment['hr-zone']):
            if zone == 0:
                left = 0
                right = bins[0]
            elif zone == len(bins):
                left = bins[-1]
                right = max_heart_rate
            else:
                left = bins[zone-1]
                right = bins[zone]
            frac = (hrate - left) / (right - left)
            zone_float.append(zone + frac)
        segment['hr-zone-float'] = np.array(zone_float)
        segment['hr-zone-frac'] = segment['hr'] / max_heart_rate
        segment['hr-regions'] = find_regions(segment['hr-zone'])
        segment['zone_txt'] = get_limits_txt(limits)


def get_limits_txt(limits):
    """Return heart rate limits as text.

    Parameters
    ----------
    limits : list of list of numbers

    Returns
    -------
    txt : dict
        Text representing the heart rate zones.

    """
    txt = {
        0: f'$<${int(limits[0][0])} bpm',
        1: f'{int(limits[0][0])}‒{int(limits[0][1])} bpm',
        2: f'{int(limits[1][0])}‒{int(limits[1][1])} bpm',
        3: f'{int(limits[2][0])}‒{int(limits[2][1])} bpm',
        4: f'{int(limits[3][0])}‒{int(limits[3][1])} bpm',
        5: f'$>${int(limits[3][1])} bpm',
    }
    return txt


def cluster_velocities(velocities, n_clusters=5):
    """Group the velocities into a predefined set of clusters.

    This is used to label velocities as `faster`, `slower`, etc.

    Parameters
    ----------
    velocities : array_like
        The velocities to cluster.
    n_clusters : int, optional
        The number of clusters to look for.

    Returns
    -------
    levels : array_like
        The velocity level (cluster) each velocity is assigned to.

    """
    if np.isnan(velocities).any():
        warnings.warn('Some velocities are NaN, skipping clustering')
        return None
    vel = np.array(velocities).reshape(-1, 1)
    clu = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10)
    labels = clu.fit_predict(vel)
    # Sort labels according to cluster centers so that a lower label
    # is a lower velocity:
    centers = clu.cluster_centers_.flatten()
    idx = list(np.argsort(centers))
    levels = np.array([idx.index(i) for i in labels], dtype=np.int_)
    return levels
