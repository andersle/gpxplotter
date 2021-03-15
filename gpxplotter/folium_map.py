# -*- coding: utf-8 -*-
# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for interfacing with folium."""
from math import ceil
import folium
#import folium.features
import branca.colormap
import numpy as np
from gpxplotter.common import RELABEL


TILES = [
    {
        'name': 'topo4',
        'url': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    },
    {
        'name': 'topo4graatone',
        'url': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4graatone&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    }
]


def create_folium_map(**kwargs):
    """Create a folium map.

    Parameters
    ----------
    kwargs : optional
        Arguments passed to the method generating the map,
        see :py:func:`folium.Map`.

    Returns
    -------
    the_map : object like :py:class:`folium.folium.Map`
        The map created here.

    """
    # Add a few defaults:
    kwargs['control_scale'] = kwargs.get('control_scale', True)
    kwargs['tiles'] = kwargs.get('tiles', None)
    the_map = folium.Map(**kwargs)
    # Add extra tiles:
    for tile in TILES:
        folium.TileLayer(
            tile['url'], attr=tile['attr'], name=tile['name']
        ).add_to(the_map)
    folium.TileLayer('openstreetmap').add_to(the_map)
    folium.TileLayer('stamenterrain').add_to(the_map)
    folium.LayerControl().add_to(the_map)
    return the_map


def add_start_top_markers(the_map, segment):
    """Add markers for the start and end of the segment."""
    start_time = segment['time'][0].strftime('%A %B %d, %Y: %H:%M:%S')
    start = folium.Marker(
        location=segment['latlon'][0],
        tooltip='Start',
        popup=folium.Popup(start_time, max_width=250),
        icon=folium.Icon(icon='ok', color='green'),
    )
    start.add_to(the_map)
    end_time = segment['time'][-1].strftime('%A %B %d, %Y: %H:%M:%S')
    stop = folium.Marker(
        location=segment['latlon'][-1],
        tooltip='End',
        popup=folium.Popup(end_time, max_width=250),
        icon=folium.Icon(icon='home', color='lightgray'),
    )
    stop.add_to(the_map)


def add_segment_to_map(the_map, segment, color_by=None, line_options=None):
    """Add a segment as a line to a map."""
    if color_by is None:
        if line_options is None:
            line_options = {}
        line = folium.features.PolyLine(segment['latlon'], **line_options)
        line.add_to(the_map)
    else:
        add_colored_line(the_map, segment, color_by)
    add_start_top_markers(the_map, segment)
    boundary = the_map.get_bounds()
    the_map.fit_bounds(boundary, padding=(3, 3))


def add_colored_line(the_map, segment, color_by, line_options=None):
    """Add segment as a colored line to a map."""
    zdata = segment[color_by]
    avg = 0.5 * (zdata[1:] + zdata[:-1])
    minz, maxz = min(avg), max(avg)
    colormap = branca.colormap.linear.viridis.scale(minz, maxz).to_step(10)
    colormap.caption = RELABEL.get(color_by, color_by)
    if line_options is None:
        line_options = {'weight': 6}
    line_options['weight'] = line_options.get('weight', 6)
    line = folium.ColorLine(positions=segment['latlon'], colormap=colormap,
                            colors=avg, control=False, **line_options)
    line.add_to(the_map)
    the_map.add_child(colormap)
