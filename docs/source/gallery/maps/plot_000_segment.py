# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Display a segment in a map
==========================

This example will create a map and add a track to it.
"""
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map

# Define some properties for drawing the line:
line_options = {'color': 'red', 'weight': 8, 'opacity': 0.5}

the_map = create_folium_map(tiles='openstreetmap')
for track in read_gpx_file('example1.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, line_options=line_options)

# To store the map as a HTML page:
the_map.save('map_000.html')
# To display the map in a Jupyter notebook:
the_map
