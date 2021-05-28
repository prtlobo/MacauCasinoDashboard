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
# To Do:
# 
# *   Sector Performance ratios?
# *   Loop through all api functions
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
# 

# %%
#import packages
# pip install pandas
# pip install plotly
# pip install requests
# pip install jupyter-dash
# !pip install plotly --upgrade
# from jupyter_dash import JupyterDash
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

# %%
#API call information
#API_key = '3c48cfed0ed8536fa3d40f9234fed1fb'
API_key = 'demo'
ticker = 'AAPL'
site = 'https://financialmodelingprep.com'
api_functions = {'stock':'/api/v3/historical-price-full/{}?serietype=line&apikey={}',
                'ratios':'/api/v3/ratios/{}?apikey={}',
                'a_income':'/api/v3/income-statement/{}?&apikey={}',
                'a_balance': '/api/v3/balance-sheet-statement/{}?&apikey={}',
                'a_cash':'/api/v3/cash-flow-statement/{}?&apikey={}',
                'dividend':'/api/v3/historical-price-full/stock_dividend/{}?apikey={}',
                'DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}'               
}

#'q_cash':'/api/v3/cash-flow-statement/{}?period=quarter&apikey={}'
#'q_balance':'/api/v3/balance-sheet-statement/{}?period=quarter&apikey={}',
#'q_income':'/api/v3/income-statement/{}?period=quarter&apikey={}',
#'a_enterprise':'/api/v3/enterprise-values/{}?&apikey={}'


# %%
#call API and store results
AAPL = []
for function,link in api_functions.items():
  url = site+(link.format(ticker,API_key))
  response = requests.get(url)
  data = response.json()
  if function == 'stock' or function =='dividend':
    df = pd.json_normalize(data,'historical')
    df.sort_values('date',ascending=True,inplace=True)
    df['date'] =  pd.to_datetime(df['date'])
#    df['year'] = df['date'].dt.year
    AAPL.append(df)
  else: 
    df = pd.json_normalize(data)
    df.sort_values('date',ascending=True,inplace=True)
    df['date'] =  pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    AAPL.append(df)
AAPL[0]['Daily Returns'] = AAPL[0]['close'].pct_change()
AAPL[0]['Daily Cum. Return %'] = ((1 + AAPL[0]['Daily Returns']).cumprod()) * 100
AAPL[6]['undervalue'] = ((AAPL[0]['close'] / AAPL[6]['dcf']))
AAPL[5] = AAPL[5].merge(AAPL[0][['date', 'close']], on='date')
AAPL[5]['divYield'] = AAPL[5]['adjDividend']/AAPL[5]['close']
AAPL[5]['quarters']=AAPL[5]['date'].dt.quarter
AAPL[5]['year']=AAPL[5]['date'].dt.year
AAPL[5]['columnText']='Q'+AAPL[5]['quarters'].astype(str)+' '+AAPL[5]['year'].astype(str)
# %% [markdown]
#AAPL[1] -> dividendYield
#AAPL[1] -> payoutRatio
#AAPL[1] -> dividendPayoutRatio
# %%
fig= go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(name='Dividends', 
                    x=AAPL[5]['columnText'], 
                    y= AAPL[5]['adjDividend'],
                    xperiod='M1',
                    xperiodalignment='middle')
                    ,secondary_y=False
                    )

fig.add_trace(go.Scatter(x = AAPL[5]['columnText'], y =AAPL[5]['divYield'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Dividend Yield', 
                  xperiod='M1',
                  xperiodalignment='middle'),secondary_y=True)
fig.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    yaxis=dict(
        title='Dividend per share (DPS)',
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
#
#
#fig.update_xaxes(
#    type='category',
#    ticktext=AAPL[5]['columnText'],
#    tickvals=AAPL[5]['date'],
#)

#fig.update_xaxes(type='category',
#                dtick='M1',
#                tickformat='%b\b%Y')
#fig.update_layout(
#    xaxis_tickformatstops = [
#        dict(dtickrange=["M1", "M12"], value="%b \n %Y"),
#        dict(dtickrange=["M12", None], value="%q \n %Y")
#    ]
#)
#fig.update_xaxes(dtick='M1',
#                tickformat='%q\n%Y')
#.dt.strftime('%m-%Y')
#fig.update_layout(yaxis_tickformat='.2%',secondary_y=True)
fig.show()


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


