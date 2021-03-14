# -*- coding: utf-8 -*-
# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for interfacing with folium."""
import folium
import folium.features
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


def create_folium_map(tiles=None):
    """Create a folium map.

    Returns
    -------
    the_map : object like folium.folium.Map
        The map created here.

    """
    the_map = folium.Map(
        location=['63.446827', 10.421906],
        tiles=None,
        zoom_start=11,
        control_scale=True,
    )
    folium.TileLayer('openstreetmap').add_to(the_map)
    if tiles is None:
        tiles = TILES
    for tile in tiles:
        folium.TileLayer(
            tile['url'], attr=tile['attr'], name=tile['name']
        ).add_to(the_map)
    folium.TileLayer('stamenterrain').add_to(the_map)
    folium.LayerControl().add_to(the_map)
    return the_map


def add_segment_to_map(the_map, segment, color_by=None, line_options=None):
    """Add a segment as a line to a map."""
    if color_by is None:
        if line_options is None:
            line_options = {}
        line = folium.features.PolyLine(segment['latlon'], **line_options)
        line.add_to(the_map)
    else:
        add_colored_line(the_map, segment, color_by)
    start = folium.Marker(
        location=segment['latlon'][0],
        tooltip='Start',
        icon=folium.Icon(icon='ok', color='green'),
    )
    start.add_to(the_map)
    stop = folium.Marker(
        location=segment['latlon'][-1],
        tooltip='End',
        icon=folium.Icon(icon='home', color='lightgray'),
    )
    stop.add_to(the_map)
    the_map.location = list(np.mean(segment['latlon'], axis=0))
    the_map.options['zoom'] = 15


def add_colored_line(the_map, segment, color_by, line_options=None):
    """Add segment as a colored line to a map."""
    zdata = segment[color_by]
    avg = 0.5 * (zdata[1:] + zdata[:-1])
    minz, maxz = min(avg), max(avg)
    colormap = branca.colormap.linear.viridis.scale(minz, maxz).to_step(10)
    colormap.caption = RELABEL.get(color_by, color_by)
    if line_options is None:
        line_options = {}
    line = folium.ColorLine(positions=segment['latlon'], colormap=colormap,
                            colors=avg, control=False, **line_options)
    line.add_to(the_map)
    the_map.add_child(colormap)
