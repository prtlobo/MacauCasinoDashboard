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

stock=go.Figure()
stock.add_trace(go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['close'],
  mode='lines',
  name=ticker))
stock.update_layout(
    hovermode = 'x',
    showlegend=True,
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=0, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
)
stock.update_xaxes(
                showgrid =False,
                ticks = 'outside',
                ticklen = 10
    )
stock.update_yaxes(
                showgrid =False
    )
cumilative=go.Figure()
cumilative.add_trace(go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['Daily Cum. Return %'],
                  mode='lines',
                  showlegend = True,
                  name=ticker))

cumilative.update_layout(
    hovermode = 'x',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
cumilative.update_xaxes(
                showgrid =False,
                ticks = 'outside',
                ticklen = 10
    )
cumilative.update_yaxes(
                showgrid =False
    )
homelayout = html.Div(children=[
    html.Div([
        html.H3(children='Stock Price'),
        html.Div(id='result1'),
        
        dcc.Graph(id='graph1',figure=stock)
    ]),

    html.Div([
        html.H3('Daily Cumilative Returns since IPO'),
        html.Div(id='result2'),
        
        dcc.Graph(id='graph2', figure=cumilative)
    ])
])