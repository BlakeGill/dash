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

for i in df:
        if '_' not in i:
                pass
        else:
                parameterlist.append([i.split('_', 1)[0]])


print(parameterlist)

df.index = pd.Datetimeindex.df['Date_Time']
print(df)