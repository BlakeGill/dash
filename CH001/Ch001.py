import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-12-14-14_influxdb_data.csv')

app = dash.Dash()

values = df['false.3']
values = values[3:]

time = df['false.2']
time = time[3:]  #only using the values required

#'#group', 'false', 'false.1', 'true', 'true.1', 'false.2', 'false.3', 'true.2', 'true.3'
fig = px.line(df, x=time, y=values)
fig.update_yaxes(categoryorder='category ascending', type='log', tick0=0, dtick=1)

fig.show()

if __name__ == '__main__':
    app.run_server()
