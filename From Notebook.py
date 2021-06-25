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
#   5.5 return on capitcal employed
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

# %% [markdown]
# To Do:
# 
# * Sector Performance ratios?
# * Loop through all api functions
# * add vertical lines with date and annotation (major news)
# * PEG chart chaange to under vs Over valued
# * DPS = Total Dividends paid/shares outstanding
# OR 
# Earnings per Share X Dividend payout ratio
# *Graham Number: sqrt((22.5)(EPS)(Book Value Per Share))
# OR sqrt((22.5)(EPS)(shareholder's equity/shares outstanding))
# * DCF- Over/under value  By = (Current Price / Fair Value price ) - 1 * 100
# * Add different zoom levels units for dividend figure (tickformatstops)
# * Representative colors for each company for traces
# * Vectorize datafram functions to make it faster
# * input dcc.Loading for loading pages

# %%
#import packages
# pip install pandas
# pip install plotly
# pip install requests
# pip install jupyter-dash
# !pip install plotly --upgrade
# from jupyter_dash import JupyterDash
from numpy import frompyfunc
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
import config

# %%
#API call information
tickers = {'SJM':'0880.HK','MGM':'2282.HK','GEG':'0027.HK','SANDS':'1928.HK','WYNN':'1128.HK'}
site = 'https://financialmodelingprep.com'
api_functions = {'stock':'/api/v3/historical-price-full/{}?serietype=line&apikey={}',
                'ratios':'/api/v3/ratios/{}?apikey={}',
                'a_income':'/api/v3/income-statement/{}?&apikey={}',
                'a_balance': '/api/v3/balance-sheet-statement/{}?&apikey={}',
                'a_cash':'/api/v3/cash-flow-statement/{}?&apikey={}',
                'dividend':'/api/v3/historical-price-full/stock_dividend/{}?apikey={}',
                'd_DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}',
                'a_DCF':'/api/v3/historical-discounted-cash-flow-statement/'
}
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
#        df.set_index(keys='date',inplace=True)
    elif len(data) > 2:
        df = pd.json_normalize(data)
        df.sort_values('date',ascending=True,inplace=True, ignore_index=True)
        df['date'] =  pd.to_datetime(df['date'])
#        df.set_index(keys='date',inplace=True)
    else:
        df = pd.DataFrame()
    return df

companies = pd.DataFrame(
    {'Name':['SJM','MGM','GEG','SANDS','WYNN'],
    'Ticker':['0880.HK','2282.HK','0027.HK','1928.HK','1128.HK'],
    'Color':['red','green','pink','blue','yellow']
    })

api_functions = {'stock':'/api/v3/historical-price-full/{}?serietype=line&apikey={}',
                'ratios':'/api/v3/ratios/{}?apikey={}',
                'a_income':'/api/v3/income-statement/{}?&apikey={}',
                'a_balance': '/api/v3/balance-sheet-statement/{}?&apikey={}',
                'a_cash':'/api/v3/cash-flow-statement/{}?&apikey={}',
                'dividend':'/api/v3/historical-price-full/stock_dividend/{}?apikey={}',
                'd_DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}',
                'a_DCF':'/api/v3/historical-discounted-cash-flow-statement/{}?&apikey={}'
}

dashboard_data = {**api_functions}
#for function, link in api_functions.items():
for function, link in api_functions.items():
    SJM =API_call(companies['Ticker'].loc[0],link,config.API_key)
    MGM = API_call(companies['Ticker'].loc[1],link,config.API_key)
    GEG = API_call(companies['Ticker'].loc[2],link,config.API_key)
    SANDS = API_call(companies['Ticker'].loc[3],link,config.API_key)
    WYNN = API_call(companies['Ticker'].loc[4],link,config.API_key)
    datalist = [SJM, MGM, GEG, SANDS, WYNN]
    dashboard_data[function] = pd.concat(datalist,keys=companies['Name'].tolist())
    dashboard_data[function].index.names=['Company','index']  
# %%
def cumilative(df):
    df['Daily Returns'] = df['close'].pct_change()
    df['Daily Cum. Return %'] = ((1 + df['Daily Returns']).cumprod()) * 100
    return df

dashboard_data['stock']=dashboard_data['stock'].groupby(level=0, axis =0).apply(cumilative)
dashboard_data['ratios']['year']=dashboard_data['ratios']['date'].dt.year
dashboard_data['dividend']['quarters']=dashboard_data['dividend']['date'].dt.quarter
dashboard_data['dividend']['year']=dashboard_data['dividend']['date'].dt.year
dashboard_data['dividend']['columnText']=('Q'
                                    +dashboard_data['dividend']['quarters'].astype(str)
                                    +' '
                                    +dashboard_data['dividend']['year'].astype(str))
dashboard_data['dividend']= dashboard_data['dividend'].merge(dashboard_data['stock'], left_on=['Company','date'], right_on=['Company','date']).set_index(dashboard_data['dividend'].index)
dashboard_data['dividend']['divYield'] = dashboard_data['dividend']['adjDividend']/dashboard_data['dividend']['close']
dashboard_data['a_DCF']['undervalue'] = ((dashboard_data['a_DCF']['price'] / dashboard_data['a_DCF']['dcf']))
#dashboard_data['dividend'] = dashboard_data['dividend'].merge(dashboard_data['stock'], left_index=True, right_on=['Company','date'])
#dashboard_data['dividend']= dashboard_data['dividend'].merge(dashboard_data['stock'], left_on=['Company','date'], right_on=['Company','date']).set_index('index')
#if not dashboard_data['DCF'].empty:
#    dashboard_data['DCF']['undervalue'] = ((dashboard_data['stock']['close'] / dashboard_data['DCF']['dcf']))
# %%
fig = go.Figure()
ymax = dashboard_data['a_DCF']['undervalue'].max()*1.05
fig.add_hline(y=1, line_dash='dash')
fig.add_hrect(y0=0, 
                    y1=1, 
                    line_width=0, 
                    fillcolor="green", 
                    opacity=0.2, 
                    annotation_text='UNDERVALUED', 
                    annotation_position='top left',
                    layer='below')
fig.add_hrect(y0=1, 
                    y1=ymax, 
                    line_width=0, 
                    fillcolor="red", 
                    opacity=0.2,
                    annotation_text='OVERVALUED', 
                    annotation_position='bottom left',
                    layer = 'below')
for n, df in dashboard_data['a_DCF'].groupby(level=0):
    fig.add_trace(go.Scatter(name=n, 
                    x=df['date'], 
                    y= df['undervalue'])
                                       )

fig.update_yaxes(zeroline=False)
fig.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
fig.show()

# %%
#fig= go.Figure()

#sorteddflist= sorted(dflist,key=lambda x:x["age"].max(axis=0))

""" for n, df in dashboard_data['dividend'].groupby(level=0):
    fig.add_trace(go.Bar(name=n, 
                    x=df['columnText'], 
                    y= df['adjDividend'],
                    xperiod='M1',
                    xperiodalignment='middle')
                    
                    ) """
fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])
df = dashboard_data['dividend']['SJM']
fig.add_trace(go.Bar(name='Dividends', 
                    x=df['columnText'], 
                    y= df['adjDividend'],
                    xperiod='M1',
                    xperiodalignment='middle')
                    ,secondary_y=False
                    )

fig.add_trace(go.Scatter(x = df['columnText'], 
                        y =df['divYield'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Dividend Yield', 
                  xperiod='M1',
                  xperiodalignment='middle'),secondary_y=True)
fig.update_layout(
    hovermode='x unified',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(
        title='Diividend per share (DPS)',
        tickprefix='$'
    ),
    yaxis2=dict(
        title='Dividend Yield',
        anchor='y',
        overlaying='y',
        side='right',
        tickformat='.2%'
    )
)
fig.show()

# %%

#xaxis_tickmode = 'array',
#paper_bgcolor = 'rgba(0,0,0,0)',
#plot_bgcolor='rgba(0,0,0,0)',
#yaxis_showgrid = False
#xaxis_tickvals = AAPL[1]['year'],
#xaxis_ticktext = AAPL[1]['year'],
ROCE=go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROCE.add_trace(go.Scatter(x = df['year'], y =df['returnOnCapitalEmployed'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
ROCE.update_layout(xaxis_tickmode = 'array',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')


ROE = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROE.add_trace(go.Scatter(x = df['year'], y =df['returnOnEquity'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape = 'spline'))

PEG = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    PEG.add_trace(go.Scatter(x = df['year'], y =df['priceEarningsToGrowthRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))

P_B = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    P_B.add_trace(go.Scatter(x = ['year'], y =['priceToBookRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
P_E = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    P_E.add_trace(go.Scatter(x = df['year'], y =df['priceEarningsRatio'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))
ROA = go.Figure()
for n, df in dashboard_data['ratios'].groupby(level=0):
    ROA.add_trace(go.Scatter(x = df['year'], y =df['returnOnAssets'],
                    name = n,
                    mode = 'lines+markers',
                    line_shape= 'spline'))

#fig.update_traces()

# %% [markdown]
#AAPL[1] -> dividendYield
#AAPL[1] -> payoutRatio
#AAPL[1] -> dividendPayoutRatio
# %%
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

app.title = 'Macau Casinos'
pio.templates.default = "plotly_dark"


#create stock figure
stock=go.Figure()
stock.add_trace(go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['close'],
  mode='lines',
  name=ticker))
stock.update_layout(
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

#Create Cumilative gain figure
cumilative=go.Figure()
cumilative.add_trace(go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['Daily Cum. Return %'],
                  mode='lines',
                  showlegend = True,
                  name=ticker))

cumilative.update_layout(
    xaxis = dict(showgrid=False),
    yaxis = dict(showgrid=False),
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
cumilative.update_xaxes(
                ticks = 'outside',
                ticklen = 10
    )
#create ratio figures
ROCE=go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnCapitalEmployed'],
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
                  line_shape= 'spline')

layout_ratios = go.Layout(
    xaxis_tickmode = 'array',
    xaxis_tickvals = AAPL[1]['year'],
    xaxis_ticktext = AAPL[1]['year'],
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_showgrid = False)

ROCE_plot = go.Figure(data=ROCE,layout=layout_ratios)
ROE_plot = go.Figure(data=ROE,layout=layout_ratios)
PEG_plot = go.Figure(data=PEG,layout=layout_ratios)
P_B_plot = go.Figure(data=P_B,layout=layout_ratios)
P_E_plot = go.Figure(data=P_E,layout=layout_ratios)
ROA_plot = go.Figure(data=ROA,layout=layout_ratios)

#create cashflow figure
cash_flow = go.Figure()
cash_flow.add_trace(go.Bar(name='Operating', 
                            x=AAPL[4]['year'], 
                            y= AAPL[4]['netCashProvidedByOperatingActivities']))
cash_flow.add_trace(go.Bar(name='Investing', 
                            x=AAPL[4]['year'], 
                            y=AAPL[4]['netCashUsedForInvestingActivites']))
cash_flow.add_trace(go.Bar(name='Financing', 
                            x=AAPL[4]['year'], 
                            y=AAPL[4]['netCashUsedProvidedByFinancingActivities']))
cash_flow.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
#create Assets to Liabilites figure

A_to_L = make_subplots(specs=[[{"secondary_y": True}]])
A_to_L.add_trace(go.Bar(name='Assets', x=AAPL[3]['year'], y= AAPL[3]['totalAssets']),secondary_y=False)
A_to_L.add_trace(go.Bar(name='Liabilities', x=AAPL[3]['year'], y=AAPL[3]['totalLiabilities']),secondary_y=False)
A_to_L.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['debtEquityRatio'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Debt to Equity Ratio'),secondary_y=True)
A_to_L.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
A_to_L.update_yaxes(title_text = 'Assets & Liabilites (USD)', secondary_y=False)
A_to_L.update_yaxes(title_text= ' Debt To Equity Ratio', secondary_y=True)            

#Create Profit Margins figure
profit_margin = make_subplots(specs=[[{"secondary_y": True}]])
profit_margin.add_trace(go.Bar(name='Revenue', x=AAPL[2]['year'], y= AAPL[2]['revenue']),secondary_y=False)
profit_margin.add_trace(go.Bar(name='Net Income', x=AAPL[2]['year'], y=AAPL[2]['netIncome']),secondary_y=False)
profit_margin.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['netProfitMargin'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Net Profit Margin'),secondary_y=True)
profit_margin.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
#Create Earning and Revenue CAGR

def CAGR_revenue(df, year):
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
)
#create Fair value vs Price Figure
DCF = go.Figure()
DCF.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['dcf'], name ='Fair Value',visible=True))
DCF.add_trace(go.Scatter(x = AAPL[0]['date'], y =AAPL[0]['close'], name ='Price', visible=True ))
DCF.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
#create price/fair value ratio figure
fair_DCF = go.Figure()
ymax = AAPL[6]['undervalue'].max()*1.05
fair_DCF.add_hline(y=1, line_dash='dash')
fair_DCF.add_hrect(y0=0, 
                    y1=1, 
                    line_width=0, 
                    fillcolor="green", 
                    opacity=0.2, 
                    annotation_text='UNDERVALUED', 
                    annotation_position='top left',
                    layer='below')
fair_DCF.add_hrect(y0=1, 
                    y1=ymax, 
                    line_width=0, 
                    fillcolor="red", 
                    opacity=0.2,
                    annotation_text='OVERVALUED', 
                    annotation_position='bottom left',
                    layer = 'below')
fair_DCF.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['undervalue'], name ='Price/DCF Ratio'))
fair_DCF.update_yaxes(zeroline=False)
fair_DCF.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
# Create dividend and dividend yield figure
dividend = go.Figure()
dividend = make_subplots(specs=[[{"secondary_y": True}]])

dividend.add_trace(go.Bar(name='Dividends', 
                    x=AAPL[5]['columnText'], 
                    y= AAPL[5]['adjDividend'],
                    xperiod='M1',
                    xperiodalignment='middle')
                    ,secondary_y=False
                    )

dividend.add_trace(go.Scatter(x = AAPL[5]['columnText'], y =AAPL[5]['divYield'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Dividend Yield', 
                  xperiod='M1',
                  xperiodalignment='middle'),secondary_y=True)
dividend.update_layout(
    hovermode='x unified',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(
        title='Diividend per share (DPS)',
        tickprefix='$'
    ),
    yaxis2=dict(
        title='Dividend Yield',
        anchor='y',
        overlaying='y',
        side='right',
        tickformat='.2%'
    )
)

#app layouts
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Macau Casinos'),
        html.H2('Stock Price'),
        html.Div(id='result1'),
        
        dcc.Graph(id='graph1',figure=stock)
    ]),

    html.Div([
        html.H2('Cumilative Returns'),
        html.Div(id='result2'),
        
        dcc.Graph(id='graph2', figure=cumilative)
    ]),

    html.Div([
        html.H2('Return on Capital Employed'),
        html.Div(id='result3'),
        
        dcc.Graph(id='graph3', figure=ROCE_plot)
    ]),

    html.Div([
        html.H2('Return on Equity'),
        html.Div(id='result4'),
        
        dcc.Graph(id='graph4', figure=ROE_plot)
    ]),

    html.Div([
        html.H2('Price to Earning Growth Ratio'),
        html.Div(id='result5'),
        
        dcc.Graph(id='graph5', figure=PEG_plot)
    ]),

    html.Div([
        html.H2('Price to Book Ratio'),
        html.Div(id='result6'),
        
        dcc.Graph(id='graph6', figure=P_B_plot)
    ]),
    html.Div([
        html.H2('Price to Earnings Ratio'),
        html.Div(id='result7'),
        
        dcc.Graph(id='graph7', figure=P_E_plot)
    ]),

    html.Div([
        html.H2('Return on Assets'),
        html.Div(id='result8'),
        
        dcc.Graph(id='graph8', figure=ROA_plot)
    ]),
    html.Div([
        html.H2('Cash Flow'),
        html.Div(id='result9'),
        
        dcc.Graph(id='graph9', figure=cash_flow)
    ]),
    html.Div([
        html.H2('Assets to Liabilities'),
        html.Div(id='result10'),
        
        dcc.Graph(id='graph10', figure=A_to_L)
    ]),
    html.Div([
        html.H2('Profit Margins'),
        html.Div(id='result11'),
        
        dcc.Graph(id='graph11', figure=profit_margin)
    ]),
    html.Div([
        html.H2('Earnings and Revenue Growth'),
        html.Div(id='result12'),
        
        dcc.Graph(id='graph12', figure=CAGR_fig)
    ]),
    html.Div([
        html.H2('Fair Value Vs Price'),
        html.Div(id='result13'),
        
        dcc.Graph(id='graph13', figure=DCF)
    ]),
    html.Div([
        html.H2('Price / DCF Ratio'),
        html.Div(id='result14'),
        
        dcc.Graph(id='graph14', figure=fair_DCF)
    ]),
    html.Div([
        html.H2('Dividend & Dividend Yield'),
        html.Div(id='result15'),
        
        dcc.Graph(id='graph15', figure=dividend)
    ])

])

#def zoom(layout, xrange):
#    in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#    fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

if __name__ == '__main__':
    app.run_server(debug=False)


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


