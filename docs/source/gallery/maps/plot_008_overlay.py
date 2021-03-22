# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding overlays
===============

This example will create a map, add a track and some
overlays that will display the steepness.
"""
import folium
from gpxplotter import (
    create_folium_map,
    read_gpx_file,
    add_segment_to_map,
)
line_options = {'weight': 8}

the_map = create_folium_map(tiles='kartverket_topo4')

for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, line_options=line_options)

steepness = folium.WmsTileLayer(
    url='https://gis3.nve.no/map/services/Bratthet/MapServer/WmsServer',
    layers='Bratthet_snoskred',
    fmt='image/png',
    opacity=0.7,
    transparent=True,
    name='Steepness',
)
steepness.add_to(the_map)

# Add layer control:
folium.LayerControl(sortLayers=True).add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_008.html')

# To display the map in a Jupyter notebook:
the_map
