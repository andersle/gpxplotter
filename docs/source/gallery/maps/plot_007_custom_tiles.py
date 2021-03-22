# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding custom tiles to a map
============================

In this example we will add custom tiles to a map.
Specifically, we will add tiles from
`Thunderforest <https://www.thunderforest.com/>`_.

To use these maps, you will have to sign up at
`Thunderforest <https://www.thunderforest.com/>`_
and obtain an API key to use for retrieving the
tiles.
"""
import folium
from gpxplotter import create_folium_map, read_gpx_file, add_segment_to_map

line_options = {'weight': 10}

API_KEY = '<insert-your-apikey-here>'
the_map = create_folium_map()

# Make use of the Thunderforest Outdoors map:
tile_settings1 = {
    'tiles': (
        'https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=' +
        API_KEY
    ),
    'name': 'Thunderforest Outdoors',
    'attr': (
        '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>,'
        ' &copy; <a href="https://www.openstreetmap.org/copyright">'
        'OpenStreetMap</a> contributors'
    )
}
# Create a tile layer and add it to the map:
tile_layer1 = folium.TileLayer(**tile_settings1)
the_map.add_child(tile_layer1, name=tile_layer1.tile_name)

# Make use of the Thunderforest Landscape map:
tile_settings2 = {
    'tiles': (
        'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=' +
        API_KEY
    ),
    'name': 'Thunderforest Landscape',
    'attr': (
        '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>,'
        ' &copy; <a href="https://www.openstreetmap.org/copyright">'
        'OpenStreetMap</a> contributors'
    )
}
# Create a tile layer and add it to the map:
tile_layer2 = folium.TileLayer(**tile_settings2)
the_map.add_child(tile_layer2, name=tile_layer2.tile_name)

folium.LayerControl(sortLayers=True).add_to(the_map)

# Add a track:
for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, line_options=line_options)

# To store the map as a HTML page:
# the_map.save('map_007.html')

# To display the map in a Jupyter notebook:
the_map
