import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/all-accrest-channels-2021-10-20-14-02_influxdb_data.csv')

app.layout = html.Div(children=[
    html.H1(children='Status of Channels'),
    dbc.Col([
        <img src=
    ], width={'order':1}
),
    dbc.Col([
    dcc.Dropdown(id='Channel-dropdown', multi=True, value=['Ch000_accrest_g'],
                 options=[{'label': i, 'value': i}
                          for i in sorted(df['_field'].unique())],
                 ),
    dcc.Graph(id='status-graph', figure={})
    ], width={'order':2})
])

@app.callback(
    Output(component_id='status-graph', component_property='figure'),
    Input(component_id='Channel-dropdown', component_property='value')
)

def update_graph(selected_channel):
    dff = df[df['_field'].isin(selected_channel)]
    line_fig = px.line(dff, x='_time', y='_value', color='_field')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=False)