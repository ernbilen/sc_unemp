from bokeh.io import show,curdoc, output_notebook
from bokeh.models import LogColorMapper, Slider,ColumnDataSource, HoverTool, GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import Viridis6 as palette
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import widgetbox, row, column
import pandas as pd
import geopandas as gpd

df_final2 = pd.read_pickle('df_final.pkl')


from bokeh.plotting import figure, output_file, show, save
import math
from bokeh.io import output_notebook, show
output_notebook()
'''
us_states = us_states.data.copy()
us_counties = us_counties.data.copy()
unemployment = unemployment.data
counties = {
    code: county for code, county in counties.items() if county["state"] == "sc"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

import pandas as pd


df = pd.read_csv('/Users/owner/Downloads/sc_unemployment.csv',names = ['county', 'year', 'rate'], skiprows = 1)
df['id'] = pd.factorize(df.county)[0]
df2 = pd.DataFrame({'xs': county_xs, 'ys': county_ys})
df2['id'] = df2.index
df_final=pd.merge(df, df2, left_on='id', right_on='id', how='left')
'''

##############################################
#
#
#
#
from bokeh.io import show,curdoc
from bokeh.models import LogColorMapper, Slider,ColumnDataSource, HoverTool, GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import Viridis6 as palette
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import widgetbox, row, column
import pandas as pd
import geopandas as gpd

from bokeh.palettes import brewer

#Input GeoJSON source that contains features for plotting.
source = ColumnDataSource(data={
    'xs':list(df_final2[df_final2['year']==2007]['xs']),
    'ys':list(df_final2[df_final2['year']==2007]['ys']),
    'name':list(df_final2[df_final2['year']==2007]['county']),
    'rate':list(df_final2[df_final2['year']==2007]['rate']),
    'year':list(df_final2[df_final2['year']==2007]['year'])}
)

#Define a sequential multi-hue color palette.
palette2 = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
palette2 = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette2, low = 2, high = 10)

TOOLS = "pan,wheel_zoom,reset,hover,save"



#Define custom tick labels for color bar.
tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Country/region','@county'),('% obesity', '@rate')])

#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

#Create figure object.
p = figure(
    title="South Carolina Unemployment, 2007", tools=TOOLS, plot_width=600, plot_height=500,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ])

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure.
p.patches('xs','ys', source = source, fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

#Specify figure layout.
p.add_layout(color_bar, 'below')

def update_plot(attr, old, new):
    # Set the yr name to slider.value and new_data to source.data
    yr = slider.value
    new_data = {
    'xs':list(df_final2[df_final2['year']==yr]['xs']),
    'ys':list(df_final2[df_final2['year']==yr]['ys']),
    'name':list(df_final2[df_final2['year']==yr]['county']),
    'rate':list(df_final2[df_final2['year']==yr]['rate']),
    'year':list(df_final2[df_final2['year']==yr]['year']),
}
    source.data = new_data
    p.title.text = 'South Carolina Unemployment, %d' %yr

# Make a slider object: slider
slider = Slider(title = 'Year',start = 2007, end = 2018, step = 1, value = 2007)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)

#Display figure inline in Jupyter Notebook.
output_notebook()

#Display figure.
show(layout)
