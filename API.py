import pandas as pd
import requests
#API_key = '3c48cfed0ed8536fa3d40f9234fed1fb'
#API_key = 'demo'
#ticker = 'AAPL'

#'q_cash':'/api/v3/cash-flow-statement/{}?period=quarter&apikey={}'
#'q_balance':'/api/v3/balance-sheet-statement/{}?period=quarter&apikey={}',
#'q_income':'/api/v3/income-statement/{}?period=quarter&apikey={}',
#'a_enterprise':'/api/v3/enterprise-values/{}?&apikey={}'

def fmp_call(ticker,API_key):
  site = 'https://financialmodelingprep.com'
  api_functions = {'stock':'/api/v3/historical-price-full/{}?serietype=line&apikey={}',
                'ratios':'/api/v3/ratios/{}?apikey={}',
                'a_income':'/api/v3/income-statement/{}?&apikey={}',
                'a_balance': '/api/v3/balance-sheet-statement/{}?&apikey={}',
                'a_cash':'/api/v3/cash-flow-statement/{}?&apikey={}',
                'dividend':'/api/v3/historical-price-full/stock_dividend/{}?apikey={}',
                'DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}'               
  }
  df_results = []
  for function,link in api_functions.items():
    url = site+(link.format(ticker,API_key))
    response = requests.get(url)
    data = response.json()
    if function == 'stock' or function =='dividend':
      df = pd.json_normalize(data,'historical')
      df.sort_values('date',ascending=True,inplace=True)
      df['date'] =  pd.to_datetime(df['date'])
      df_results.append(df)
    else:
      df = pd.json_normalize(data)
      df.sort_values('date',ascending=True,inplace=True)
      df['date'] =  pd.to_datetime(df['date'])
      df['year'] = df['date'].dt.year
      df_results.append(df)
  df_results[0]['Daily Returns'] = df_results[0]['close'].pct_change()
  df_results[0]['Daily Cum. Return %'] = ((1 + df_results[0]['Daily Returns']).cumprod()) * 100
  df_results[6]['undervalue'] = ((df_results[0]['close'] / df_results[6]['dcf']))
  df_results[5] = df_results[5].merge(df_results[0][['date', 'close']], on='date')
  df_results[5]['divYield'] = df_results[5]['adjDividend']/df_results[5]['close']
  df_results[5]['quarters']=df_results[5]['date'].dt.quarter
  df_results[5]['year']=df_results[5]['date'].dt.year
  df_results[5]['columnText']='Q'+df_results[5]['quarters'].astype(str)+' '+df_results[5]['year'].astype(str)
  return df_results

API_key = 'demo'
ticker = 'AAPL'
AAPL = fmp_call(ticker, API_key)