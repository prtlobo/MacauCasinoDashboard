import pandas as pd
import requests
import config

# Define API GET request
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
                'd_DCF':'/api/v3/historical-daily-discounted-cash-flow/{}?&apikey={}',
                'a_DCF':'/api/v3/historical-discounted-cash-flow-statement/{}?&apikey={}'
}

dashboard_data = {**api_functions}
#for function, link in api_functions.items():
companyresults = {}
for function, link in api_functions.items():
    for c,tick in zip(companies['name'].tolist(),companies['ticker'].tolist()):
        companyresults[c]=API_call(tick,link,config.API_key)
    dashboard_data[function] = pd.concat(companyresults.values(),keys=companyresults.keys())
    dashboard_data[function].index.names=['Company','index']

""" dashboard_data['stock']=dashboard_data['stock'].groupby(level=0, axis =0).apply(cumilative)
dashboard_data['dividend']['quarters']=dashboard_data['dividend']['date'].dt.quarter
dashboard_data['dividend']['columnText']=('Q'
                                    +dashboard_data['dividend']['quarters'].astype(str)
                                    +' '
                                    +dashboard_data['dividend']['year'].astype(str))
dashboard_data['dividend']= dashboard_data['dividend'].merge(dashboard_data['stock'],
                                                             left_on=['Company','date'], 
                                                            right_on=['Company','date']).set_index(dashboard_data['dividend'].index)
dashboard_data['dividend']['divYield'] = dashboard_data['dividend']['adjDividend']/dashboard_data['dividend']['close']
dashboard_data['a_DCF']['undervalue'] = ((dashboard_data['a_DCF']['price'] / dashboard_data['a_DCF']['dcf'])) """