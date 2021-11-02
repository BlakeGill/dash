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


df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/FeatureTable_All.csv', sep=';')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

statuslist = []
parameterlist = []
channellist = []

for i in df.columns:
        if '_' not in i:
                pass
        else:
                parameterlist.append([i.split('_', 1)[0]])

print(parameterlist)

dcc.Dropdown(id='blank', multi=False,
                         options=[{'label' : x, 'value':x}
                                  for x in sorted(df.columns)]
                         ),
dcc.Graph(id='line-fig,', figure={})

@app.callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='Channel-dropdown', component_property='value')
)
def update_graph(parameterlist):
    dff = df[df[0].isin(parameterlist)]
    line_fig = px.line(dff, x='Date_Time', y='')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=False)