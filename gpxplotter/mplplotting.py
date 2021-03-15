# -*- coding: utf-8 -*-
# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for plotting GPX data using matplotlib."""
from math import floor, ceil
import datetime
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from gpxplotter.common import format_time_delta, RELABEL


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
    xdata : list or array_like
        The x positions for the curve.
    ydata : list or array_like
        The y positions for the curve.
    zdata : list or array_like
        A list of values associated with each point, used for
        coloring.
    cmap_name : string, optional
        The name of the color map to use.

    Returns
    -------
    out[0] : object like :py:class:`matplotlib.collections.PolyCollection`
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
    col = PolyCollection(verts, facecolors=colors, edgecolors=colors,
                         cmap=cmap_name)
    return col, colors, cmap, norm


def _make_time_labels(delta_seconds, nlab=5):
    """Make n time-formatted labels for data in seconds"""
    label_pos = np.linspace(min(delta_seconds), max(delta_seconds),
                            nlab, dtype=np.int_)
    label_lab = format_time_delta(label_pos)
    return label_pos, label_lab


def set_up_figure(track):
    """Helper method to create a figure.

    This method will just create the figure and axis and
    set the title.

    Parameters
    ----------
    track : dict
        The track we are creating a figure for.


    Returns
    -------
    fig: object like :py:class:`matplotlib.figure.Figure`
        The figure created here.
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axis created here

    """
    fig, ax1 = plt.subplots(constrained_layout=True)
    ax1.set_title(f'{track["name"][0]}: {track["type"][0]}')
    return fig, ax1


def add_colorbar(figi, axi, patch, zvar, norm):
    """Add colorbar to figure.

    Parameters
    ----------
    figi: object like :py:class:`matplotlib.figure.Figure`
        The figure to add the color bar to.
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to which we add the color bar next to.
    patch : object like :py:class:`matplotlib.cm.ScalarMappable`
        The mappable described by the color bar.
    zvar : string
        The variable we are using for coloring.
    norm :  :py:class:`matplotlib.colors.Normalize`
        The normalization of values for mapping to colors.

    """
    cbar = figi.colorbar(patch, ax=axi)
    cbar.set_label(RELABEL.get(zvar, zvar))
    ticks, ticks_pos = [], []
    for i in cbar.get_ticks():
        ticks.append(f'{norm.inverse(i):g}')
        ticks_pos.append(i)
    cbar.set_ticks(ticks_pos)
    cbar.set_ticklabels(ticks)


def add_regions(axi, xdata, ydata, regions, cut):
    """Add heart rate patches to axis.

    Parameters
    ----------
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to add regions to.
    xdata : array_like
        The x-values we are plotting for.
    ydata : array_like
        The y-values we are plotting for.
    regions : list of lists
        regions[i] defines a heart rate region as [start, stop, hr-region].
    cut : integer, optional
        If given, the zones will be divided into smaller (inclusive) or
        larger than the given cut.

    """
    legends, handles = [], []
    if cut is None:
        for i in regions:
            xpos = xdata[i[0]:i[1]+1]
            ypos = ydata[i[0]:i[1]+1]
            axi.fill_between(xpos, min(ydata), ypos, alpha=1.0,
                             color=ZONE_COLORS_0[i[2]])
        for i in range(1, 6):
            patch = mpatches.Patch(color=ZONE_COLORS_0[i])
            legend = f'Zone = {i}'
            handles.append(patch)
            legends.append(legend)
    else:
        for i in regions:
            xpos = xdata[i[0]:i[1]+1]
            ypos = ydata[i[0]:i[1]+1]
            idx = 0 if i[2] <= cut else 1
            axi.fill_between(
                xpos,
                min(ydata),
                ypos,
                alpha=1.0,
                color=ZONE_COLORS[idx]
            )
        handles.append(mpatches.Patch(color=ZONE_COLORS[0]))
        legends.append(fr'Zone $\leq$ {cut}')
        handles.append(mpatches.Patch(color=ZONE_COLORS[1]))
        legends.append(f'Zone > {cut}')
    axi.legend(handles, legends)


def _get_data(data, key):
    """Attempt to read a key from a dictionary.

    This method is here to give some more instructive error messages.

    Parameters
    ----------
    data : dict
        The dictionary to read from.
    key : string
        The key we attempt to read from the dictionary.

    Returns
    -------
    out : any
        The values returned by ``data[key]``.
    """
    kdata = None
    try:
        kdata = data[key]
    except KeyError as error:
        msg = (
            f'Requested "{key}" not found in data!'
            f'\nValid: {data.keys()}'
        )
        raise Exception(msg) from error
    return kdata


def add_segmented_line(xdata, ydata, zdata, cmap='viridis'):
    """Create multicolored line.

    Create a multicolored line colored after the zdata-values.

    Parameters
    ----------
    xdata : array_like
        x-positions to use.
    ydata : array_like
        y-positions to use.
    zdata : array_like
        Values to use for coloring the line segments.
    cmap : string, optional
        Colormap to use for the colors.

    Returns
    -------
    out : object like :py:class:`matplotlib.collections.LineCollection`
        The multicolored lines.

    Note
    ----
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html

    """
    norm = Normalize(min(zdata), max(zdata))
    points = np.array([xdata, ydata]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lines = LineCollection(segments, cmap=cmap, norm=norm)
    lines.set_array(zdata)
    return lines


def _update_limits(axi, data, which='x', factor=0.025):
    """Update limits for axes (x or y).

    This method will lengthen the given axes.

    Parameters
    ----------
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to update for.
    data : array_like
        The data we are plotting on the given axes.
    which : string, optional
        Determines if we are updating the x or y-axes.
    factor : float, optional
        Half of the factor of the current length to add.

    """
    length = abs(data.max() - data.min())
    if which == 'x':
        axi.set_xlim(
            data.min() - length * factor, data.max() + length * factor
        )
    elif which == 'y':
        axi.set_ylim(
            data.min() - length * factor, data.max() + length * factor
        )
    else:
        pass


def _add_elapsed_labels(axi, data, which='x'):
    """Add nicer labels for time-difference.

    Convert elapsed time in seconds to hours:minutes:seconds.

    Parameters
    ----------
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to add ticks for.
    data : array_like
        The data we are updating.
    which : string, optional
        Selects the axes (x or y) we are updating.

    """
    label_pos, label_lab = _make_time_labels(data, 5)
    if which == 'x':
        axi.set_xticks(label_pos)
        axi.set_xticklabels(label_lab, rotation=25)
        axi.set_xlabel('Time')
    elif which == 'y':
        axi.set_yticks(label_pos)
        axi.set_yticklabels(label_lab)
        axi.set_ylabel('Time')


def _shift_elapsed_labels(axi, start_time, which='x'):
    """Shift elapsed labels with a given time origin.

    Make a time difference start at a given time.

    Parameters
    ----------
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to add ticks for.
    start_time : object like :py:class:`datetime.datetime`
        The starting time to use for shifting.
    which : string, optional
        Selects the axes (x or y) we are updating.

    """
    if which == 'x':
        ticks = axi.get_xticks()
    elif which == 'y':
        ticks = axi.get_yticks()
    else:
        ticks = []
    seconds = [datetime.timedelta(seconds=int(i)) for i in ticks]
    time = [start_time + i for i in seconds]
    time_lab = [i.strftime('%H:%M:%S') for i in time]
    if which == 'x':
        axi.set_xticklabels(time_lab)
    elif which == 'y':
        axi.set_yticklabels(time_lab)


def _update_time_ticklabels(axi, xvar, yvar, xdata, ydata):
    """Update time tick labels for time data.

    Parameters
    ----------
    axi : object like :py:class:`matplotlib.axes.Axes`
        The axes to add ticks for.
    xvar : string
        The variable used for the x-axis.
    yvar : string
        The variable used for the y-axis.
    xdata : array_like
        The data used for the x-axis.
    ydata : array_like
        The data used for the y-axis.

    """
    # Add nicer labels if we have elapsed-time:
    if xvar == 'elapsed-time':
        _add_elapsed_labels(axi, xdata, which='x')
    elif xvar == 'time':
        fmt = mdates.DateFormatter("%H:%M:%S")
        axi.xaxis.set_major_formatter(fmt)
        axi.tick_params(axis='x', rotation=25)
    if yvar == 'elapsed-time':
        _add_elapsed_labels(axi, ydata, which='y')
    elif yvar == 'time':
        fmt = mdates.DateFormatter("%H:%M:%S")
        axi.yaxis.set_major_formatter(fmt)


def plot_line(track, data, xvar='distance', yvar='elevation', zvar=None,
              **kwargs):
    """Plot line data from a segment.

    Plot a given segment from a track as a line. The line
    can be colored according to a given value.

    Parameters
    ----------
    track : dict
        The track we are plotting for.
    data : dict
        The segment we are plotting.
    xvar : string, optional
        Selects the variable to use for the x-axes.
    yvar : string, optional
        Selects the variable to use for the y-axes.
    zvar : string, optional
        Selects the variable to use for coloring the line.
    **kwargs : matplotlib.lines.Line2D properties, optional
        Extra properties for the plotting passed to the ``axi.plot``
        method.

    Returns
    -------
    fig: object like :py:class:`matplotlib.figure.Figure`
        The figure created here.

    """
    fig, ax1 = set_up_figure(track)
    xdata = _get_data(data, xvar)
    ydata = _get_data(data, yvar)
    ax1.set(xlabel=RELABEL.get(xvar, xvar), ylabel=RELABEL.get(yvar, yvar))
    if zvar is None:
        ax1.plot(xdata, ydata, **kwargs)
    else:
        zdata = _get_data(data, zvar)
        # For time, use the elapsed-time for making the segmented line
        if xvar == 'time':
            xdata = _get_data(data, 'elapsed-time')
        if yvar == 'time':
            ydata = _get_data(data, 'elapsed-time')
        lines = add_segmented_line(xdata, ydata, zdata, cmap='viridis')
        lines.set_linewidth(kwargs.get('lw', 3))
        line = ax1.add_collection(lines)
        _update_limits(ax1, xdata, which='x')
        _update_limits(ax1, ydata, which='y')
        cbar = fig.colorbar(line, ax=ax1)
        cbar.set_label(RELABEL.get(zvar, zvar))
        # Shift back for time:
        if xvar == 'time':
            _add_elapsed_labels(ax1, xdata, which='x')
            xdata = _get_data(data, xvar)
            _shift_elapsed_labels(ax1, xdata[0], which='x')
        if yvar == 'time':
            _add_elapsed_labels(ax1, ydata, which='y')
            ydata = _get_data(data, yvar)
            _shift_elapsed_labels(ax1, ydata[0], which='y')
    _update_time_ticklabels(ax1, xvar, yvar, xdata, ydata)
    return fig


def plot_filled(track, data, xvar='distance', yvar='elevation', zvar='hr',
                cmap='viridis', cut=None, **kwargs):
    """Plot a filled graph (line with colored area).

    Plot a line and fill the area under it, given a specified variable.

    Parameters
    ----------
    track : dict
        The track we are plotting for.
    data : dict
        The segment we are plotting.
    xvar : string, optional
        Selects the variable to use for the x-axes.
    yvar : string, optional
        Selects the variable to use for the y-axes.
    zvar : string, optional
        Selects the variable to use for coloring the area.
    cmap : string, optional
        Color map to use for the coloring
    cut : integer, optional
        If given and if we are plotting hr-regions, this will divide
        the coloring into two different groups (see `.add_regions`).
    **kwargs : matplotlib.lines.Line2D properties, optional
        Extra properties for the plotting passed to the ``axi.plot``
        method.

    Returns
    -------
    fig: object like :py:class:`matplotlib.figure.Figure`
        The figure created here.

    """
    fig, ax1 = set_up_figure(track)
    xdata = _get_data(data, xvar)
    ydata = _get_data(data, yvar)
    zdata = _get_data(data, zvar)
    ax1.set(xlabel=RELABEL.get(xvar, xvar), ylabel=RELABEL.get(yvar, yvar))
    ax1.plot(xdata, ydata, **kwargs)

    if zvar == 'hr-regions':
        add_regions(ax1, xdata, ydata, data[zvar], cut)
    else:
        poly, _, _, norm = make_patches(
            xdata,
            ydata,
            zdata,
            cmap_name=cmap,
        )
        col = ax1.add_collection(poly)
        add_colorbar(fig, ax1, col, zvar, norm)

    _update_time_ticklabels(ax1, xvar, yvar, xdata, ydata)
    return fig
