import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-12-12-57_influxdb_data.csv')

app = dash.Dash()


print(df)
app.layout = html.Div(children=[
    html.H1(children='Hello World!'),
    html.Div(children='Dash: a framework')
])

fig = px.line(df, x='_time', y='_value')
fig.show()

if __name__ == '__main__':
    app.run_server()
