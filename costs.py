import os
import datetime as dt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from MoneyAfterDark import NarcoAnalytics as narc, Montana as mn, TaxTools as tax
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

slash = '/'
path = os.getcwd()
export_loc = path + slash + "Exports"
cost = pd.read_csv(path + slash + "spending.csv", infer_datetime_format=True)
pack = pd.read_csv(path + slash + "packages.csv", infer_datetime_format=True)
#clients = pd.read_csv(path + slash + "clients.csv", infer_datetime_format=True)
#sales = pd.read_csv(path + slash + "calex.csv", infer_datetime_format=True)
x = [cost]
for i in x:
    narc.set_dates(i)
c = narc.split_dates(cost,format='period')



costs_layout = html.Div(children=[html.H1('Cost Analysis',style={'textAlign':'center','color':'#503D36','font-size': 40}),
                                  html.P('Cost Analysis', style={'text-align':'center', 'color':'#503D36'}),
                                  html.Div([dcc.Dropdown(id='cdropdown-1', 
                                                         value='year',
                                                         options=[
                                                             {'label': 'year', 'value': 'year'},
                                                             {'label': 'quarter', 'value': 'quarter'},
                                                             {'label': 'month', 'value': 'month'},
                                                             {'label': 'week', 'value': 'week'}
                                                             ]),
                                            
                                          dcc.Dropdown(id='sub-cdropdown-1',value='2022',options=[]),
                                          dcc.Dropdown(id='sub-cdropdown-2',value='month',options=[]),
                                         ]),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div(dcc.Graph(id='costs')),
                                    ])
                                    ])

@app.callback(Output('sub-cdropdown-1', 'options'), [Input('cdropdown-1', 'value')])
def sub_dropdown_1(main_dropdown_value):
    options = mn.input_dropdown_column_set(c,main_dropdown_value)
    return options

@app.callback(Output('sub-cdropdown-2', 'options'), [Input('cdropdown-1', 'value')])
def sub_dropdown_2(main_dropdown_value):
    options = mn.input_dropdown_micro(main_dropdown_value)
    return options

@app.callback([Output(component_id='costs', component_property='figure')],
              [Input(component_id='cdropdown-1', component_property='value'),
               Input(component_id='sub-cdropdown-1', component_property='value'),
               Input(component_id='sub-cdropdown-2', component_property='value'),]
               )

def get_graph(main_dropdown_value,sub_dropdown_1,sub_dropdown_2):
    color = 'one'
    bar_mode = 'group'

    cat='type'
    order_c = narc.column_set(c,cat,'cost')

    cc = c[c[main_dropdown_value] == sub_dropdown_1]

    costs = narc.aggregate_category(cc,sub_dropdown_2,cat,'cost',order_c)

    gr = narc.graph_index_columns(costs,colors=color,barmode=bar_mode)

    return [gr]