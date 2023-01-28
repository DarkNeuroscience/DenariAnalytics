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

costs = pd.read_csv(path + slash + "spending.csv", infer_datetime_format=True)

x = [costs]
for i in x:
    narc.set_dates(i)
    
df = narc.split_dates(costs,format='period')

app.layout = html.Div([
    
    html.H1(children="Personal Training"),

    dcc.Dropdown(id="slct-aggregate",
                options=[
                    {"label":"Shop", "value": 'shop'},
                    {"label":"Category", "value": 'type'}],
                 multi=False,
                 value="shop",
                 style={'width':"40%"}
                ),

    html.Div(id='output_container',children=[]),
    html.Br(),
    dcc.Graph(id='d',figure={})
]
)
@app.callback(
    Output(component_id='d', component_property='figure'),
    [Input(component_id='slct-aggregate', component_property='value')]
)

def aggs(selected):
    
    x = group_aggregate(df,'month',selected,'cost','sum')
    
if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)