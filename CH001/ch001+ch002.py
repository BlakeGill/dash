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
df001 = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/2021-10-12-14-14_influxdb_data.csv')
df002 = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/ch002%20-2021-10-19-15-36_influxdb_data.csv')

df['_time'] = pd.to_datetime(df['_time'])
df = df.groupby(['_time', '_value', '_field'], as_index=False)['_value'].mean()
df = df.set_index('_time')
#print(df[:5])
df = df.loc['2016-01-01':'2019-12-31']
df = df.groupby([pd.Grouper(freq="S"),'_field'])['_value'].mean().reset_index()


app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ], className='nine columns'),

    html.Div([

        html.Br(),
        html.Label(['Choose which channel:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='channel one',
                     options=[{'label': x, 'value': x} for x in
                              df.sort_values('_field')['_field'].unique()],
                     value='Ch001_accrest_g',
                     multi=False,
                     disabled=False,
                     clearable=True,
                     searchable=True,
                     placeholder='Choose Channel...',
                     className='form-dropdown',
                     style={'width': "90%"},
                     persistence='string',
                     persistence_type='memory'),

    ],className='column')
])

#-------------------------------------------------------------------

@app.callback(
    Output(component_id='our_graph' , component_property='figure')
    [Input(component_id='channel one', component_property='value'),
     Input(component_id='channel two', component_property='value'), ]
)

def build_graph(first_channel, second_channel):
    dff = df[(df['_field'] == first_channel)|
           (df['_field'] == second_channel)]
    print(dff[:5])

    fig=px.line(dff, x='Time', y='Status', color='_field', height=600)
    fig.update_layout(yaxis={'title':'Negative point'},
                      title={'text':'Status of channels'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)