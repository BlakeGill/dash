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
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/FeatureTable_All.csv', sep=';')

app.layout = html.Div(children=[
    html.H1(children='Status of Channels'),
        dcc.Dropdown(id='Channel-dropdown', multi=True,
        options = [
            {'label': 'A1', 'Value' : 'A1_All'},
            {'label': 'A2', 'Value' : 'A2_All'},
            {'label': 'A3', 'Value' : 'A3_All'}
        ],),
        html.Div(id='dd-output'),
        dcc.Graph(id='line-fig,', figure={})
    ])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)

@app.callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='Channel-dropdown', component_property='value')

)

def update_graph(selected_channel):
    dff = df[df.State==selected_channel]
    return [{'label': c, 'value': c} for c in sorted(dff.Column.unique)]

def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=False)