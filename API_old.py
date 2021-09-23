import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
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
    if len(data) == 1:
        df = pd.json_normalize(data)
    elif len(data) == 2:
            df = pd.json_normalize(data,'historical')
            df.sort_values('date',ascending=True,inplace=True, ignore_index=True)
            df['date'] =  pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
    elif len(data) > 2:
        df = pd.json_normalize(data)
        df.sort_values('date',ascending=True,inplace=True, ignore_index=True)
        df['date'] =  pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
    else:
        df = pd.DataFrame()
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
                'a_DCF':'/api/v3/historical-discounted-cash-flow-statement/{}?&apikey={}',
                'quote':'/api/v3/quote/{}?apikey={}'
}

dashboard_data = {**api_functions}
#for function, link in api_functions.items():
companyresults = {}
for function, link in api_functions.items():
    for c,tick in zip(companies['name'].tolist(),companies['ticker'].tolist()):
        companyresults[c]=API_call(tick,link,SECRET_KEY)
    dashboard_data[function] = pd.concat(companyresults.values(),keys=companyresults.keys())
    dashboard_data[function].index.names=['Company','index']
