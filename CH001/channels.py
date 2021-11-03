import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import plotly
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import test_class

# csv source
df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/all%20channels%20-%202021-10-27-12-13_influxdb_data.csv')


# list of channel object
channel = []
parameter = []

for i in df['_field']:
    i=i[:5]
    channel.append(i)

for j in df['_field']:
    j=j[6:]
    parameter.append(j)

# extra user-made columns
df["Channels"] = channel
df["Parameter"] = parameter
print(df)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Label("Channel:", style={'fontSize':30, 'textAlign':'center'}),
        dcc.Dropdown(
            id='channel-dpdn',
            options=[{'label': s, 'value': s} for s in sorted(df["_field"].unique())],
            value=[],
            clearable=False
        ),

    html.Label("Parameter:", style={'fontSize':30, 'textAlign':'center'}),
        dcc.Dropdown(id='parameter-dpdn',
                 options=[],
                 value=[],
                 multi=True),
        html.Div(id='graph-container', children=[])
])


@app.callback(
    Output('parameter-dpdn', 'options'),
    Output('parameter-dpdn', 'value'),
    Input('channel-dpdn', 'value'),
)
def set_parameter_options(chosen_parameter):
    dff = df[df["_field"]==chosen_parameter]
    parameter_of_channel = [{'label': c, 'value': c} for c in sorted(dff["_field"].unique())]
    values_selected = [x['value'] for x in parameter_of_channel]
    return parameter_of_channel, values_selected

@app.callback(
    Output('graph-container', 'children'),
    Input('parameter-dpdn', 'value'),
    Input('channel-dpdn', 'value'),
    prevent_initial_call=True
)

def update_graph(selected_parameters, selected_channels):
    dff = df[(df["_field"]==selected_channels) & (df["_field"].isin(selected_parameters))]
    fig = px.line(dff, x='_time', y='_value' )
    return dcc.Graph(id='display-map', figure=fig)

if __name__ == '__main__':
    app.run_server(debug=False)