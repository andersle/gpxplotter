# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Track colored by heart rate
===========================

This example will create a map and color the track according
to the measured heart rate.
"""
import folium
from gpxplotter import (
    read_gpx_file,
    create_folium_map,
    add_segment_to_map,
    add_all_tiles,
)

the_map = create_folium_map(tiles='kartverket_topo4')
# Add pre-defined tiles:
add_all_tiles(the_map)

for track in read_gpx_file('example1.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='hr')

# Add layer control to change tiles:
folium.LayerControl(sortLayers=True).add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_001.html')

# To display the map in a Jupyter notebook:
the_map
