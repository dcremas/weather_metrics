from pathlib import Path

import pandas as pd
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, RangeTool, HoverTool, Paragraph
from bokeh.plotting import figure, curdoc
from bokeh.themes import Theme

from models import airports, data, headers, update

df = pd.DataFrame(data, columns=headers)
df['time'] = np.array(df['time'], dtype=np.datetime64)
dates = np.array(df['time'], dtype=np.datetime64)
source = ColumnDataSource(data=dict(date=df[df['station_name'] == airports[0]]['time'],
                                    temp=df[df['station_name'] == airports[0]]['temp_f'],
                                    pressure=df[df['station_name'] == airports[0]]['pressure_in'],
                                    humidity=df[df['station_name'] == airports[0]]['humidity'],
                                    wind=df[df['station_name'] == airports[0]]['wind_mph'],
                                    precip=df[df['station_name'] == airports[0]]['precip_in']))

plot_bp = figure(tools="xpan", x_axis_type="datetime", x_axis_location="above",
                 y_range=(28.5, 31.5),
                 height=400, width=400, margin=(10, 10, 10, 15), 
                 background_fill_color="#ebf2ff", 
                 sizing_mode="stretch_width")
plot_bp.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Time', '@date{%I:%M %p}'), ('Pressure', '@pressure{0.2f}')],
                         formatters={'@date': 'datetime'}, mode='vline'))
plot_bp.line('date', 'pressure', source=source)
plot_bp.circle('date', 'pressure', source=source, fill_color="white", size=2)
plot_bp.yaxis.axis_label = 'Barometric Pressure'

plot_temp = figure(tools="xpan", x_axis_type="datetime", x_axis_location="above",
                   y_range=(-25.0, 125.0),
                   height=400, width=400, margin=(10, 10, 10, 15), 
                   background_fill_color="#feffeb", 
                   sizing_mode="stretch_width")
plot_temp.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Time', '@date{%I:%M %p}'), ('Temperature', '@temp{0.2f}')],
                         formatters={'@date': 'datetime'}, mode='vline'))
plot_temp.line('date', 'temp', source=source)
plot_temp.circle('date', 'temp', source=source, fill_color="white", size=2)
plot_temp.yaxis.axis_label = 'Temperature'

plot_humid = figure(tools="xpan", x_axis_type="datetime", x_axis_location="above",
                   y_range=(0.0, 100.0),
                   height=400, width=400, margin=(10, 10, 10, 15), 
                    background_fill_color="#ebf2ff", 
                   sizing_mode="stretch_width")
plot_humid.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Time', '@date{%I:%M %p}'), ('Humidity', '@humidity{0.2f}')],
                         formatters={'@date': 'datetime'}, mode='vline'))
plot_humid.line('date', 'humidity', source=source)
plot_humid.circle('date', 'humidity', source=source, fill_color="white", size=2)
plot_humid.yaxis.axis_label = 'Humidity'

plot_wind = figure(tools="xpan", x_axis_type="datetime", x_axis_location="above",
                   y_range=(0.0, 50.0),
                   height=400, width=400, margin=(10, 10, 10, 15), 
                   background_fill_color="#feffeb", 
                   sizing_mode="stretch_width")
plot_wind.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Time', '@date{%I:%M %p}'), ('Wind', '@wind{0.2f}')],
                         formatters={'@date': 'datetime'}, mode='vline'))
plot_wind.line('date', 'wind', source=source)
plot_wind.circle('date', 'wind', source=source, fill_color="white", size=2)
plot_wind.yaxis.axis_label = 'Wind'

plot_precip = figure(height=150, width=400, title="", toolbar_location=None,
                     x_axis_type="datetime", y_range=(0.0, 1.0), margin=(10, 10, 10, 15),
                     background_fill_color="#f2f6fc", outline_line_color='white',
                     sizing_mode="stretch_width")

plot_precip.vbar(x="date", top="precip", source=source)
plot_precip.yaxis.axis_label = "Precip"

desc = Div(text=(Path(__file__).parent / "description.html").read_text("utf8"), sizing_mode="stretch_width",
           margin=(2, 2, 5, 15))

def callback(attr, old, new):
    if new == 0:
        data = dict(date=df[df['station_name'] == old]['time'],
                    temp=df[df['station_name'] == old]['temp_f'],
                    pressure=df[df['station_name'] == old]['pressure_in'],
                    humidity=df[df['station_name'] == old]['humidity'],
                    wind=df[df['station_name'] == old]['wind_mph'],
                    precip=df[df['station_name'] == old]['precip_in'])
    else:
        data = dict(date=df[df['station_name'] == new]['time'],
                    temp=df[df['station_name'] == new]['temp_f'],
                    pressure=df[df['station_name'] == new]['pressure_in'],
                    humidity=df[df['station_name'] == new]['humidity'],
                    wind=df[df['station_name'] == new]['wind_mph'],
                    precip=df[df['station_name'] == new]['precip_in'])
    source.data = data

select_airport = Select(title="Select Airport:", value="", options=airports, margin=(5, 10, 5, 15))
select_airport.on_change('value', callback)

update_text_1 = f'- The Postgresql AWS Cloud Database that feeds the visuals was last updated:'
update_text_2 = f'- Date: {update.strftime("%d %B, %Y")}'
update_text_3 = f'- Time: {update.strftime("%I:%M:%S %p")}'

p1 = Paragraph(text=update_text_1, width=800, height=10, margin=(25, 25, 5, 15))
p2 = Paragraph(text=update_text_2, width=800, height=10, margin=(5, 25, 5, 15))
p3 = Paragraph(text=update_text_3, width=800, height=10, margin=(5, 25, 25, 15))

hyperlink_github = Div(
    text="""<p><i>To see the full codebase for this interactive web-based visualization: </i><a href="https://github.com/dcremas/weather_metrics">Link to my github account</a></p>""",
    width=800, height=25, margin=(10, 10, 10, 15)
    )

hyperlink_div = Div(
    text="""<a href="https://dataviz.dustincremascoli.com">Go back to Data Visualizations Main Page</a>""",
    width=400, height=100, margin=(10, 10, 10, 15)
    )

curdoc().add_root(column(desc, hyperlink_github, select_airport,
                         row(plot_bp, plot_temp, sizing_mode="inherit"),
                         row(plot_humid, plot_wind, sizing_mode="inherit"),
                         row(plot_precip, sizing_mode="inherit"),
                         p1, p2, p3, hyperlink_div,
                         sizing_mode="stretch_width"))

curdoc().theme = Theme(filename="theme.yaml")
curdoc().title = '10 Day Historical & Forecasted Weather Metrics'
