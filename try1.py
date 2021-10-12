import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-08-13-48_influxdb_data.csv')

app = dash.Dash()


print(df)
app.layout = html.Div(children=[
    html.H1(children='Hello World!'),
    html.Div(children='Dash: a framework'),

dcc.Graph(
    id='graphid',
    figure={
        'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Cats'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Dogs'},
            ],
            'layout': {
                'title': 'Cats vs Dogs'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server()
