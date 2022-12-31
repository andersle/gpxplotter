# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Adding overlays
===============

This example will create a map, add a track and some
overlays that will display the steepness.
"""
from branca.element import MacroElement
from jinja2 import Template
import folium
from gpxplotter import (
    create_folium_map,
    read_gpx_file,
    add_segment_to_map,
)
line_options = {'weight': 8}

the_map = create_folium_map(tiles='kartverket_topo4')

for track in read_gpx_file('example3.gpx'):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, line_options=line_options)

steepness = folium.WmsTileLayer(
    url='https://nve.geodataonline.no/arcgis/services/Bratthet/MapServer/WmsServer?',
    layers='Bratthet_snoskred',
    fmt='image/png',
    opacity=0.7,
    transparent=True,
    name='Steepness',
)
steepness.add_to(the_map)


# Add some custom code to show a legend:
class Legend(MacroElement):
    """Just add a hard-coded legend template."""
    _template = Template(u"""
        {% macro header(this,kwargs) %}
            <style>
                .info {
                    padding: 6px 8px;
                    font: 14px/16px Arial, Helvetica, sans-serif;
                    background: white;
                    background: rgba(255,255,255,0.8);
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    border-radius: 5px;
                }
                .info h4 {
                    margin: 0 0 5px;
                    color: #777;
                }
                .legend {
                    line-height: 18px;
                    color: #555;
                }
                .legend i {
                    width: 18px;
                    height: 18px;
                    float: left;
                    margin-right: 8px;
                    opacity: 0.7;
                }
            </style>
        {% endmacro %}

        {% macro script(this,kwargs) %}
            var legend = L.control({position: 'bottomright'});
            legend.onAdd = function (map) {

                var div = L.DomUtil.create('div', 'info legend'),
                steep = [27, 30, 35, 40, 45, 50, 90];
                colors = ['#13711d', '#fff93e', '#ffa228', '#ff4e11',
                          '#f50000', '#7c0000'];
                labels = ['Degrees'];
                for (var i = 0; i < steep.length - 1; i++) {
                    labels.push(
                        '<i style="background:' + colors[i] + '"></i> ' +
                        steep[i] + '&ndash;' + steep[i + 1]);
                }
                div.innerHTML += labels.join('<br>');
                return div;
            };
            legend.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)


the_map.add_child(Legend())

# Add layer control:
folium.LayerControl(sortLayers=True).add_to(the_map)

# To store the map as a HTML page:
# the_map.save('map_008.html')

# To display the map in a Jupyter notebook:
the_map
