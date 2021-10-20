import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-12-14-14_influxdb_data.csv')

app = dash.Dash()


#'#group', 'false', 'false.1', 'true', 'true.1', 'false.2', 'false.3', 'true.2', 'true.3'
fig = px.line(df, x='_time', y='_value')
fig.update_yaxes(categoryorder='category ascending', type='log', tick0=0, dtick=1)

fig.show()

if __name__ == '__main__':
    app.run_server()

    for group, dataframe in fields:
        dataframe = df.sort_values(by=['_time'])
        trace = go.line(x='_time',
                        y='value',
                        marker=dict(color=colors[len(data)]),
                        name=group)
        data.append(trace)

    layout = go.Layout(xaxis={'title: Time'},
                       # yaxis={'title: Status'},
                       # hovermode='closest')
                       figure=go.Figure(data=data, layout=layout)
    figure.show()
