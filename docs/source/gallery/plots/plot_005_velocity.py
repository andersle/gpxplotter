# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Inspecting velocity
===================

This example will inspect the calculated velocities.
"""
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from gpxplotter import read_gpx_file, plot_filled, plot_line
from gpxplotter.common import cluster_velocities
plt.style.use('seaborn-talk')

for track in read_gpx_file('example1.gpx'):
    for i, segment in enumerate(track['segments']):
        fig, (axi, axj) = plt.subplots(constrained_layout=True, ncols=2)
        # First draw a histogram:
        axi.hist(segment['velocity'], bins=100)
        axi.set_title('Histogram of velocities')
        axi.set(xlabel='Velocity / m/s', ylabel='Frequency')
        # Add clustering of velocities for grouping them into levels:
        level = cluster_velocities(segment['velocity'], n_clusters=6)
        scatter = axj.scatter(segment['time'], segment['velocity'], c=level, cmap='viridis')
        axj.legend(
            *scatter.legend_elements(num=len(set(level))),
            title='Velocity level'
        )
        axj.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        axj.tick_params(axis='x', rotation=25)
        axj.set(xlabel='Time', ylabel='Velocity')
        # The velocity levels is also calculated when loading the gpx-file:
        plot_filled(track, segment, xvar='Distance / km', yvar='elevation',
                    zvar='velocity-level')
        # The number of levels can be changed by updating the
        # velocity-level:
        segment['velocity-level'] = cluster_velocities(segment['velocity'], n_clusters=6)
        plot_filled(track, segment, xvar='Distance / km', yvar='elevation',
                    zvar='velocity-level')
        plot_line(track, segment, xvar='Distance / km', yvar='elevation',
                    zvar='velocity-level', cmap='Spectral_r')
plt.show()
