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


df = pd.read_csv('https://raw.githubusercontent.com/BlakeGill/dash/master/FeatureTable_All.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

for i, j in df.iterrows():
    print(i, j)
    print()