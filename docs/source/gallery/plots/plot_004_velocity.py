# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding velocity
===============

This example will plot the elevation as a
function of distance and color the plot
according to the velocity.
"""
from matplotlib import pyplot as plt
from gpxplotter import read_gpx_file, plot_filled
plt.style.use('seaborn-talk')

for track in read_gpx_file('example1.gpx'):
    for i, segment in enumerate(track['segments']):
        # Convert m -> km:
        segment['Distance / km'] = segment['distance'] / 1000.
        segment['Velocity / km/h'] = segment['velocity'] * 3.6
        # Plot elevation as function of distance:
        plot_filled(track, segment, xvar='Distance / km', yvar='elevation',
                    zvar='Velocity / km/h')
plt.show()