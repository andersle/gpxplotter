# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Simple plot with matplotlib (2)
===============================

This example will combine some information into a single
plot with matplotlib.
"""
from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap
from gpxplotter import read_gpx_file
import numpy as np
plt.style.use('seaborn-talk')


for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        time = segment['time']
        time_in_zones = {}
        for start, stop, value in segment['hr-regions']:
            seconds = (time[stop] - time[start]).seconds
            if value not in time_in_zones:
                time_in_zones[value] = 0
            time_in_zones[value] += seconds
        sum_time = sum([val for _, val in time_in_zones.items()])
        # Check consistency:
        print('Times are equal?', sum_time == (time[-1] - time[0]).seconds)

        zones = sorted(list(time_in_zones.keys()))
        percent = {
            key: 100 * val / sum_time for key, val in time_in_zones.items()
        }
        labels = [f'Zone {i}\n({percent[i]:.1f}%)' for i in zones]
        values = [time_in_zones[i] for i in zones]
        cmap = get_cmap(name='Reds')
        colors = cmap(np.linspace(0, 1, 6))
        colors = colors[1:]  # Skip the color for zone = 0
        fig, ax1 = plt.subplots(constrained_layout=True)
        ax1.pie(
            values,
            colors=colors,
            labels=labels,
            labeldistance=1.15,
            wedgeprops={'width': 0.45, 'linewidth': 3, 'edgecolor': 'w'},
            textprops={'fontsize': 'x-large', 'ha': 'center'},
            normalize=True,
            startangle=90,
            counterclock=False,
        )
        ax1.set(aspect='equal')
        ax1.text(
            0, 0, 'Time in\nheart rate zones',
            fontdict={'fontsize': 'x-large', 'ha': 'center', 'va': 'center'},
        )
plt.show()
