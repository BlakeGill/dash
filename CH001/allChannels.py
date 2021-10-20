import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State

app = dash.Dash()

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/ch001%20%26%20ch002%20-%202021-10-19-15-01_influxdb_data.csv')

app.layout = html.Div(children=[
    html.H1(children='Status of Channels'),
    dcc.Dropdown(id='Channel-Dropdown',
                 options=[{'label': i, 'value': i}
                          for i in df['_field'].unique()],
                 value='Ch002_accrest_g'),
    dcc.Graph(id='status-graph')

])
@app.callback(
    Output(component_id='status-graph', component_property='figure'),
    Input(component_id='Channel-Dropdown', component_property='value')
)

def update_graph(selected_channel):
    dff = df[df['_field'] == selected_channel]
    print(dff)
    line_fig = px.line(dff, x='_time', y='_value')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=False)