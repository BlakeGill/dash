import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/ch001%20%26%20ch002%20-%202021-10-19-15-01_influxdb_data.csv')
df001 = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-12-14-14_influxdb_data.csv')
df002 = pd.read_csv()


app = dash.Dash()

fig = px.line(df, x='_time', y='_value')
fig.update_yaxes(categoryorder='category ascending', type='log', tick0=0, dtick=1)

fig.show()

if __name__ == '__main__':
    app.run_server()