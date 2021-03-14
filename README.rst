##########
gpxplotter
##########

``gpxplotter`` is a Python package for reading .gpx [1]_ files and make some simple plots.
It uses `matplotlib <http://matplotlib.org/>`_ to create some simple predefined plots and
`folium <https://python-visualization.github.io/folium/>`_ for making maps.


Examples
========

Simple example for plotting an elevation profile with heart rate
----------------------------------------------------------------

.. literalinclude:: examples/python/plot1.py

.. image:: examples/images/plot1.png
   :scale: 50 %
   :alt: Example output
   :align: center

Simple example for showing a track in a map, colored by heart rate
------------------------------------------------------------------

.. code:: python

   from gpxplotter import read_gpx_file
   from gpxplotter.mplplotting import plot_map, save_map
   
   
   for track in read_gpx_file('test.gpx'):
       for i, segment in enumerate(track['segments']):
           fig = plot_map(track, segment, zcolor='pulse')
           save_map(fig, 'test-{}.html'.format(i))


.. image:: examples/images/test-hr-map.png
   :scale: 50 %
   :alt: Example output
   :align: center


Installation
============

gpxplotter can be installed via pip:

``pip install gpxplotter``


Note
====
The intended usage is for displaying heart rate information together with
other information (e.g. elevation and time). 


References
==========

.. [1] https://en.wikipedia.org/wiki/GPS_Exchange_Format
