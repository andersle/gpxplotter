# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Track colored by heart rate zones
=================================

This example will create a map and color the track according
to heart rate zones.
"""
import folium
from gpxplotter import (
    create_folium_map,
    read_gpx_file,
    add_segment_to_map,
    add_tiles_to_map,
)
line_options = {'weight': 8}

the_map = create_folium_map()
add_tiles_to_map(the_map, 'kartverket_topo4', 'kartverket_topo4graatone')
folium.LayerControl(sortLayers=True).add_to(the_map)

for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='hr-zone-float',
                           cmap='viridis', line_options=line_options)

# To store the map as a HTML page:
# the_map.save('map_004.html')

# To display the map in a Jupyter notebook:
the_map
