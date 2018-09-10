# -*- coding: utf-8 -*-
# Copyright (c) 2018, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for plotting GPX data using matplotlib."""
from math import floor, ceil
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.patches as mpatches
from matplotlib import gridspec
from matplotlib import pyplot as plt
import mplleaflet
from mplleaflet.maptiles import tiles
from gpxplotter.common import heart_rate_zone_limits, format_time_delta


ZONE_COLORS_0 = {
    1: '#ffffcc',
    2: '#a1dab4',
    3: '#41b6c4',
    4: '#2c7fb8',
    5: '#253494'
}
ZONE_COLORS_1 = {
    1: '#e41a1c',
    2: '#377eb8',
    3: '#4daf4a',
    4: '#984ea3',
    5: '#ff7f00',
}
ZONE_COLORS = {
    0: '#bcbddc',
    1: '#9e9ac8',
}


def make_patches(xdata, ydata, zdata, cmap_name='viridis'):
    """Make some patches for multi-coloring the area under a curve.

    Parameters
    ----------
    xdata : list or numpy.array or similar
        The x positions for the curve.
    ydata : list or numpy.array or similar
        The y positions for the curve.
    zdata : list or numpy.array or similar
        A list of values associated with each point, used for
        coloring.
    cmap_name : string, optional
        The name of the color map to use.

    Returns
    -------
    out[0] : object like :py:class:`.PolyCollection`
        The polygons created here, with individual colors.
    out[1] : list of floats
        The colors associated with the given ``zdata``.
    out[2] : object like :py:class:`matplotlib.colors.ListedColormap`
        The created color map.
    out[3] : object like :py:class:`matplotlib.colors.Normalize`
        The created normalization for the data.

    """
    cmap = get_cmap(cmap_name)
    norm = Normalize(vmin=floor(min(zdata)), vmax=ceil(max(zdata)))
    colors = [cmap(norm(i)) for i in zdata]
    verts = []
    for i, (xval, yval) in enumerate(zip(xdata, ydata)):
        if i == 0:
            xnext = 0.5 * (xdata[i + 1] + xval)
            ynext = 0.5 * (ydata[i + 1] + yval)
            verts.append([
                [xval, 0], [xval, yval], [xnext, ynext], [xnext, 0]
            ])
        elif i == len(xdata) - 1:
            xprev = 0.5 * (xval + xdata[i - 1])
            yprev = 0.5 * (yval + ydata[i - 1])
            verts.append([
                [xprev, 0], [xprev, yprev], [xval, yval], [xval, 0]
            ])
        else:
            xnext = 0.5 * (xdata[i + 1] + xval)
            ynext = 0.5 * (ydata[i + 1] + yval)
            xprev = 0.5 * (xval + xdata[i - 1])
            yprev = 0.5 * (yval + ydata[i - 1])
            verts.append([
                [xprev, 0], [xprev, yprev], [xval, yval],
                [xnext, ynext], [xnext, 0]
            ])
    return (PolyCollection(verts, facecolors=colors, edgecolors=colors),
            colors, cmap, norm)


def _make_time_labels(delta_seconds, nlab=5):
    """Make n time formatted labels for data i seconds"""
    label_pos = np.linspace(min(delta_seconds), max(delta_seconds),
                            nlab, dtype=np.int_)
    label_lab = format_time_delta(label_pos)
    return label_pos, label_lab


def plot_elevation_hr(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    ax1.set_facecolor('0.90')
    xdata = data['delta-seconds']
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    handles = []
    legends = []
    for i in data['hr-regions']:
        xpos = xdata[i[0]:i[1]+1]
        ypos = ydata[i[0]:i[1]+1]
        idx = 0 if i[2] < 3 else 1
        ax1.fill_between(xpos, 0, ypos, alpha=1.0,
                         color=ZONE_COLORS[idx])
    patch = mpatches.Patch(color=ZONE_COLORS[0])
    legend = r'Zone $\leq$ 2'
    handles.append(patch)
    legends.append(legend)
    patch = mpatches.Patch(color=ZONE_COLORS[1])
    legend = 'Zone > 2'
    handles.append(patch)
    legends.append(legend)
    ax1.legend(handles, legends)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    label_pos, label_lab = _make_time_labels(xdata, 5)
    ax1.set_xticks(label_pos)
    ax1.set_xticklabels(label_lab, rotation=25)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_elevation_hr_dist(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    ax1.set_facecolor('0.90')
    xdata = data['distance'] / 1000.
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    handles = []
    legends = []
    for i in data['hr-regions']:
        xpos = xdata[i[0]:i[1]+1]
        ypos = ydata[i[0]:i[1]+1]
        idx = 0 if i[2] < 3 else 1
        ax1.fill_between(xpos, 0, ypos, alpha=1.0,
                         color=ZONE_COLORS[idx])
    patch = mpatches.Patch(color=ZONE_COLORS[0])
    legend = r'Zone $\leq$ 2'
    handles.append(patch)
    legends.append(legend)
    patch = mpatches.Patch(color=ZONE_COLORS[1])
    legend = 'Zone > 2'
    handles.append(patch)
    legends.append(legend)
    ax1.legend(handles, legends)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    ax1.set_xlabel('Distance / km')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_elevation_hrz(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_facecolor('0.90')
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    xdata = data['delta-seconds']
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    handles = []
    legends = []
    for i in data['hr-regions']:
        xpos = xdata[i[0]:i[1]+1]
        ypos = ydata[i[0]:i[1]+1]
        ax1.fill_between(xpos, 0, ypos, alpha=1.0,
                         color=ZONE_COLORS_0[i[2]])
    for i in range(1, 6):
        patch = mpatches.Patch(color=ZONE_COLORS_0[i])
        legend = 'Zone = {}'.format(i)
        handles.append(patch)
        legends.append(legend)
    ax1.legend(handles, legends)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    label_pos, label_lab = _make_time_labels(xdata, 5)
    ax1.set_xticks(label_pos)
    ax1.set_xticklabels(label_lab, rotation=25)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_elevation_hrz_dist(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_facecolor('0.90')
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    xdata = data['distance'] / 1000.
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    handles = []
    legends = []
    for i in data['hr-regions']:
        xpos = xdata[i[0]:i[1]+1]
        ypos = ydata[i[0]:i[1]+1]
        ax1.fill_between(xpos, 0, ypos, alpha=1.0,
                         color=ZONE_COLORS_0[i[2]])
    for i in range(1, 6):
        patch = mpatches.Patch(color=ZONE_COLORS_0[i])
        legend = 'Zone = {}'.format(i)
        handles.append(patch)
        legends.append(legend)
    ax1.legend(handles, legends)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    ax1.set_xlabel('Distance / km')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_elevation_hr_multi(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ncol = 20
    grid = gridspec.GridSpec(1, ncol)
    ax1 = fig.add_subplot(grid[:, :ncol-1])
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    cbarax = fig.add_subplot(grid[:, ncol-1])
    ax1.set_facecolor('0.90')
    xdata = data['delta-seconds']
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    poly, _, cmap, norm = make_patches(xdata, ydata, data['pulse'],
                                       cmap_name='viridis')
    _ = ColorbarBase(cbarax, cmap=cmap, norm=norm, label='Heart rate / bpm')
    ax1.add_collection(poly)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    label_pos, label_lab = _make_time_labels(xdata, 5)
    ax1.set_xticks(label_pos)
    ax1.set_xticklabels(label_lab, rotation=25)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_elevation_hr_multi_dist(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ncol = 20
    grid = gridspec.GridSpec(1, ncol)
    ax1 = fig.add_subplot(grid[:, :ncol-1])
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    cbarax = fig.add_subplot(grid[:, ncol-1])
    ax1.set_facecolor('0.90')
    xdata = data['distance'] / 1000.
    ydata = data['ele']
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    poly, _, cmap, norm = make_patches(xdata, ydata, data['pulse'],
                                       cmap_name='viridis')
    _ = ColorbarBase(cbarax, cmap=cmap, norm=norm, label='Heart rate / bpm')
    ax1.add_collection(poly)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    ax1.set_xlabel('Distance / km')
    ax1.set_ylabel('Elevation / m')
    fig.tight_layout()
    return fig


def plot_hr(data, maxpulse=187):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_facecolor('0.90')
    xdata = data['delta-seconds']
    ydata = data['pulse']
    handles = []
    legends = []
    zones = heart_rate_zone_limits(maxpulse=maxpulse)
    for i, zone in enumerate(zones):
        patch = mpatches.Patch(color=ZONE_COLORS_0[i+1])
        legend = 'Zone = {}'.format(i + 1)
        handles.append(patch)
        legends.append(legend)
        ax1.axhspan(zone[0], zone[1], color=ZONE_COLORS_0[i+1])
    ax1.plot(xdata, ydata, color='#262626', lw=3)
    ax1.legend(handles, legends)
    ax1.set_ylim(min(ydata) - 2, max(ydata) + 2)
    label_pos, label_lab = _make_time_labels(xdata, 5)
    ax1.set_xticks(label_pos)
    ax1.set_xticklabels(label_lab, rotation=25)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Heart rate / bpm')
    fig.tight_layout()
    return fig


def plot_hr_time(data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_facecolor('0.90')
    xdata = data['delta-seconds']
    handles = []
    legends = []
    zones = {i + 1: 0 for i in range(5)}
    for i in data['hr-regions']:
        xpos = xdata[i[0]:i[1]+1]
        zones[i[2]] += (xpos[-1] - xpos[0])
    total_time = xdata[-1]
    for key, val in zones.items():
        ax1.bar(key, val / total_time, 1.0, align='center',
                color=ZONE_COLORS_0[key])
        patch = mpatches.Patch(color=ZONE_COLORS_0[key])
        legend = 'Zone {}'.format(key)
        handles.append(patch)
        legends.append(legend)
    ax1.text(
        0.05,
        0.90,
        'Average heart rate: {}'.format(int(np.round(data['average-hr']))),
        transform=ax1.transAxes,
        fontsize=20,
    )
    ax1.legend(handles, legends)
    ax1.set_xlabel('Zone')
    ax1.set_ylabel('Fraction of time')
    fig.tight_layout()
    return fig


def save_fig(fig, name):
    """Just store a figure."""
    fig.savefig(name)


def monkey_patch_tiles(mpltiles):
    """Add some new tiles to the mplleaflet."""
    mpltiles['norgeskart_topo4'] = (
        (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4&zoom={z}&x={x}&y={y}'
        ),
        (
            'Copyright: Kartverket - see http://www.statkart.no/nor/Land/'
            'Kart_og_produkter/visningstjenester/'
        )
    )
    mpltiles['norgeskart_toporaster3'] = (
        (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=toporaster3&zoom={z}&x={x}&y={y}'
        ),
        (
            'Copyright: Kartverket - see http://www.statkart.no/nor/Land/'
            'Kart_og_produkter/visningstjenester/'
        ),
    )


def plot_map(track, data, zcolor='pulse'):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    xdata = data['lon']
    ydata = data['lat']
    zdata = data[zcolor]
    cmap = get_cmap('viridis')
    norm = Normalize(vmin=floor(min(zdata)), vmax=ceil(max(zdata)))
    colors = [cmap(norm(i)) for i in zdata]
    for i, (xval, yval) in enumerate(zip(xdata, ydata)):
        try:
            ax1.plot([xval, xdata[i + 1]], [yval, ydata[i + 1]],
                     color=colors[i], lw=4)
        except IndexError:
            break
    fig.tight_layout()
    return fig


def plot_map_zones(track, data):
    """Plot the elevation profile with heart rate annotations."""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('{}: {}'.format(track['name'][0], track['type'][0]))
    xdata = data['lon']
    ydata = data['lat']
    for i, (xval, yval, zone) in enumerate(zip(xdata, ydata, data['hr-zone'])):
        try:
            ax1.plot([xval, xdata[i + 1]], [yval, ydata[i + 1]],
                     color=ZONE_COLORS_1[zone])
        except IndexError:
            break
    fig.tight_layout()
    return fig


def save_map(fig, name, tile='norgeskart_topo4'):
    """Just store a map."""
    mplleaflet.show(path=name, fig=fig, tiles=tile)


monkey_patch_tiles(tiles)
