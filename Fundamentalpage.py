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

""" fundamentals= make_subplots(
    rows=6, cols=1,
    subplot_titles=('Return on Capital Employed',
                     'Return On Equity',
                     'Price/Earnings To Growth', 
                     'Price/Book', 'Price/Earnings','Return on Assets'),
    shared_xaxes=True)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnCapitalEmployed'],
                  name = 'ROCE',
                  mode = 'lines+markers',
                  line_shape= 'spline'),row=1,col=1)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnEquity'],
                  name = 'ROE',
                  mode = 'lines+markers',
                  line_shape = 'spline'),row=2,col=1)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsToGrowthRatio'],
                  name = 'PEG',
                  mode = 'lines+markers',
                  line_shape= 'spline'),row=3,col=1)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceToBookRatio'],
                  name = 'P/B',
                  mode = 'lines+markers',
                  line_shape= 'spline'),row=4,col=1)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsRatio'],
                  name = 'P/E',
                  mode = 'lines+markers',
                  line_shape= 'spline'),row=5,col=1)
fundamentals.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnAssets'],
                  name = 'ROA',
                  mode = 'lines+markers',
                  line_shape= 'spline'),row=6,col=1)

fundamentals.update_layout(
    modebar_orientation = 'v',
    modebar_bgcolor = 'rgba(0,0,0,0)',
    height = 2100,
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    )

fundamentals.update_xaxes(tickmode = 'array',tickvals = AAPL[1]['year'],
    ticktext = AAPL[1]['year'], gridcolor='#a0a0a0', showticklabels=True)
fundamentals.update_yaxes(showgrid = False) """

ROCE=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROCE.add_trace(go.Scatter(x = df['year'], y =df['returnOnCapitalEmployed'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
ROCE.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)
ROE=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROE.add_trace(go.Scatter(x = df['year'], y =df['returnOnEquity'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape = 'spline'))
ROE.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)
PEG=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    PEG.add_trace(go.Scatter(x = df['year'], y =df['priceEarningsToGrowthRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
PEG.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)
P_B=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    P_B.add_trace(go.Scatter(x = df['year'], y =df['priceToBookRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
P_B.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)
P_E=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    P_E.add_trace(go.Scatter(x = df['year'], y =df['priceEarningsRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
P_E.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)
ROA=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROA.add_trace(go.Scatter(x = df['year'], y =df['returnOnAssets'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
ROA.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)

fundamentallayout = html.Div(children=[
 html.Div([
        html.H3('Return on Capital Employed'),
        html.Div(id='fundamentalpage1'),
        
        dcc.Graph(id='ROCE', figure=ROCE)
    ]),

    html.Div([
        html.H3('Return on Equity'),
        html.Div(id='fundamentalpage2'),
        
        dcc.Graph(id='ROE', figure=ROE)
    ]),

    html.Div([
        html.H3('Price to Earning Growth Ratio'),
        html.Div(id='fundamentalpage3'),
        
        dcc.Graph(id='PEG', figure=PEG)
    ]),

    html.Div([
        html.H3('Price to Book Ratio'),
        html.Div(id='fundamentalpage4'),
        
        dcc.Graph(id='P_B', figure=P_B)
    ]),
    html.Div([
        html.H3('Price to Earnings Ratio'),
        html.Div(id='fundamentalpage5'),
        
        dcc.Graph(id='P_E', figure=P_E)
    ])

])

""" fundamentallayout = html.Div(children=[
 html.Div([
        html.H3('Fundamental Ratios'),
        html.Div(id='result3'),
        
        dcc.Graph(id='graph3', figure=fundamentals)
    ])
])  """