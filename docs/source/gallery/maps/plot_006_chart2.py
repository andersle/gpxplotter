# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding a chart to a map (altair)
================================

In this example we will add the elevation profile as a chart
to the map. The chart is placed inside a popup.
"""
import json
import folium
from gpxplotter import create_folium_map, read_gpx_file, add_segment_to_map
import numpy as np
import pandas as pd
import altair

line_options = {'weight': 8}

the_map = create_folium_map(tiles='kartverket_topo4')
for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='hr-zone-float',
                           cmap='viridis', line_options=line_options)


idx = np.argmax(segment['elevation'])

WIDTH = 400
HEIGHT = 200


def smooth(signal, points):
    """Smooth the given signal using a rectangular window."""
    window = np.ones(points) / points
    return np.convolve(signal, window, mode='same')


data = pd.DataFrame(
    {
        'dist': segment['Distance / km'],
        'elevation': segment['elevation'],
        'heart': smooth(segment['hr'], 51),
    }
)

area1 = altair.Chart(data).mark_area(
    fillOpacity=0.4, strokeWidth=5, line=True
).encode(
    x=altair.X('dist', title='Distance / km'),
    y=altair.Y('elevation', title='Elevation / m'),
)

line1 = altair.Chart(data).mark_line(
    strokeWidth=5
).encode(
    x=altair.X('dist', title='Distance / km'),
    y=altair.Y('heart', title='Heart rate / bpm'),
    color=altair.value('#1b9e77'),
)
chart = altair.layer(
    area1,
    line1,
    width=WIDTH,
    height=HEIGHT,
).resolve_scale(y='independent')

chart.title = 'Elevation & heart rate profile (altair)'

chart_dict = json.loads(chart.to_json())
popup = folium.Popup(max_width=WIDTH+100, show=True)
chart_vega = folium.features.VegaLite(
    chart_dict,
    width=WIDTH+100,
    height=HEIGHT+50
)
chart_vega.add_to(popup)
marker = folium.Marker(
    location=segment['latlon'][idx],
    popup=popup,
    icon=folium.Icon(icon='star'),
)
marker.add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_006_chart2.html')

# To display the map in a Jupyter notebook:
the_map
