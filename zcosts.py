import os
import datetime as dt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from MoneyAfterDark import NarcoAnalytics as narc, Montana as mn, TaxTools as tax
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from zapp import app

slash = '/'
path = os.getcwd()
export_loc = path + slash + "Exports"
costs = pd.read_csv(path + slash + "spending.csv", infer_datetime_format=True)
pack = pd.read_csv(path + slash + "packages.csv", infer_datetime_format=True)
#clients = pd.read_csv(path + slash + "clients.csv", infer_datetime_format=True)
sales = pd.read_csv(path + slash + "calex.csv", infer_datetime_format=True)
x = [costs,pack,sales]
for i in x:
    narc.set_dates(i)
c = narc.split_dates(costs,format='period')
s = narc.split_dates(sales,format='period')

