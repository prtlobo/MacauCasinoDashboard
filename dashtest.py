import pandas as pd
import plotly.graph_objects as go
import requests
#!pip install jupyter-dash
#!pip install plotly --upgrade
import plotly
#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import datetime
from plotly.subplots import make_subplots


app = JupyterDash(__name__)

app.title = 'Macau Casinos'
#create stock figure
datastock=go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['close'],
  mode='lines',
  name=ticker)
layoutstock = go.Layout(
    title='AAPL Daily Stock',
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
stock=go.Figure(data=datastock,layout=layoutstock)

#Create Cumilative gain figure
trace1 = go.Scatter(x=AAPL[0]['date'], y=AAPL[0]['Daily Cum. Return %'],
                  mode='lines',
                  showlegend = False,
                  name=ticker)
trace2= go.Scatter(x=[AAPL[0]['date'].iloc[-1]],
                         y=[AAPL[0]['Daily Cum. Return %'].iloc[-1]],
                         text=[AAPL[0]['Daily Cum. Return %'].iloc[-1]],
                         mode='markers+text',
                        showlegend = False,
                        textposition='top right')

layoutcumilative = go.Layout(
    xaxis = dict(showgrid=False),
    yaxis = dict(showgrid=False)
)
cumilative = go.Figure(data=[trace1,trace2],layout=layoutcumilative)

#create ratio figures
ROCE=go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnCapitalEmployed'],
                  mode = 'lines+markers',
                  line_shape= 'spline')
ROE = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnEquity'],
                  mode = 'lines+markers',
                  line_shape = 'spline')
PEG = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsToGrowthRatio'],
                  mode = 'lines+markers',
                  line_shape= 'spline')
P_B = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceToBookRatio'],
                  mode = 'lines+markers',
                  line_shape= 'spline')
P_E = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['priceEarningsRatio'],
                  mode = 'lines+markers',
                  line_shape= 'spline')
ROA = go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['returnOnAssets'],
                  mode = 'lines+markers',
                  line_shape= 'spline')

layout_ratios = go.Layout(
    xaxis_tickmode = 'array',
    xaxis_tickvals = AAPL[1]['year'],
    xaxis_ticktext = AAPL[1]['year'],
    yaxis_showgrid = False)

ROCE_plot = go.Figure(data=ROCE,layout=layout_ratios)
ROE_plot = go.Figure(data=ROE,layout=layout_ratios)
PEG_plot = go.Figure(data=PEG,layout=layout_ratios)
P_B_plot = go.Figure(data=P_B,layout=layout_ratios)
P_E_plot = go.Figure(data=P_E,layout=layout_ratios)
ROA_plot = go.Figure(data=ROA,layout=layout_ratios)

#create cashflow figure
cash_trace1 = go.Bar(name='Operating', x=AAPL[4]['year'], y= AAPL[4]['netCashProvidedByOperatingActivities'])
cash_trace2 = go.Bar(name='Investing', x=AAPL[4]['year'], y=AAPL[4]['netCashUsedForInvestingActivites'])
cash_trace3 = go.Bar(name='Financing', x=AAPL[4]['year'], y=AAPL[4]['netCashUsedProvidedByFinancingActivities'])


cash_flow = go.Figure(data=[cash_trace1,cash_trace2,cash_trace3])

#create Assets to Liabilites figure

A_to_L = make_subplots(specs=[[{"secondary_y": True}]])
A_to_L.add_trace(go.Bar(name='Assets', x=AAPL[3]['year'], y= AAPL[3]['totalAssets']),secondary_y=False)
A_to_L.add_trace(go.Bar(name='Liabilities', x=AAPL[3]['year'], y=AAPL[3]['totalLiabilities']),secondary_y=False)
A_to_L.add_trace(go.Scatter(x = AAPL[1]['year'], y =AAPL[1]['debtEquityRatio'],
                  mode = 'lines+markers',
                  line_shape= 'spline',
                  name='Debt to Equity Ratio'),secondary_y=True)
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

#create price/fair value ratio figure
fair_DCF = go.Figure()
ymax = AAPL[6]['undervalue'].max()*1.05
fair_DCF.add_hline(y=1, line_dash='dash')
fair_DCF.add_hrect(y0=0, y1=1, line_width=0, fillcolor="green", opacity=0.2,annotation_text='UNDERVALUED', annotation_position='top left')
fair_DCF.add_hrect(y0=1, y1=ymax, line_width=0, fillcolor="red", opacity=0.2,annotation_text='OVERVALUED', annotation_position='bottom left')
fair_DCF.add_trace(go.Scatter(x = AAPL[6]['date'], y =AAPL[6]['undervalue'], name ='Price/DCF Ratio'))
fair_DCF.update_yaxes(zeroline=False)
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
    ])
])

#def zoom(layout, xrange):
#    in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#    fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

if __name__ == '__main__':
    app.run_server(debug=True)
