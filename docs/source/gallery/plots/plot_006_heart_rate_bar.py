# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Bar chart of heart rate zones
=============================

This example will use the calculated heart rate zones from
gpxplotter to show the fraction of time spent in the different
zones.
"""
from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap
from gpxplotter import read_gpx_file
from gpxplotter.common import format_time_delta, heart_rate_zone_limits
import numpy as np
plt.style.use('seaborn-talk')


MAX_HEART_RATE = 189


for track in read_gpx_file('example4.gpx', max_heart_rate=MAX_HEART_RATE):
    for j, segment in enumerate(track['segments']):
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

        limits = heart_rate_zone_limits(max_heart_rate=MAX_HEART_RATE)
        zone_txt = {
            0: f'$<${int(limits[0][0])} bpm',
            1: f'{int(limits[0][0])}‒{int(limits[0][1])} bpm',
            2: f'{int(limits[1][0])}‒{int(limits[1][1])} bpm',
            3: f'{int(limits[2][0])}‒{int(limits[2][1])} bpm',
            4: f'{int(limits[3][0])}‒{int(limits[3][1])} bpm',
            5: f'$>${int(limits[3][1])} bpm',
        }

        zones = sorted(list(time_in_zones.keys()))
        percent = {
            key: 100 * val / sum_time for key, val in time_in_zones.items()
        }
        labels = [
            f'Zone {i} ({zone_txt[i]})\n({percent[i]:.1f}%)' for i in zones
        ]
        values = [time_in_zones[i] for i in zones]
        times = format_time_delta(values)
        cmap = get_cmap(name='Reds')
        colors = cmap(np.linspace(0, 1, len(zones) + 1))
        colors = colors[1:]  # Skip the first color
        fig, ax1 = plt.subplots(constrained_layout=True)
        rects = ax1.barh(zones, values, align='center', tick_label=labels)
        for i, recti in enumerate(rects):
            recti.set_facecolor(colors[i])
            width = int(recti.get_width())
            yloc = recti.get_y() + recti.get_height() / 2
            ax1.annotate(
                times[i],
                xy=(width, yloc),
                xytext=(3, 0),
                textcoords="offset points",
                ha='left', va='center',
                fontsize='x-large'
            )
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.tick_params(bottom=False)
        ax1.tick_params(labelbottom=False)
plt.show()
