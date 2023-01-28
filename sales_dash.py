import os
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from MoneyAfterDark import NarcoAnalytics as narc, Montana as mn, TaxTools as tax
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
app = Dash(__name__)

slash = '/'
path = os.getcwd()
export_loc = path + slash + "Exports"

sales = pd.read_csv(path + slash + "calex.csv", infer_datetime_format=True)

x = [sales]
for i in x:
    narc.set_dates(i)
    
df = narc.split_dates(sales,format='period')

app.layout = html.Div([
    
    html.H1(children="Personal Training"),

    dcc.Dropdown(id="slct-timescale",
                options=[
                    {"label":"Package", "value": 'package'},
                    {"label":"Payment Type", "value": 'payment type'}],
                 multi=False,
                 value="package",
                 style={'width':"40%"}
                ),

    html.Div(id='output_container',children=[]),
    html.Br(),
    dcc.Graph(id='d',figure={})
]
)
@app.callback(
    Output(component_id='d', component_property='figure'),
    [Input(component_id='slct-timescale', component_property='value')]
)

def aggs(selected):
    
    x = mn.gr_aggregate(df,df.index,selected,'payment')

if __name__ == '__main__':
    app.run_server(host='localhost',port=1000)