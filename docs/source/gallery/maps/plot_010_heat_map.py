# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Heart rate heat map
===================

This example will create a map and add a heart rate heat map along
a track.
"""
from folium.plugins import HeatMap
from gpxplotter import read_gpx_file, create_folium_map


the_map = create_folium_map(tiles='openstreetmap')
for track in read_gpx_file('example4.gpx'):
    for i, segment in enumerate(track['segments']):
        data = []
        for lat, lon, hr in zip(segment['lat'], segment['lon'], segment['hr']):
            data.append([lat, lon, float(hr)])
        HeatMap(data, name='Heart rate', radius=20).add_to(the_map)
        boundary = the_map.get_bounds()
        the_map.fit_bounds(boundary, padding=(3, 3))
        break
# To store the map as a HTML page:
# the_map.save('map_010.html')

# To display the map in a Jupyter notebook:
the_map
