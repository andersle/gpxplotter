# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Elevation profiles - filled plots
=================================

This example will use the plotting methods of gpxplotter
to plot the elevation as a
function of distance and elapsed time.
"""
import seaborn as sns
from matplotlib import pyplot as plt

from gpxplotter import plot_filled, read_gpx_file

sns.set_context("notebook")

for track in read_gpx_file("example1.gpx"):
    for i, segment in enumerate(track["segments"]):
        # Plot elevation as function of distance:
        fig1, _ = plot_filled(
            track, segment, xvar="Distance / km", yvar="elevation", zvar="hr"
        )
        sns.despine(fig=fig1)
        # Plot elevation as function of elapsed time:
        fig2, _ = plot_filled(
            track,
            segment,
            xvar="elapsed-time",
            yvar="elevation",
            zvar="hr",
            cmap="vlag",
        )
        sns.despine(fig=fig2)
plt.show()
