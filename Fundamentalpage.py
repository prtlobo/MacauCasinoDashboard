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

from API import AAPL, ticker
from app import app
fundamentals= make_subplots(
    rows=6, cols=1,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4", 'plot 5','plot 6'),
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
fundamentals.update_yaxes(showgrid = False)
""" ROCE=go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnCapitalEmployed'],
                  name = 'ROCE',
                  mode = 'lines+markers',
                  line_shape= 'spline')
ROE = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnEquity'],
                  name = 'ROE',
                  mode = 'lines+markers',
                  line_shape = 'spline')
PEG = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsToGrowthRatio'],
                  name = 'PEG',
                  mode = 'lines+markers',
                  line_shape= 'spline')
P_B = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceToBookRatio'],
                  name = 'P/B',
                  mode = 'lines+markers',
                  line_shape= 'spline')
P_E = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsRatio'],
                  name = 'P/E',
                  mode = 'lines+markers',
                  line_shape= 'spline')
ROA = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnAssets'],
                  name = 'ROA',
                  mode = 'lines+markers',
                  line_shape= 'spline') """

""" layout_ratios = go.Layout(
    xaxis_tickmode = 'array',
    xaxis_tickvals = AAPL[1]['year'],
    xaxis_ticktext = AAPL[1]['year'],
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False,
    yaxis_showgrid = False) """

""" ROCE_plot = go.Figure(data=ROCE,layout=layout_ratios)
ROE_plot = go.Figure(data=ROE,layout=layout_ratios)
PEG_plot = go.Figure(data=PEG,layout=layout_ratios)
P_B_plot = go.Figure(data=P_B,layout=layout_ratios)
P_E_plot = go.Figure(data=P_E,layout=layout_ratios)
ROA_plot = go.Figure(data=ROA,layout=layout_ratios) """

""" fundamentallayout = html.Div(children=[
 html.Div([
        html.H3('Return on Capital Employed'),
        html.Div(id='result3'),
        
        dcc.Graph(id='graph3', figure=ROCE_plot)
    ]),

    html.Div([
        html.H3('Return on Equity'),
        html.Div(id='result4'),
        
        dcc.Graph(id='graph4', figure=ROE_plot)
    ]),

    html.Div([
        html.H3('Price to Earning Growth Ratio'),
        html.Div(id='result5'),
        
        dcc.Graph(id='graph5', figure=PEG_plot)
    ]),

    html.Div([
        html.H3('Price to Book Ratio'),
        html.Div(id='result6'),
        
        dcc.Graph(id='graph6', figure=P_B_plot)
    ]),
    html.Div([
        html.H3('Price to Earnings Ratio'),
        html.Div(id='result7'),
        
        dcc.Graph(id='graph7', figure=P_E_plot)
    ])

]) """
fundamentallayout = html.Div(children=[
 html.Div([
        html.H3('Fundamental Ratios'),
        html.Div(id='result3'),
        
        dcc.Graph(id='graph3', figure=fundamentals)
    ])
]) 