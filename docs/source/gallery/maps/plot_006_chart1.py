# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding a chart to a map (vincent)
=================================

In this example we will add the elevation profile as a chart
to the map. The chart is placed inside a popup.
"""
import json

import folium
import numpy as np
import vincent

from gpxplotter import add_segment_to_map, create_folium_map, read_gpx_file

line_options = {"weight": 8}

the_map = create_folium_map(tiles="kartverket_topo4")
for track in read_gpx_file("example3.gpx"):
    for i, segment in enumerate(track["segments"]):
        add_segment_to_map(
            the_map,
            segment,
            color_by="hr-zone-float",
            cmap="viridis",
            line_options=line_options,
        )

# Create a chart using vincent
idx = np.argmax(segment["elevation"])

data = {
    "x": segment["Distance / km"],
    "y": segment["elevation"],
}

WIDTH = 400
HEIGHT = 200


line = vincent.Line(data, iter_idx="x", width=WIDTH, height=HEIGHT)
line.axis_titles(x="Distance / km", y="Elevation / m")
line.x_axis_properties(title_offset=2)
line.y_axis_properties(title_offset=-10)
line_json = line.to_json()
line_dict = json.loads(line_json)


popup = folium.Popup(max_width=WIDTH + 50, show=True)
chart = folium.Vega(line_dict, width=WIDTH + 50, height=HEIGHT + 50)
chart.add_to(popup)

marker = folium.Marker(
    location=segment["latlon"][idx],
    popup=popup,
    icon=folium.Icon(icon="star"),
)
marker.add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_006_chart1.html')

# To display the map in a Jupyter notebook:
the_map
