import pandas as pd
import requests
import json
import numpy as np
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
import os

response = requests.get("https://api.tfl.gov.uk/BikePoint/")

names = [response.json()[i]["commonName"] for i in range(len(response.json()))]
lats = [response.json()[i]["lat"] for i in range(len(response.json()))]
longs = [response.json()[i]["lon"] for i in range(len(response.json()))]
bikes = [response.json()[i]["additionalProperties"][6]["value"] for i in range(len(response.json()))]
spaces = [response.json()[i]["additionalProperties"][7]["value"] for i in range(len(response.json()))]
df = pd.DataFrame(data=zip(names, lats, longs, bikes, spaces), columns=["name", 'latitude', 'longitude', 'bikes', 'spaces'])

df["url"] = np.where(df.bikes == "0", "static/borisbw.png", 'static/boris.png')
df["width"] = 300
df["height"] = 300

output_file("boris.html")

TOOLTIPS = [
    ("Location", "@name"),
    ("Available Bikes", "@bikes"),
    ("Spaces Left", "@spaces"),
]

map_options = GMapOptions(lat=51.5, lng=-0.125, map_type="roadmap", zoom=14)
title = "Boris Bikes - Hover over each Boris to find out how many bikes and spaces are available (a black and white Boris symbolises no bikes available!)"
p = gmap(GOOGLE_API_KEY, map_options, title=title, height=800, width=1200,
         tools=['hover', 'reset', 'wheel_zoom', 'pan'])
p.axis.visible = False
source = ColumnDataSource(data=df)

p.circle(x="longitude", y="latitude", size=15, fill_alpha=0, line_alpha=0, source=source) #for the tooltips
p.image_url(url="url", x="longitude", y="latitude", w="width", h="height", source=source, anchor="center")
p.add_tools(HoverTool(tooltips=TOOLTIPS))

show(p)



