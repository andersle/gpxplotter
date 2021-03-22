# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines methods for interfacing with folium."""
import folium
import branca.colormap
from gpxplotter.common import RELABEL


TILES = {
    'kartverket_topo4': {
        'name': 'Kartverket (topo4)',
        'tiles': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    },
    'kartverket_topo4graatone': {
        'name': 'Kartverket (topo4graatone)',
        'tiles': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4graatone&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    },
    'opentopomap': {
        'name': 'OpenTopoMap',
        'tiles': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        'attr': (
            'Map data: &copy; '
            '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap'
            '</a> contributors, <a href="http://viewfinderpanoramas.org">'
            'SRTM</a> | Map style: &copy; <a href="https://opentopomap.org'
            '">OpenTopoMap</a> (<a href="https://creativecommons.org/licen'
            'ses/by-sa/3.0/">CC-BY-SA</a>)'
        ),
    },
    'ersi.worldtopomap': {
        'name': 'Esri.WorldTopoMap',
        'tiles': (
            'https://server.arcgisonline.com/ArcGIS/rest/services/'
            'World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
        ),
        'attr': (
            'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, '
            'TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase,'
            ' Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri'
            ' China (Hong Kong), and the GIS User Community'
        ),
    },
    'esri_worldimagery': {
        'name': 'Esri_WorldImagery',
        'tiles': (
            'https://server.arcgisonline.com/ArcGIS/rest/services/'
            'World_Imagery/MapServer/tile/{z}/{y}/{x}'
        ),
        'attr': (
            'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, '
            'USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP'
            ', and the GIS User Community'
        ),
    },
}


_FOLIUM_TILES = ('openstreetmap', 'stamenterrain')


def create_folium_map(**kwargs):
    """Create a folium map.

    This method is essentially the same as calling
    ``folium.Map(**kwargs)``, with a few differences:

    * ``control_scale = True`` by default.
    * ``tiles`` can be ``"openstreetmap"`` or ``"stamenterrain"`` or
      any of the tiles defined in :py:const:`.TILES`.

    Parameters
    ----------
    kwargs : optional
        Arguments passed to the method generating the map,
        see :py:func:`folium.Map`.

    Returns
    -------
    the_map : object like :py:class:`folium.folium.Map`
        The map created here.

    """
    # Add a few defaults:
    kwargs['control_scale'] = kwargs.get('control_scale', True)
    tiles = kwargs.get('tiles', None)
    if tiles is None:
        the_map = folium.Map(**kwargs)
    else:
        if tiles in _FOLIUM_TILES:
            the_map = folium.Map(**kwargs)
        else:
            if tiles in TILES:
                tile_layer = folium.TileLayer(**TILES[tiles])
                kwargs['tiles'] = None
                the_map = folium.Map(**kwargs)
                the_map.add_child(tile_layer, name=tile_layer.tile_name)
    return the_map


def add_tiles_to_map(the_map, *tiles):
    """Add pre-defined tiles to the given map.

    Parameters
    ----------
    the_map : object like :py:class:`folium.folium.Map`
        The map to add tiles to.
    tiles : list of strings
        The name of the tiles to add.

    """
    for tile in tiles:
        if tile in _FOLIUM_TILES:
            folium.TileLayer(tile).add_to(the_map)
        else:
            if tile in TILES:
                tile_layer = folium.TileLayer(**TILES[tile])
                the_map.add_child(tile_layer, name=tile_layer.tile_name)


def add_start_top_markers(the_map, segment):
    """Add markers for the start and end of the segment.

    Parameters
    ----------
    the_map : object like :py:class:`folium.folium.Map`
        The map to add the markers to.
    segment : dict
        The segment to use for finding the start and end points.

    """
    start_time = segment['time'][0].strftime('%A %B %d, %Y: %H:%M:%S')
    start = folium.Marker(
        location=segment['latlon'][0],
        tooltip='Start',
        popup=folium.Popup(start_time, max_width=250),
        icon=folium.Icon(icon='ok', color='green'),
    )
    start.add_to(the_map)
    end_time = segment['time'][-1].strftime('%A %B %d, %Y: %H:%M:%S')
    stop = folium.Marker(
        location=segment['latlon'][-1],
        tooltip='End',
        popup=folium.Popup(end_time, max_width=250),
        icon=folium.Icon(icon='home', color='lightgray'),
    )
    stop.add_to(the_map)


def add_segment_to_map(the_map, segment, color_by=None, cmap='viridis',
                       line_options=None, fit_bounds=True, add_start_end=True):
    """Add a segment as a line to a map.

    This method will add a segment as a line to the given map. The line
    can be colored according to values selected by the parameter
    ``color_by``.

    Parameters
    ----------
    the_map : object like :py:class:`folium.folium.Map`
        The map to add the segment to.
    segment : dict
        The segment to add.
    color_by : string, optional
        This string selects what property we will color the segment
        according to. If this is None, the segment will be displayed
        with a single color.
    cmap : string
        The colormap to use if ``color_by != None``.
    line_options : dict
        Extra control options for drawing the line.
    fit_bounds : boolean, optional
        Determines if we try to fit the map so the whole segment
        is shown.
    add_start_end : boolean, optional
        If True, this method will add markers at the start/end of the
        segment.

    """
    if color_by is None:
        if line_options is None:
            line_options = {}
        line = folium.features.PolyLine(segment['latlon'], **line_options)
        line.add_to(the_map)
    else:
        add_colored_line(the_map, segment, color_by, cmap=cmap,
                         line_options=line_options)
    if add_start_end:
        add_start_top_markers(the_map, segment)
    if fit_bounds:
        boundary = the_map.get_bounds()
        the_map.fit_bounds(boundary, padding=(3, 3))


def add_colored_line(the_map, segment, color_by, cmap='viridis',
                     line_options=None):
    """Add segment as a colored line to a map.

    Add a line colored by some value to the given map.

    Parameters
    ----------
    the_map : object like :py:class:`folium.folium.Map`
        The map to add the segment to.
    segment : dict
        The segment to add.
    color_by : string
        This string selects what property we will color the segment
        according to.
    cmap : string
        The colormap to use for coloring.
    line_options : dict
        Extra control options for drawing the line.

    """
    zdata = segment[color_by]
    avg = 0.5 * (zdata[1:] + zdata[:-1])
    minz, maxz = min(avg), max(avg)
    uniq = len(set(zdata))
    if uniq < 10:
        levels = uniq + 1
    else:
        levels = 10
    linmap = getattr(branca.colormap.linear, cmap)
    colormap = linmap.scale(minz, maxz).to_step(levels)
    colormap.caption = RELABEL.get(color_by, color_by)
    if line_options is None:
        line_options = {'weight': 6}
    line_options['weight'] = line_options.get('weight', 6)
    line = folium.ColorLine(positions=segment['latlon'], colormap=colormap,
                            colors=avg, control=False, **line_options)
    line.add_to(the_map)
    the_map.add_child(colormap)
