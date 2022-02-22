import pandas as pd
from datetime import datetime
import pandas_datareader.data as web
import pyEX as p
c = p.Client(api_token='YOUR_API_TOKEN', version='stable')


from decouple import config

def get_s_and_p():
    sp_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_constituents = pd.read_html(sp_url, header=0)[0]
    return sp500_constituents

IEX_API_KEY = config("IEX_API_KEY")

start = datetime(2015, 2, 9)
# end = datetime(2017, 5, 24)

iex = web.DataReader('FB', 'iex', start, api_key=IEX_API_KEY)
print(iex.info())