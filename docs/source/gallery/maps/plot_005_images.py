# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding images to a map
======================

In this example we will add some images to the map, these
are placed in the map by matching time and location information
from the image.
"""
import datetime
from gpxplotter import create_folium_map, read_gpx_file, add_segment_to_map
import folium
import numpy as np
import PIL
from PIL.ExifTags import TAGS, GPSTAGS


line_options = {'weight': 8}

the_map = create_folium_map()
for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='hr-zone-float',
                           cmap='viridis', line_options=line_options)

# Display initial map:
the_map


# Create a method to get coordinates from an image:
def get_lat_lon(imagefile):
    image = PIL.Image.open(imagefile)
    exif = image.getexif()
    exif_info = {TAGS.get(key, key): val for key, val in exif.items()}
    # Get the GPSInfo:
    for key, value in TAGS.items():
        if value == "GPSInfo":
            exif_info[value] = exif.get_ifd(key)
            break
    gps_info = {}
    for key, val in exif_info["GPSInfo"].items():
        gps_info[GPSTAGS.get(key, key)] = val
    # Convert to decimal latitude/longitude:
    deg, minutes, seconds = gps_info["GPSLatitude"]
    latitude = deg + minutes / 60.0 + seconds / 3600.0
    if "GPSLatitudeRef" == "S":
        latitude *= -1
    deg, minutes, seconds = gps_info["GPSLongitude"]
    longitude = deg + minutes / 60.0 + seconds / 3600.0
    if "GPSLongitudeRef" == "W":
        longitude *= -1
    # Turn time into datetime:
    time = datetime.datetime.strptime(
        exif_info["DateTime"], "%Y:%m:%d %H:%M:%S"
    )
    return latitude, longitude, time

info = {}
for filename in ('image1.jpg', 'image2.jpg', 'image3.jpg'):
    #lat, lon, time = get_lat_lon(f'../../_static/{filename}')
    lat, lon, time = get_lat_lon(f'../../_static/{filename}')
    info[filename] = {'latlon': (lat, lon), 'time': time}


# Add, markers to the gps-locations we read from the images
for key, val in info.items():
    marker = folium.Marker(
        location=val['latlon'],
        tooltip=f'You took a picture here? {key} says so...',
        icon=folium.Icon(icon='camera', color='red'),
    )
    marker.add_to(the_map)
boundary = the_map.get_bounds()
the_map.fit_bounds(boundary, padding=(3, 3))

# To store the map as a HTML page:
# the_map.save('map_005_v1.html')

# Display updated map:
the_map

# As can be seen in the map above, the GPS locations in the
# image files may be a bit off.
# Let's try to see if we can use the time information to place them better.
# Note: The best approach is probably to make your GPS devise show its
# current time, and then take a photo of it with your phone. This can
# be used to "align" time-stamps from the two devices better.

# Time read from the images does not contain time zone information, so it's
# difficult to compare with the timestamps from the GPS device.
# Here, I remember when I started so I will use that.

time_offset = datetime.timedelta(seconds=2*3600)  # time_offset is 2 hours
for key, val in info.items():
    time = val['time']
    times = [i.replace(tzinfo=None) + time_offset for i in segment['time']]
    time_diff = []
    for i in times:
        if i < time:
            time_diff.append((time - i).seconds)
        else:
            time_diff.append((i - time).seconds)
    minidx = np.argmin(time_diff)
    info[key]['latlon_time'] = segment['latlon'][minidx]

# Mark the gps-locations we interpolated using time:
the_map = create_folium_map(
    zoom_start=18,
    location=info['image1.jpg']['latlon_time']
)
add_segment_to_map(
    the_map, segment, line_options=line_options, fit_bounds=False,
    color_by='hr-zone-float',
)
colors = ['blue', 'red', 'green']
for i, (key, val) in enumerate(info.items()):
    show = i == 0  # Open the first one.
    popup = folium.Popup(
        f'<img alt="{key}" src="../_static/{key}", width=200/>',
        show=show
    )
    marker = folium.Marker(
        location=val['latlon_time'],
        popup=popup,
        icon=folium.Icon(icon='camera', color=colors[i]),
    )
    marker.add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_005_v2.html')

# To display the map in a Jupyter notebook:
the_map
