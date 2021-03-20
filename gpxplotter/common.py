# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines common methods for gpxplotter."""
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


def heart_rate_zones(pulse, max_heart_rate=187):
    """Calculate heart rate zones.

    Parameters
    ----------
    pulse : int (or float)
        The heart rate to converte into a heart rate zone.
    max_heart_rate : int (or float), optional
        The maximal heart rate.

    Returns
    -------
    out[0] : float
        The heart rate zone.
    out[1] : float
        The heart rate zone, rounded to an integer.
    out[2] : float
        The fraction of the heart rate to the max heart rate.

    """
    frac = float(pulse) / float(max_heart_rate)
    zone = 10.0 * frac - 4.0
    if zone < 1.0:
        zone = 1.0
    if zone > 5.0:
        zone = 5.0
    return zone, int(zone), frac


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
    """
    if limits is None:
        limits = HR_LIMITS
    return [(max_heart_rate * i[0], max_heart_rate * i[1]) for i in limits]


def format_time_delta(time_delta):
    """Format time deltas as strings on the form hh:mm:ss."""
    timel = []
    for i in time_delta:
        hours, res = divmod(i, 3600)
        minutes, seconds = divmod(res, 60)
        timel.append(f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}')
    return timel


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


def update_hr_zones(segment, max_heart_rate=187):
    """Find and update heart rate zones for a segment.

    Parameters
    ----------
    segment : dict
        The segment to add zones for.
    max_heart_rate : int (or float)
        The maximum heart rate, used for calculation of zones.

    """
    if 'hr' in segment:
        hrzone = []
        for i in segment['hr']:
            zonei = heart_rate_zones(i, max_heart_rate=max_heart_rate)
            hrzone.append(zonei)
        segment['hr-zone'] = np.array([i[1] for i in hrzone], dtype=np.int_)
        segment['hr-zone-float'] = np.array([i[0] for i in hrzone])
        segment['hr-zone-frac'] = np.array([i[2] for i in hrzone])
        segment['hr-regions'] = find_regions(segment['hr-zone'])


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
    vel = np.array(velocities).reshape(-1, 1)
    clu = KMeans(n_clusters=n_clusters, init='k-means++')
    labels = clu.fit_predict(vel)
    # Sort labels according to cluster centers so that a lower label
    # is a lower velocity:
    centers = clu.cluster_centers_.flatten()
    idx = list(np.argsort(centers))
    levels = np.array([idx.index(i) for i in labels], dtype=np.int_)
    return levels
