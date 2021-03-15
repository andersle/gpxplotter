# gpxplotter

[![Documentation Status](https://readthedocs.org/projects/gpxplotter/badge/?version=latest)](https://gpxplotter.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/andersle/gpxplotter/master?filepath=%2Flectures)

*gpxplotter* is a Python package for reading 
[gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format)
files and creating simple plots.

The intended usage is for displaying heart rate information together with
other information (e.g. elevation and time). 

It uses [matplotlib](http://matplotlib.org/) to create some simple predefined plots and
[folium](https://python-visualization.github.io/folium/) for creating maps.

Please see
[https://gpxplotter.readthedocs.io/en/latest/](https://gpxplotter.readthedocs.io/en/latest/)
for the latest documentation.

## Installation

gpxplotter can be installed via pip:

``pip install gpxplotter``

## Examples

Interactive examples can be explored
via [Binder](https://mybinder.org/v2/gh/andersle/gpxplotter/master?filepath=%2Flectures)


#### Simple example for showing a track in a map, colored by heart rate

```python

from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map

the_map = create_folium_map()
for track in read_gpx_file('ruten.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='hr')

# To display the map in a Jupyter notebook:
the_map
```

[![map](examples/images/map001.png)](examples/html/map001.html)
