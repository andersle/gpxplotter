# -*- coding: utf-8 -*-
# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines common methods for gpxplotter."""


# Define heart-rate limits:
HR_LIMITS = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]

# For adding text:
RELABEL = {
    'hr': 'Heart rate / bpm',
    'distance': 'Distance / m',
    'time': 'Time',
    'elevation': 'Elevation / m',
    'hr-zone-frac': 'Fraction of maximum heart rate',
    'hr-zone-float': 'Heart rate zone',
}


def heart_rate_zones(pulse, maxpulse=187):
    """Calculate heart rate zones.

    Parameters
    ----------
    pulse : int (or float)
        The heart rate to converte into a heart rate zone.
    maxpulse : int (or float), optional
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
    frac = float(pulse) / float(maxpulse)
    zone = 10.0 * frac - 4.0
    if zone < 1.0:
        zone = 1.0
    if zone > 5.0:
        zone = 5.0
    return zone, int(zone), frac


def heart_rate_zone_limits(maxpulse=187, lims=None):
    """Return the limits for the heart rate zones."""
    if lims is None:
        lims = HR_LIMITS
    return [(maxpulse * i[0], maxpulse * i[1]) for i in lims]


def format_time_delta(time_delta):
    """Format time deltas as strings on the form hh:mm:ss."""
    timel = []
    for i in time_delta:
        hours, res = divmod(i, 3600)
        minutes, seconds = divmod(res, 60)
        timel.append(f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}')
    return timel
