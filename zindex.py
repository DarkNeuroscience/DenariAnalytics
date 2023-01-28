import os
import pandas as pd
from MoneyAfterDark import NarcoAnalytics as narc, Montana as mn, TaxTools as tax
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

from zsales import sales_layout

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'font-family': 'garamond'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#75AEFA',
    'color': 'white',
    'padding': '6px',
    'font-family': 'garamond'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-inline", value='sales', children=[
        dcc.Tab(label='Cash Flow', value='cash-flow', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Revenue/Expenditure', value='rev-exp', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Product Sales', value='sales', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Costs', value='costs', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Tax Analysis', value='tax', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline-3')
])

@app.callback(Output('tabs-content-inline-3', 'children'),
              Input('tabs-inline', 'value'))

def render_content(tab):
    
    selected = {'cash_flow':html.H3('Cash Flow'),
                'rev-exp':html.H3('Revenue/Expenditure'),
                'sales':html.Div(sales_layout),
                'costs':html.H3('Costs'),
                'tax':html.H3('Tax')}
    
    return html.Div([selected[tab]])

if __name__ == '__main__':
    app.run_server()