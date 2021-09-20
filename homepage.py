import pandas as pd
import plotly.graph_objects as go
import dash
#import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
#import datetime
#from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.io as pio


from app import app
from API import dashboard_data

""" def cumilative(df):
    df['Daily Returns'] = df['close'].pct_change()
    df['Daily Cum. Return %'] = ((1 + df['Daily Returns']).cumprod()) * 100
    return df
def sort_df(df,column):
    df=df.reindex(index=df.groupby(level=0)[column].tail(1) \
                        .sort_values(ascending=False) \
                        .index \
                        .get_level_values(0),
                level=0)
    return df
#dashboard_data = API_call()

dashboard_data['stock']=dashboard_data['stock'].groupby(level=0, axis =0).apply(cumilative)

stock=go.Figure()
for n, df in dashboard_data['stock'].groupby(level=0):
    stock.add_trace(go.Scatter(x=df['date'], y=df['close'],
    mode='lines',
    name=n,
    ))
stock.update_layout(
    template='plotly_dark',
    hovermode = 'x',
    showlegend=True,
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation='h'),
    modebar=dict(orientation='v',
                 bgcolor='rgba(0,0,0,0)'
                 ),
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
for n, df in dashboard_data['stock'].groupby(level=0):
    cumilative.add_trace(go.Scatter(x=df['date'], y=df['Daily Cum. Return %'],
                    mode='lines',
                    showlegend = True,
                    name=n,
                    ))

cumilative.update_layout(
    template='plotly_dark',
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

homelayout = html.Div([

    html.Div([
        html.H3(children='Stock Price'),
        html.Div(id='homepage1'),
        
        dcc.Graph(id='stock',figure=stock,animate=True)
    ]),

    html.Div([
        html.H3('Daily Cumilative Returns since IPO'),
        html.Div(id='homepage2'),
        
        dcc.Graph(id='cumilative', figure=cumilative,animate=True)
    ])
])

 """

overviewlayout = html.Div([html.H3('Placeholder')


 ])