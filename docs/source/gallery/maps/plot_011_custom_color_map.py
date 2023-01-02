# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Track colored with a custom color map
=====================================

This example will create a map and color the track according
to the velocity using a custom color map, instead of a pre-defined one.

.. note:: The velocities are calculated from the distance
   so it is a bit noisy.
"""
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
from branca.colormap import LinearColormap
line_options = {'weight': 8}

color_map = LinearColormap(['#00ff00', '#ff0000'])

the_map = create_folium_map(tiles='openstreetmap')
for track in read_gpx_file('example2.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='velocity-level',
                           cmap=color_map, line_options=line_options)

# To store the map as a HTML page:
# the_map.save('map_011.html')

# To display the map in a Jupyter notebook:
the_map
