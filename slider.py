#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import geopandas as gpd

from bokeh.io import curdoc
from bokeh.plotting import figure, show, save, output_file
import bokeh.models
from bokeh.models import LogColorMapper,ColorBar
from bokeh.layouts import widgetbox, row, column
# from bokeh.palettes import brewer
from bokeh.palettes import RdPu9 as palette

# Output inline in the notebook
output_file('Slider.html',
            title='Average sold price around trainstations')

trainlines = gpd.read_file(r'D:\viz\trainlines\viz_layers.gpkg', layer='railway')
clyde = gpd.read_file(r'D:\viz\trainlines\viz_layers.gpkg', layer='river')
# stations  contains schematics geometry and calculated price
stations = gpd.read_file(r'd:\viz\trainlines\derived\New folder\station_price.gpkg', layer='price_dz_points')
station_labels = gpd.read_file(r'D:\viz\trainlines\viz_layers.gpkg', layer='railstation_labels')
stations['mean'] = pd.to_numeric(stations['mean']).round()
station_labels['name'] = station_labels['name'].str.upper()

subway = gpd.read_file(r'D:\viz\trainlines\viz_layers.gpkg', layer='subway')
subway_labels = gpd.read_file(r'D:\viz\trainlines\viz_layers.gpkg', layer='subway_lables')
subway_labels['name'] = subway_labels['name'].str.upper()

tsource = bokeh.models.ColumnDataSource(trainlines)
stsource = bokeh.models.ColumnDataSource(stations)
ssource = bokeh.models.ColumnDataSource(subway)
slsource = bokeh.models.ColumnDataSource(subway_labels)
stlsource = bokeh.models.ColumnDataSource(station_labels)


def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list(exterior.coords.xy[0])
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list(exterior.coords.xy[1])


def getLineCoords(row, geom, coord_type):
    """Returns a list of coordinates ('x' or 'y') of a LineString geometry"""
    if coord_type == 'x':
        return list(row[geom].coords.xy[0])
    elif coord_type == 'y':
        return list(row[geom].coords.xy[1])


def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y


# Calculate x and y coordinates of the line
trainlines['x'] = trainlines.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
trainlines['y'] = trainlines.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

clyde['x'] = clyde.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
clyde['y'] = clyde.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

# Calculate x and y coordinates of the points
subway['x'] = subway.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
subway['y'] = subway.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

subway_labels['x'] = subway_labels.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
subway_labels['y'] = subway_labels.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

stations['x'] = stations.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
stations['y'] = stations.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

station_labels['x'] = station_labels.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
station_labels['y'] = station_labels.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

stations['x'] = stations.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
stations['y'] = stations.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

# Make a copy, drop the geometry column and create ColumnDataSource
tr_df = trainlines.drop('geometry', axis=1).copy()
trsource = bokeh.models.ColumnDataSource(tr_df)

# Make a copy, drop the geometry column and create ColumnDataSource
cl_df = clyde.drop('geometry', axis=1).copy()
clsource = bokeh.models.ColumnDataSource(cl_df)

# Make a copy, drop the geometry column and create ColumnDataSource
s_df = subway.drop('geometry', axis=1).copy()
ssource = bokeh.models.ColumnDataSource(s_df)

# Make a copy, drop the geometry column and create ColumnDataSource
sl_df = subway_labels.drop('geometry', axis=1).copy()
slsource = bokeh.models.ColumnDataSource(sl_df)

# Make a copy, drop the geometry column and create ColumnDataSource
st_df = stations.drop('geometry', axis=1).copy()
stsource = bokeh.models.ColumnDataSource(st_df)

# Make a copy, drop the geometry column and create ColumnDataSource
stl_df = station_labels.drop('geometry', axis=1).copy()
stlsource = bokeh.models.ColumnDataSource(stl_df)

p3 = figure(plot_width=1150, plot_height=800, title='The darker/bigger the circle is the higher is the average property price',
            title_location='above',
            toolbar_location=None)

# Add clyde on top of the same figure
p3.multi_line('x', 'y', source=clsource, color="#5e96cb", line_width=14, line_cap='round', line_join='round')
# Add clyde additional styling 
##TO-DO find a better way to achieve similar styling result
p3.multi_line('x', 'y', source=clsource, color="white", line_width=12, line_cap='round', line_join='round')
p3.multi_line('x', 'y', source=clsource, color="#98bcde", line_width=10, line_cap='round', line_join='round')

# Add trainlines on top of the same figure
p3.multi_line('x', 'y', source=trsource, color="#B0B0B0", line_width=7, line_cap='round', line_join='round')
# just for styling
p3.multi_line('x', 'y', source=trsource, color="white", line_width=5, line_cap='round', line_join='round')
p3.multi_line('x', 'y', source=trsource, color="#B0B0B0", line_width=3, line_cap='round', line_join='round')

# Add subway on top (as black points)
subway = p3.circle('x', 'y', size=12, source=ssource, color="#99cc00", fill_alpha=0.5)
# labels for subway
labels2 = bokeh.models.LabelSet(x='x', y='y', text='name',
                                text_font='calibri', text_font_style='italic', text_font_size='7pt', text_color='#0e3271',
                                x_offset=-5,
                                # level='glyph',
                                source=slsource, render_mode='canvas')
#  angle = 30,angle_units='deg',x_offset=-15, y_offset=10,y_offset=10, x_offset=-15,
# lables for stations
labels1 = bokeh.models.LabelSet(x='x', y='y', x_offset=-5, y_offset=10,
                                text_font='calibri', text_font_style='italic', text='name', text_font_size='7pt',
                                text_color='#696969',
                                # level='glyph',#angle = 30,angle_units='deg',
                                source=stlsource, render_mode='canvas')

# Flip the colors in color palette
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

# colour based on mean value
#palette = RdPu9
colormap = bokeh.models.LinearColorMapper(palette=palette, low=min(stsource.data['mean']), high=max(stsource.data['mean']))

size_mapper = bokeh.models.LinearInterpolator(
    x=[min(stsource.data['mean']), max(stsource.data['mean'])],
    y=[5, 50]
)
stations = p3.circle(x="x", y="y", source=stsource, color={'field': 'mean', 'transform': colormap},
                     size={'field': 'mean', 'transform': size_mapper})
# Hover tool referring to our own data field using @ and
# a position on the graph using $
h = bokeh.models.HoverTool(tooltips=[('Price ', '@mean'), ('Year', '@year')])


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # Set the year name to slider.value and new_data to source.data
    year = slider.value
    stsource.data = st_df[st_df.year == year]


# Make a slider object: slider
slider = bokeh.models.Slider(title='Year', start=2008, end=2020, step=1, value=2012)

# Hover tool referring to our own data field using @ and
# a position on the graph using $
p3.add_tools(h)
p3.hover.renderers = [stations]


#colormap1 = LinearColorMapper(palette='Viridis256' , low=min(stsource.data['mean']), high=max(stsource.data['mean']))
tick_labels = {'100000':'100K','150000':'150K','200000':'200K','250000':'250K','300000':'300K','350000':'350K','500000':'500K','750000':'750K','950000':'950K'}
color_bar = ColorBar(color_mapper=colormap, width=8,major_label_overrides=tick_labels,major_label_text_font_size="10pt",
                     #title ='Price, £',title_text_align = 'center',
                     label_standoff=15, border_line_color=None,location=(-5,0))
p3.add_layout(color_bar, 'right')
# removing grid lines

p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None

# hiding axis
p3.axis.visible = False

p3.add_layout(labels1)
p3.add_layout(labels2)
# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Make a row layout of widgetbox(slider) and plot and add it to the current document##
#layout = row(widgetbox(slider), p3)
layout = column(widgetbox(slider), p3)
curdoc().add_root(layout)
