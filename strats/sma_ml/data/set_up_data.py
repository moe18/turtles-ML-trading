import pandas as pd
from yahooquery import Ticker


from data.get_stock_univers import get_s_and_p_stocks
from data.sampeling import vol_sampling, dollar_bar


def get_sma_std(data, look_back):
    sma_n = data.close.rolling(window=look_back).std()
    return sma_n


def get_sma_mean(data, look_back):
    sma_n = data.close.rolling(window=look_back).mean()
    return sma_n


universe = get_s_and_p_stocks()['Symbol']
n = 10  # chunk row size
list_df = [universe[i:i+n] for i in range(0, universe.shape[0], n)]

stocks = Ticker(list_df[0])
stock_hist = stocks.history(period='1mo', interval='5m')

for df in list_df:

    stocks = Ticker(df)
    stock_hist = stocks.history(period='1mo', interval='5m')
    for stock in stock_hist.index:
        stock_name = stock[0]
        date = stock[1]
        dollar_bar_data = dollar_bar(stock_hist.loc[stock_name])

        dollar_bar_data.drop(['timestamp'], axis=1, inplace=True)

        dollar_bar_data = dollar_bar_data.pct_change()
        dollar_bar_data['sma_1_mean'] = get_sma_mean(dollar_bar_data, 1)
        dollar_bar_data['sma_1_std'] = get_sma_std(dollar_bar_data, 1)
        dollar_bar_data['sma_5_mean'] = get_sma_mean(dollar_bar_data, 5)
        dollar_bar_data['sma_5_std'] = get_sma_std(dollar_bar_data, 5)
        dollar_bar_data['sma_10_mean'] = get_sma_mean(dollar_bar_data, 10)
        dollar_bar_data['sma_10_std'] = get_sma_std(dollar_bar_data, 10)
        dollar_bar_data['close'] = dollar_bar_data['close'].shift(-1)
        X = dollar_bar_data.drop(['close', 'vwap', 'txn'], axis=1)
        y = dollar_bar_data['close']





