========================================
Welcome to |gpxplotter|'s documentation!
========================================

|gpxplotter| is a small package for reading `.gpx` files and
generating plots and maps using `matplotlib <https://www.matplotlib.org/>`_
and `folium <https://python-visualization.github.io/folium/>`_.
The source code for |gpxplotter| can be found
at Github: https://github.com/andersle/gpxplotter.

Here is
a short example of the usage of |gpxplotter|
(please see :ref:`examples-maps` and :ref:`examples-plots` for more examples):


.. literalinclude:: gallery/maps/plot_001_heart_rate.py
   :lines: 3-

.. raw:: html

   <iframe src="_static/map_001.html" height="500px" width="100%"></iframe>



Installing |gpxplotter|
=======================

|gpxplotter| can be installed via  `pip <https://pypi.org/project/gpxplotter/>`_:

.. code-block:: bash

    pip install gpxplotter


.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   auto_examples_maps/index
   auto_examples_plots/index
   source/gpxplotter
