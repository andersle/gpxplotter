##########
gpxplotter
##########

``gpxplotter`` is a Python package for reading .gpx [1]_ files and make some simple plots.


Example
=======

.. code:: python

   from gpxplotter import read_gpx_file
   from gpxplotter.mplplotting import plot_elevation_hr_multi_dist, save_fig
   from matplotlib import pyplot as plt
   plt.style.use('seaborn-poster')
   
   
   for track in read_gpx_file('test.gpx'):
       for i, segment in enumerate(track['segments']):
           fig = plot_elevation_hr_multi_dist(track, segment)
           save_fig(fig, 'test-{}.png'.format(i))

.. image:: examples/images/test-ele-multi.png
   :scale: 50 %
   :alt: Example output
   :align: center


Installation
============

gpxplot can be installed via pip:

``pip install gpxplot``


References
==========

.. [1] https://en.wikipedia.org/wiki/GPS_Exchange_Format
