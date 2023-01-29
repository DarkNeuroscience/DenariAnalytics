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
#costs = pd.read_csv(path + slash + "spending.csv", infer_datetime_format=True)
pack = pd.read_csv(path + slash + "packages.csv", infer_datetime_format=True)
#clients = pd.read_csv(path + slash + "clients.csv", infer_datetime_format=True)
sales = pd.read_csv(path + slash + "calex.csv", infer_datetime_format=True)
x = [pack,sales]
for i in x:
    narc.set_dates(i)
s = narc.split_dates(sales,format='period')


sales_layout = html.Div(children=[html.H1('Sales Analysis',style={'textAlign':'center','color':'#503D36','font-size': 40}),
                                  html.P('Analysis of Revenue by Packages', style={'text-align':'center', 'color':'#503D36'}),
                                  html.Div([dcc.Dropdown(id='dropdown-1', 
                                                         value='year',
                                                         options=[
                                                             {'label': 'year', 'value': 'year'},
                                                             {'label': 'quarter', 'value': 'quarter'},
                                                             {'label': 'month', 'value': 'month'},
                                                             {'label': 'week', 'value': 'week'}
                                                             ]),
                                            
                                          dcc.Dropdown(id='sub-dropdown-1',value='2022',options=[]),
                                          dcc.Dropdown(id='sub-dropdown-2',value='month',options=[]),
                                          dcc.Dropdown(id='bar-type',value='group',options=[{'label': 'group', 'value': 'group'},
                                                                                            {'label': 'stack', 'value': 'stack'}])
                                         ]),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div(dcc.Graph(id='pack-sales')),
                                    html.Div(dcc.Graph(id='pack-tot'))], style={'display': 'flex'}),
                                
                                html.Div([
                                    html.Div(dcc.Graph(id='cash-card')),
                                    html.Div(dcc.Graph(id='pay-tot'))], style={'display': 'flex'})
                               ])
                                

@app.callback(Output('sub-dropdown-1', 'options'), [Input('dropdown-1', 'value')])
def sub_dropdown_1(main_dropdown_value):
    options = mn.input_dropdown_column_set(s,main_dropdown_value)
    return options

@app.callback(Output('sub-dropdown-2', 'options'), [Input('dropdown-1', 'value')])
def sub_dropdown_2(main_dropdown_value):
    options = mn.input_dropdown_micro(main_dropdown_value)
    return options

@app.callback([Output(component_id='pack-sales', component_property='figure'),
               Output(component_id='cash-card', component_property='figure'),
               Output(component_id='pack-tot', component_property='figure'),
               Output(component_id='pay-tot', component_property='figure')],
              [Input(component_id='dropdown-1', component_property='value'),
               Input(component_id='sub-dropdown-1', component_property='value'),
               Input(component_id='sub-dropdown-2', component_property='value'),
               Input(component_id='bar-type', component_property='value')
              ]
             )

def get_graph(main_dropdown_value,sub_dropdown_1,sub_dropdown_2,bar_mode):
    color = 'one'
    dff = s.copy()
    cat = 'package'
    
    order_ls = narc.column_set(dff,cat,'payment')
    order_lspt = narc.column_set(dff,'payment type','payment')
    dff = dff[dff[main_dropdown_value] == sub_dropdown_1]

    pack_sales = narc.aggregate_category(dff,sub_dropdown_2,cat,'payment',order_ls)
    cash_card = narc.aggregate_category(dff,sub_dropdown_2,'payment type','payment',order_lspt)

    mc = narc.metric_columns(pack_sales,'sum')
    pack_total = narc.graph_metrics(mc)
    ccmc = narc.metric_columns(cash_card,'sum')

    ps_fig = narc.graph_index_columns(pack_sales,colors=color,barmode=bar_mode)
    cc_fig = narc.graph_index_columns(cash_card,colors=color,barmode=bar_mode)
    pt_fig = narc.graph_metrics(mc)
    pay_tot = narc.graph_metrics(ccmc)
    
    return [ps_fig,cc_fig,pt_fig,pay_tot]