========================================
Welcome to |gpxplotter|'s documentation!
========================================

|gpxplotter| is a small package for reading `.gpx` files and
generating plots using `matplotlib <https://www.matplotlib.org/>`_
and maps using `folium <https://python-visualization.github.io/folium/>`_:

.. literalinclude:: gallery/maps/plot_001_heart_rate.py
   :lines: 3-

.. raw:: html

   <iframe src="_static/map_001.html" height="500px" width="100%"></iframe>


Using `folium <https://python-visualization.github.io/folium/>`_, the maps can
be annotated:

.. literalinclude:: gallery/maps/plot_002_annotate.py
   :lines: 3-


.. raw:: html

   <iframe src="_static/map_002.html" height="500px" width="100%"></iframe>
 


Installing |gpxplotter|
=======================

|gpxplotter| can be installed via  `pip <https://pypi.org/project/gpxplotter/>`_:

.. code-block:: bash

    pip install gpxplotter

Obtaining the source code
=========================

The source code for |gpxplotter| can be found in the
`Github repository
<https://github.com/andersle/gpxplotter>`_.

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   auto_examples/index
   source/gpxplotter

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
