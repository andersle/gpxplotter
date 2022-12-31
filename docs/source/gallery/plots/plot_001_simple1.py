# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Simple plot with matplotlib
===========================

This example will just plot the distance as a function
of time.
"""
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from gpxplotter import read_gpx_file
import seaborn as sns

sns.set_context("notebook")

for track in read_gpx_file("example1.gpx"):
    for i, segment in enumerate(track["segments"]):
        fig, ax1 = plt.subplots(constrained_layout=True)
        ax1.plot(segment["time"], segment["distance"] / 1000.0, lw=5)
        ax1.set(xlabel="Time", ylabel="Distance / km")
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        sns.despine(fig=fig)
plt.show()
