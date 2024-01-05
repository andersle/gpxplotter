# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Simple plot with matplotlib (2)
===============================

This example will combine some information into a single
plot with matplotlib.
"""
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from gpxplotter import read_gpx_file

sns.set_context("notebook")


def smooth(signal, points):
    """Smooth the given signal using a rectangular window."""
    window = np.ones(points) / points
    return np.convolve(signal, window, mode="same")


colors = sns.color_palette()


for track in read_gpx_file("example3.gpx"):
    for i, segment in enumerate(track["segments"]):
        fig, ax1 = plt.subplots(constrained_layout=True, figsize=(8, 4))
        x = segment["Distance / km"]
        y = segment["elevation"]
        (line1,) = ax1.plot(x, y, lw=3, color=colors[0])
        # Fill the area:
        ax1.fill_between(x, y, y2=y.min(), alpha=0.1)
        ax1.set(xlabel="Distance / km", ylabel="Elevation")
        # Add heart rate:
        ax2 = ax1.twinx()
        # Smooth the heart rate for plotting:
        heart = smooth(segment["hr"], 51)
        (line2,) = ax2.plot(x, heart, color=colors[1], alpha=0.8, lw=3)
        ax2.set_ylim(0, 200)
        ax2.set(ylabel="Heart rate / bpm")
        # Add velocity:
        ax3 = ax1.twinx()
        ax3.spines["right"].set_position(("axes", 1.2))
        # Smooth the velocity for plotting:
        vel = 3.6 * smooth(segment["velocity"], 51)
        (line3,) = ax3.plot(x, vel, alpha=0.8, color=colors[2], lw=3)
        ax3.set(ylabel="Velocity / km/h")
        ax3.set_ylim(0, 20)

        # Style plot:
        axes = (ax1, ax2, ax3)
        lines = (line1, line2, line3)
        for axi, linei in zip(axes, lines):
            axi.yaxis.label.set_color(linei.get_color())
            axi.tick_params(axis="y", colors=linei.get_color())
            key = "right" if axi != ax1 else "left"
            axi.spines[key].set_edgecolor(linei.get_color())
            axi.spines[key].set_linewidth(2)

        ax1.spines["top"].set_visible(False)

        for axi in (ax2, ax3):
            for key in axi.spines:
                axi.spines[key].set_visible(False)
            axi.spines["right"].set_visible(True)

        # Add legend:
        ax1.legend(
            (line1, line2, line3),
            ("Elevation", "Heart rate", "Velocity"),
            loc="upper left",
            frameon=True,
        )
plt.show()
