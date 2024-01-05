# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Annotate a map with folium
==========================

This example will create a map and color the track according
to the elevation. It will then add two folium markers to show
the location of the highest elevation and the highest heart rate.
"""
import folium
import numpy as np

from gpxplotter import add_segment_to_map, create_folium_map, read_gpx_file

the_map = create_folium_map(tiles="kartverket_topo4")
for track in read_gpx_file("example1.gpx"):
    for i, segment in enumerate(track["segments"]):
        # Add track to the map:
        add_segment_to_map(the_map, segment, color_by="elevation")

        # This is sufficient to add the segment to the map.
        # Here we will add some extra markers using folium:
        # 1) Add marker at highest elevation:
        idx = np.argmax(segment["elevation"])
        value = segment["elevation"][idx]
        time = segment["time"][idx].strftime("%A %B %d, %Y, %H:%M:%S")
        hrate = segment["heart rate"][idx]
        distance = segment["distance"][idx] / 1000.0
        txt = (
            f"The highest elevation was <b>{value:g} m</b>:"
            "<ul>"
            f"<li> Time: {time}"
            f"<li> Distance: {distance:.2f} km"
            f"<li> Heart rate: {hrate:g} bpm"
            "</ul>"
        )
        high = folium.Marker(
            location=segment["latlon"][idx],
            tooltip=f"Highest elevation:{value:g} m",
            popup=folium.Popup(txt, max_width=300),
            icon=folium.Icon(icon="star", color="green"),
        )
        high.add_to(the_map)
        # 2) Add marker at highest heart rate:
        idx = np.argmax(segment["heart rate"])
        value = segment["heart rate"][idx]
        time = segment["time"][idx].strftime("%A %B %d, %Y, %H:%M:%S")
        distance = segment["distance"][idx] / 1000.0
        elevation = segment["elevation"][idx]
        txt = (
            f"The highest heart rate was <b>{value:g} bpm</b>:"
            "<ul>"
            f"<li> Time: {time}"
            f"<li> Distance: {distance:.2f} km"
            f"<li> Elevation: {elevation:.2f} m"
            "</ul>"
        )
        high_hr = folium.Marker(
            location=segment["latlon"][idx],
            tooltip=f"Highest heart rate:{value:g} bmp",
            popup=folium.Popup(txt, max_width=300),
            icon=folium.Icon(icon="heart", color="red"),
        )
        high_hr.add_to(the_map)


# To store the map as a HTML page:
# the_map.save('map_002.html')

# To display the map in a Jupyter notebook:
the_map
