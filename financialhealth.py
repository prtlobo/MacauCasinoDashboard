import pandas as pd
import plotly.graph_objects as go
import requests
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import datetime
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.io as pio

from app import app
from API import dashboard_data

profit_margin = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    profit_margin.add_trace(go.Scatter(x = df['year'], y =df['netProfitMargin'],
                    mode = 'lines+markers',
                    line_shape= 'spline',
                    name=n))
profit_margin.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
debt_equity=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    debt_equity.add_trace(go.Scatter(x = df['year'], y =df['debtEquityRatio'],
                    mode = 'lines+markers',
                    line_shape= 'spline',
                    name=n))
debt_equity.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

radioitems = dbc.FormGroup(
    [
        dbc.Label('Please choose a graph:'),
        dbc.RadioItems(
            options=[
                {"label": "Profit Margin", "value": 1},
                {"label": "Debt to equity", "value": 2}
            ],
            value=1,
            id="radioitems-input",
            inline=True
        ),
    ]
)
@app.callback(
    Output('outputfigure', 'figure'),
    [
        Input("radioitems-input", "value")
    ],
)
def change_figure(radio_items_value):
    if radio_items_value==1:
        figure=profit_margin
    elif radio_items_value ==2:
        figure=debt_equity
    return figure

financialhealthlayout = html.Div([
    
    dbc.Row([
        dbc.Col(html.H3('Profit Margin Or Debt to Equity'),width='auto'),
        dbc.Col(html.Div(radioitems), width = 'auto')
        ],justify='between'),
    dbc.Row(dbc.Col(dcc.Graph(id='outputfigure')))
])

""" profit_margin = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    profit_margin.add_trace(go.Scatter(x = df['year'], y =df['netProfitMargin'],
                    mode = 'lines+markers',
                    line_shape= 'spline',
                    name=n))
profit_margin.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
debt_equity=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    debt_equity.add_trace(go.Scatter(x = df['year'], y =df['debtEquityRatio'],
                    mode = 'lines+markers',
                    line_shape= 'spline',
                    name=n))
debt_equity.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
) """



""" financialhealthlayout = html.Div(children=[
    
    html.Div([
        html.H3(children='Profit Margin'),
        html.Div(id='health1'),
        
        dcc.Graph(id='profitmargin',figure=profit_margin)
    ]),

    html.Div([
        html.H3('Debt to Equity Ratio'),
        html.Div(id='health2'),
        
        dcc.Graph(id='debt_equity', figure=debt_equity)
    ])
]) """

#financialhealthlayout = 


#   Financial health:
#       Profit Margin
#       Assets to liabilities
#       Cash Flow
# 6 financial health:
#   6.1 financial position short term & long term assest vs liabilites bar chart
#   6.2 Debt to equity history (debt vs equity line chart)
#   6.3 balance sheet marimekko charts