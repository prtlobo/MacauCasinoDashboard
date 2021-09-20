import asyncio
from aiohttp import ClientSession
import config
import pandas as pd
from aiolimiter import AsyncLimiter
import time
#company name, company ticker on Hong Kong exchange, and colors extracted from their repective website/documents for representation
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
#FMP has 10 request per second limit.
rate_limit = AsyncLimiter(5, 0.5)

def json_to_df(data):
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
def divide_responses(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
async def fetch(url, session):
    async with rate_limit:
        async with session.get(url) as response:
            data = await response.json()
            dataframe = json_to_df(data)
            return dataframe
def API_call():
    async def main():
        url = 'https://financialmodelingprep.com'
        tasks = []
        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for link in api_functions.values():
                for tick in companies['ticker']:
                    task = asyncio.create_task(fetch(url+(link.format(tick,config.API_key)), session))
                    tasks.append(task)
                responses = await asyncio.gather(*tasks)
                # you now have all response bodies in this variable
            return responses
#        return list_of_responses
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    list_of_responses = loop.run_until_complete(future)
    dashboard_data = {**api_functions}
    for n,function in enumerate(api_functions.keys()):
        comp_list = list(divide_responses(list_of_responses,len(companies['name'])))
        dashboard_data[function]=pd.concat(comp_list[n],keys=companies['name'].tolist())
        dashboard_data[function].index.names=['Company','index']   
    return dashboard_data
dashboard_data=API_call()
