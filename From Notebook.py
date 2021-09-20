# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# * SJM: 0880.HK
# * MGM: 2282.HK
# * GEG: 0027.HK
# * Sands: 1928.HK
# * Wynn: 1128.HK
# * Melco: MLCO NASDAQ
# 
# %% [markdown]
# Overview:
#   Stock graph
#       price
#       Fair value Price
#       MArket Cap
#       52 week low
#       52 week high
#       P/E
#       P/B
#       P/S
#       PEG
#       Dividend yield
#       Revenue
#       EArnings
#       Gross Margin
#       Operating Margin
#       Profit Margin
#       Debt To equity
#       operating Cash flow
#       Beta
#       Next Earnings
#       Ex-dividend
#       next dividend
#   Valuation:
#       Fair Value(DCF)
#       Price to Earnings
#       Price to Book
#       Price to earnings Growth
#   Financial health:
#       Profit Margin
#       Assets to liabilities
#       Cash Flow
# Forcast:
#   Analyst price target
#   buy/sell meter
#   Forcast return on equity
#   forcast return on assets
#   forcast earnings per share
#   revenue forcast
#   Earnings growth forcast
#   Revenue growth forcast
# Earnings:
#   Past earnings growth
#   past revenue growth
#   Earnings and revenue history
#   Return on equity
#   Return on assets
#   REturn on capital Employed
# Dividend:
#   Dividend stability and growth
#   Dividend payout ratio
# Ownership
#   buying vs selling
#   Shareholders


# 1 Executive summary:
#   1.1 starburst chart
# 2 Share Price & news:
#   2.1 stock chart with events
#   2.2 market performance 7D,30D,90D,1Y,3Y 5Y returns vs Segment VS market
#   2.3 news
# 3 Valuation:
#   price to earnings ratio
#   3.1 share price vs fair value
#   3.2 Price to earnings ratio
#   3.3 Price to earning growth ratio
#   3.4 Price to book ratio
# 4 Future growth:
#   forcasted annual earnings growth
#   4.1 earnings and revenue growth forcast line chart
#   4.2 analyst future growth forcasts (annual) bar chart
#   4.2 Earnings per share growth forcast line chart
#   4.4 future return on equity
# 5 Past performance:
#   historical annual earnings growth
#   5.1 earnings and revenue history line chart
#   5.2 Past eanings growth analysis (5Y vs 1Y growth)
#   5.3 Return on equity
#   5.4 return on assets
#   5.5 return on capital employed
# 6 financial health:
#   6.1 financial position short term & long term assest vs liabilites bar chart
#   6.2 Debt to equity history (debt vs equity line chart)
#   6.3 balance sheet marimekko charts
# 7 dividend:
#   current dividend yield
#   7.1 dividend yield vs market
#   7.2 stability and growth of payments line chart
#   7.3 Current payout to shareholders
#   7.4 future payout to shareholders
# %%
# Colors
# SJM: rgb(3,117,68)
# MGM: rgb(139,110,74)
# GEG: rgb(253,223,1)
# SANDS: rgb(0,29,104)
# WYNN: rgb(254,0,0)
# %%
#import packages
#from numpy import frompyfunc
import pandas as pd
import plotly.graph_objects as go
import requests
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from datetime import timedelta
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.io as pio
import config
from datetime import timedelta
import yfinance as yf
# %%
# Call API
# Define API GET request
def API_call(ticker, link, key):
    #Format API GET url for desired functions
    url = 'https://financialmodelingprep.com'+(link.format(ticker, key))
    response = requests.get(url)
    data = response.json()

    #If the function returns a nested json, need to normalize on key
    #For FMP, historical stock and dividends are nested
    if len(data) == 2:
        df = pd.json_normalize(data,'historical')
        df.sort_values('date',ascending=True,inplace=True, ignore_index=True)
        df['date'] =  pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
#        df.set_index(keys='date',inplace=True)
    elif len(data) > 2:
        df = pd.json_normalize(data)
        df.sort_values('date',ascending=True,inplace=True, ignore_index=True)
        df['date'] =  pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
#        df.set_index(keys='date',inplace=True)
    elif len(data) < 2:
        df = pd.json_normalize(data)
    else:
        df = pd.DataFrame()
    return df

def cumilative(df):
    df['Daily Returns'] = df['close'].pct_change()
    df['Daily Cum. Return %'] = ((1 + df['Daily Returns']).cumprod()) * 100
    return df

companies = pd.DataFrame(
    {'name':['SJM','MGM','GEG','SANDS','WYNN'],
    'ticker':['0880.HK','2282.HK','0027.HK','1928.HK','1128.HK'],
    'color':['rgb(3,117,68)','rgb(139,110,74)','rgb(253,223,1)',' rgb(0,29,104)','rgb(254,0,0)']
    })

api_functions = {'stock':'/api/v3/historical-price-full/{}?serietype=line&apikey={}',
                'ratios':'/api/v3/ratios/{}?apikey={}',
                'a_income':'/api/v3/income-statement/{}?&apikey={}',
                'a_balance': '/api/v3/balance-sheet-statement/{}?&apikey={}',
                'a_cash':'/api/v3/cash-flow-statement/{}?&apikey={}',
                'dividend':'/api/v3/historical-price-full/stock_dividend/{}?apikey={}',
                'dcf':'/api/v3/discounted-cash-flow/{}?apikey={}',
                'd_DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}',
                'a_DCF':'/api/v3/historical-discounted-cash-flow-statement/{}?&apikey={}',
                'quote':'/api/v3/quote/{}?apikey={}'
}

dashboard_data = {**api_functions}
#for function, link in api_functions.items():
companyresults = {}
for function, link in api_functions.items():
    for c,tick in zip(companies['name'].tolist(),companies['ticker'].tolist()):
        companyresults[c]=API_call(tick,link,config.API_key)
    dashboard_data[function] = pd.concat(companyresults.values(),keys=companyresults.keys())
    dashboard_data[function].index.names=['Company','index']

#dashboard_data['stock']=dashboard_data['stock'].groupby(level=0, axis =0).apply(cumilative)
""" dashboard_data['dividend']['quarters']=dashboard_data['dividend']['date'].dt.quarter
dashboard_data['dividend']['columnText']=('Q'
                                    +dashboard_data['dividend']['quarters'].astype(str)
                                    +' '
                                    +dashboard_data['dividend']['year'].astype(str))
dashboard_data['dividend']= dashboard_data['dividend'].merge(dashboard_data['stock'],
                                                             left_on=['Company','date'], 
                                                            right_on=['Company','date']).set_index(dashboard_data['dividend'].index)
dashboard_data['dividend']['divYield'] = dashboard_data['dividend']['adjDividend']/dashboard_data['dividend']['close']
dashboard_data['a_DCF']['undervalue'] = ((dashboard_data['a_DCF']['price'] / dashboard_data['a_DCF']['dcf'])) """

# %%
dashboard_data['dcf']['undervalue']=((dashboard_data['dcf']['Stock Price'] / dashboard_data['dcf']['dcf']))
dashboard_data['dcf'].reset_index(inplace=True)
dashboard_data['dcf'].sort_values(by='undervalue',ascending=False,inplace=True)
dashboard_data['dcf'].rename(columns={'Company':'name'},inplace=True)
dashboard_data['dcf'].merge(right=companies,on='name')
# %%

#Create Earning and Revenue CAGR

""" def CAGR_revenue(df, year):
  end_val = df['revenue'].iloc[-1]
  start_val = df['revenue'].iloc[-(1+year)]
  start_date = (df['date'].iloc[-(1+year)]).strftime('%d/%m/%Y')
  end_date =  df['date'].iloc[-1].strftime('%d/%m/%Y')
  cagr = ((end_val/start_val)**(1/year))-1
  return (cagr,start_date,end_date)

def CAGR_earning(df, year):
  end_val = df['netIncome'].iloc[-1]
  start_val = df['netIncome'].iloc[-(1+year)]
  start_date = (df['date'].iloc[-(1+year)]).strftime('%d/%m/%Y')
  end_date =  df['date'].iloc[-1].strftime('%d/%m/%Y')
  cagr = ((end_val/start_val)**(1/year))-1
  return (cagr,start_date,end_date)

CAGR_fig= go.Figure()

years = [1,3,5,len(AAPL[2])-1]

for year in years:
  earning = CAGR_earning(AAPL[2],year)
  revenue = CAGR_revenue(AAPL[2],year)
  if year == 1:
    CAGR_fig.add_trace(go.Bar(name='Earnings Growth', x=['{} to {}'.format(earning[1],earning[2])], y = [earning[0]], visible=True))
    CAGR_fig.add_trace(go.Bar(name='Revenue Growth', x=['{} to {}'.format(revenue[1],revenue[2])], y= [revenue[0]], visible=True)) 
  else:
    CAGR_fig.add_trace(go.Bar(name='Earnings Growth', x=['{} to {}'.format(earning[1],earning[2])], y = [earning[0]], visible=False))
    CAGR_fig.add_trace(go.Bar(name='Revenue Growth', x=['{} to {}'.format(revenue[1],revenue[2])], y= [revenue[0]], visible=False))

CAGR_fig.update_layout(yaxis_tickformat='%',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                  updatemenus=[                    
        dict(
            type = 'buttons',
            active=0,
            buttons=list([
                dict(label="1 YEAR",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False, False, False]}]),
                dict(label="3 YEARS",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False, False, False]}]),
                dict(label="5 YEARS",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, False, False]}]),
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False,True, True]}])
            ])
        )
    ]                 
) """




# %%

#fig.add_trace(go.Scatter(x = [AAPL[6]['date'].iloc[0],AAPL[6]['date'].iloc[-1]], y =[1,1] , name ='test' ))
#fig.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['undervalue'].where(AAPL[6]['undervalue'] < 1) , name ='under Value', line_color = 'green',fill='tonexty',fillcolor='rgba(26,150,65,0.1)'))
#fig.add_trace(go.Scatter(x = [AAPL[6]['date'].iloc[0],AAPL[6]['date'].iloc[-1]], y =[1,1] , name ='test2', ))
#fig.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['undervalue'].where(AAPL[6]['undervalue'] > 1) , name ='over Value', line_color = 'red',fill='tonexty',fillcolor='rgba(255, 0, 0, 0.1)'))
#fig.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['undervalue'], name ='Over Value'))
#fig.update_xaxes(zeroline=False)


# %%
#link zoom and pan to another figure
""" app=dash.Dash()

app.layout = html.Div([
                dcc.Graph(id='graph',figure=fig),
                html.Pre(id='relayout-data', style=styles['pre']),
                dcc.Graph(id='graph2', figure=fig)])

# Just to see what values are captured.
@app.callback(Output('relayout-data', 'children'),
              [Input('graph', 'relayoutData')])
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@app.callback(Output('graph2', 'figure'),
             [Input('graph', 'relayoutData')], 
             [State('graph2', 'figure')])
def graph_event(select_data,  fig):
    try:
       fig['layout'] = {'xaxis':{'range':[select_data['xaxis.range[0]'],select_data['xaxis.range[1]']]}}
    except KeyError:
       fig['layout'] = {'xaxis':{'range':[zoomed out value]}}
return fig

app.run_server() """


