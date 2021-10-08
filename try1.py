import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://gist.githubusercontent.com/omarish/5687264/raw/7e5c814ce6ef33e25d5259c1fe79463c190800d9/mpg.csv')

app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='Hello World!'),
    html.div(children='Dash: a framework'),

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
