import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output


def convert_status_file_to_csv():
    # import pandas as pd
    delimiter = '\t'
    decimal = '.'
    csv_file = "https://raw.githubusercontent.com/BlakeGill/dash/master/AMU_10.201.161.151_StatusFile_20160817_21.txt"
    df_all = pd.read_csv (csv_file, sep=delimiter, decimal=decimal, low_memory=False,
                          encoding='unicode_escape')

    csv_file1 = "https://raw.githubusercontent.com/BlakeGill/dash/master/AMU_10.201.161.151_StatusFile_20160817_21.csv"
    featuretable = df_all.copy ()
    featuretable['Date Time'] = pd.to_datetime (featuretable['Date Time'], format='%Y-%m-%d %H:%M:%S.%f',
                                                errors='ignore')
    featuretable.to_csv (csv_file1, index=False, sep=';', decimal=',')

print(csv_file1)
