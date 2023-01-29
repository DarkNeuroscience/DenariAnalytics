import os
import pandas as pd
from MoneyAfterDark import NarcoAnalytics as narc, Montana as mn, TaxTools as tax
from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

from sales import sales_layout
from costs import costs_layout

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
                'costs':html.H3(costs_layout),
                'tax':html.H3('Tax')}
    
    return html.Div([selected[tab]])

if __name__ == '__main__':
    app.run_server(debug=True)