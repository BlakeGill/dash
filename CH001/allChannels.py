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

df = pd.read_csv(
    'https://raw.githubusercontent.com/BlakeGill/dash/master/all%20channels%20-%202021-10-27-12-13_influxdb_data.csv')

#channels = df['field'[:5]]

#print(channels)

#image_filename = 'dashboard.jpg'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(children=[
    html.H1(children='Status of Channels'),
        dbc.Col([
            html.Img(
                dict(
                    source='../dashboard.jpg',
                    xref='x',
                    yref='y',
                    x=0,
                    y=3,
                    sizex=2,
                    sizey=2,
                    sizing='stretch',
                )
                #html.Img(src='data:image/png;base64,{}'.format(encoded_image))
            ), html.H2('Image of system'),
            dcc.Dropdown(id='blank', multi=False,
                         options=[{'label' : x, 'value':x}
                                  for x in sorted(df['_field'].unique())]
                         ),
            dcc.Graph(id='line-fig,', figure={})
        ],

    ),
    dbc.Col([
        dcc.Dropdown(id='Channel-dropdown', multi=True, value=['Ch000_accrest_g'],
                     options=[{'label': i, 'value': i}
                              for i in sorted(df['_field'].unique())],
                     ),
        dcc.Graph(id='status-graph', figure={})
    ], )
])


@app.callback(
    Output(component_id='status-graph', component_property='figure'),
    Input(component_id='blank', component_property='value')
)

@app.callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='Channel-dropdown', component_property='value')
)
def update_graph(selected_channel):
    dff = df[df['_field'].isin(selected_channel)]
    line_fig = px.line(dff, x='_time', y='_value', color='_field')
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=False)
