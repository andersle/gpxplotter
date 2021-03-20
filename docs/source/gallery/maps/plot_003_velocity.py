# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Track colored by velocity
==========================

This example will create a map and color the track according
to the velocity.
"""
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
line_options = {'weight': 8}

the_map = create_folium_map(tiles='openstreetmap')
for track in read_gpx_file('example2.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='velocity-level',
                           cmap='RdPu_09', line_options=line_options)

# To store the map as a HTML page:
the_map.save('map_003.html')

# To display the map in a Jupyter notebook:
the_map
