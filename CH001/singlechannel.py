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
import matplotlib.pyplot as plt


df = pd.read_csv('C:\\Users\\BGill\\dash\\influxCore-master\\tests\\test.csv', sep=';', decimal='.')

channelList = ['Ch000', 'Ch001', 'Ch002', 'Ch003', 'Ch004', 'Ch005', 'Ch006', 'Ch007', 'Ch008', 'Ch009', 'Ch010',
               'Ch011', 'Ch012', 'Ch013', 'Ch014', 'Ch015', 'Ch016', 'Ch017', 'Ch018', 'Ch019', 'Ch019', 'Ch020',
               'Ch021', 'Ch022', 'Ch023']


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Label("Channel:", style={'fontSize':30, 'textAlign':'center'}),
        dcc.Dropdown(
            id='channel-dpdn',
            options=[{'label': s, 'value': s} for s in channelList],
            clearable=True,
            value=[],

        ),
        html.Div(id='graph-container', children=[])
])

#def Select_Channel():
    #channel = [{'label': s, 'value': s} for s in channelList]
    #values_selected = [x['value'] for x in channel]
    #return channel, values_selected

@app.callback(
    Output('graph-container', 'children'),
    Input('channel-dpdn', 'value'),
    prevent_initial_call = True
)

def update_graph(Channel):
    channel_par_list = ['timestamp']
    par_list = []
    if Channel == 'Ch000' or 'Ch001' or 'Ch002' or 'Ch003':
        par_list.clear()
        par_list = ['accrest_g', 'acpeak_g', 'acrms_g', 'kurtosis_g', 'mean_g', 'peak2peak_g', 'smax_g']
    if Channel == 'Ch004' or 'Ch005':
        par_list.clear()
        par_list = ['accrest_Âµm','acpeak_Âµm','acrms_Âµm','kurtosis_Âµm','mean_Âµm','peak2peak_Âµm','smax_Âµm']
    if Channel == 'Ch006':
        par_list.clear()
        par_list = ['accrest_rpm', 'acpeak_rpm', 'acrms_rpm', 'kurtosis_rpm', 'peak2peak_rpm', 'smax_rpm']
    if Channel == 'Ch007' or 'Ch008' or 'Ch009':
        par_list.clear()
        par_list = ['accrest_V','acpeak_V','acrms_V','kurtosis_V','mean_V','peak2peak_V','smax_V']
    if Channel == 'Ch010' or 'Ch011' or 'Ch012':
        par_list.clear()
        par_list = ['accrest_A', 'acpeak_A', 'acrms_A', 'kurtosis_A', 'mean_A', 'peak2peak_A', 'smax_A']
    if Channel == 'Ch013':
        par_list.clear()
        par_list = ['accrest_Nm', 'acpeak_Nm', 'acrms_Nm', 'kurtosis_Nm', 'mean_Nm', 'peak2peak_Nm', 'smax_Nm']
    if Channel == 'Ch014':
        par_list.clear()
        par_list = ['accrest_Â°C', 'acpeak_Â°C', 'acrms_Â°C', 'kurtosis_Â°C', 'mean_Â°C', 'peak2peak_Â°C', 'smax_Â°C']
    if Channel == 'Ch015':
        par_list.clear()
        par_list = ['accrest_%', 'acpeak_%', 'acrms_%',	'kurtosis_%',	'mean_%',	'peak2peak_%',	'smax_%']
    if Channel == 'Ch016':
        par_list.clear()
        par_list = ['accrest_N', 'acpeak_N', 'acrms_N', 'kurtosis_N', 'mean_N', 'peak2peak_N', 'smax_N']
    #if Channel == 'Ch017' or 'Ch018' or 'Ch019' or 'Ch020' or 'Ch021' or 'Ch022' or 'Ch023':
        #par_list.clear()
        #par_list = ['Â°C']
    for par in par_list:
        channel_par = Channel + '_' + par
        channel_par_list.append(channel_par)
        print(channel_par_list)
    df_channel = df.loc[:, channel_par_list]
    print(df_channel)
    fig = px.line(df_channel, x='timestamp', y=channel_par_list[1:])
    return html.Div([dcc.Graph(id='display-map', figure=fig)])

#Channel="Channel"

if __name__ == '__main__':
    app.run_server(debug=False)
