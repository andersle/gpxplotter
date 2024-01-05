# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Elevation profiles - line plots
===============================

This example will use the plotting methods of
gpxplotter to plot the elevation as a
function of distance and elapsed time.
"""
import seaborn as sns
from matplotlib import pyplot as plt

from gpxplotter import plot_line, read_gpx_file

sns.set_context("notebook")

for track in read_gpx_file("example1.gpx"):
    for i, segment in enumerate(track["segments"]):
        # Plot elevation as function of distance:
        plot_line(track, segment, xvar="Distance / km", yvar="elevation")
        # Plot elevation as function of elapsed time:
        plot_line(track, segment, xvar="elapsed-time", yvar="elevation")
        # Repeat plots, but color by heart rate:
        plot_line(
            track,
            segment,
            xvar="Distance / km",
            yvar="elevation",
            zvar="hr",
            lw=10,
        )
        plot_line(
            track,
            segment,
            xvar="elapsed-time",
            yvar="elevation",
            zvar="hr",
            lw=10,
        )
plt.show()
