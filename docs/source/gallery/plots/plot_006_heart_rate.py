# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Pie chart of heart rate zones
=============================

This example will use the calculated heart rate zones from
gpxplotter to show the fraction of time spent in the different
zones.
"""
from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap
from gpxplotter import read_gpx_file
import numpy as np
plt.style.use('seaborn-talk')


for track in read_gpx_file('example4.gpx'):
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
        colors = cmap(np.linspace(0, 1, len(zones) + 1))
        colors = colors[1:]  # Skip the first color
        fig, ax1 = plt.subplots(constrained_layout=True)
        patches, _ = ax1.pie(
            values,
            colors=colors,
            # labels=labels,  # Labels may overlap, so this is commented here
            # textprops={'fontsize': 'x-large', 'ha': 'center'},
            labeldistance=1.15,
            wedgeprops={'width': 0.45, 'linewidth': 3, 'edgecolor': 'w'},
            normalize=True,
            startangle=90,
            counterclock=False,
        )
        ax1.set(aspect='equal')

        legend = ax1.legend(patches, labels, loc='upper left',
                            bbox_to_anchor=(-0.15, 1.),
                            handlelength=3, fontsize='x-large')
        # Make patches thicker for the legend:
        for patch in legend.get_patches():
            patch.set_height(20)
        ax1.text(
            0, 0, 'Time in\nheart rate zones',
            fontdict={'fontsize': 'x-large', 'ha': 'center', 'va': 'center'},
        )
plt.show()
