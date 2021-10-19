import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-19-11-52_influxdb_data.csv')

app = dash.Dash()

fig = px.line(df, x='_time', y='_value')
fig.update_yaxes(categoryorder='category ascending', type='log', tick0=0, dtick=1)

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=['_time', 'Ch001_accrest_g'],
                    label='Ch001_accrest_g',
                    method='restyle'
                ),
                dict(
                    args=['_time', 'Ch001_acpeak_g'],
                    label='Ch001_acpeak_g',
                    method='restyle'
                ),
            ]),
            direction='down',
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        )
    ]
)


fig.show()

if __name__ == '__main__':
    app.run_server()