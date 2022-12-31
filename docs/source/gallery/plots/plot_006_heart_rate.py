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
from gpxplotter.common import format_time_delta
import numpy as np
import seaborn as sns

sns.set_context("notebook")


MAX_HEART_RATE = 189


for track in read_gpx_file("example4.gpx", max_heart_rate=MAX_HEART_RATE):
    for i, segment in enumerate(track["segments"]):
        time = segment["time"]
        time_in_zones = {}
        for start, stop, value in segment["hr-regions"]:
            seconds = (time[stop] - time[start]).seconds
            if value not in time_in_zones:
                time_in_zones[value] = 0
            time_in_zones[value] += seconds
        sum_time = sum([val for _, val in time_in_zones.items()])
        # Check consistency:
        print("Times are equal?", sum_time == (time[-1] - time[0]).seconds)

        zones = sorted(list(time_in_zones.keys()))
        zone_txt = segment["zone_txt"]

        percent = {
            key: 100 * val / sum_time for key, val in time_in_zones.items()
        }
        values = [time_in_zones[j] for j in zones]
        times = format_time_delta(values)
        labels = []
        for j in zones:
            labels.append(
                f"Zone {j} ({zone_txt[j]})\n"
                f"({times[j][3:]}, {percent[j]:.1f}%)"
            )
        cmap = get_cmap(name="Reds")
        colors = cmap(np.linspace(0, 1, len(zones) + 1))
        colors = colors[1:]  # Skip the first color
        fig, ax1 = plt.subplots(constrained_layout=True)
        patches, _ = ax1.pie(
            values,
            colors=colors,
            # labels=labels,  # Labels may overlap, so this is commented here
            # textprops={'fontsize': 'x-large', 'ha': 'center'},
            labeldistance=1.15,
            wedgeprops={"width": 0.45, "linewidth": 3, "edgecolor": "w"},
            normalize=True,
            startangle=90,
            counterclock=False,
        )
        ax1.set(aspect="equal")

        legend = ax1.legend(
            patches,
            labels,
            loc="upper left",
            bbox_to_anchor=(-0.25, 1.0),
            handlelength=3,
        )  # , fontsize='x-large')
        # Make patches thicker for the legend:
        for patch in legend.get_patches():
            patch.set_height(20)
        ax1.text(
            0,
            0,
            "Time in\nheart rate zones",
            fontdict={"fontsize": "large", "ha": "center", "va": "center"},
        )
plt.show()
