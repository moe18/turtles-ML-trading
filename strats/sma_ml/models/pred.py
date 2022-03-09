from joblib import dump, load
from yahooquery import Ticker
import numpy as np
from data.sampeling import vol_sampling, dollar_bar


#TODO: add to util later
def get_sma_std(data, look_back):
    sma_n = data.close.rolling(window=look_back).std()
    return sma_n


def get_sma_mean(data, look_back):
    sma_n = data.close.rolling(window=look_back).mean()
    return sma_n


def make_prediction(stock_name, model, stock_hist):
    try:
        dollar_bar_data = dollar_bar(stock_hist.loc[stock_name])
    except:
        dollar_bar_data = dollar_bar(stock_hist)

    print(dollar_bar_data)
    dollar_bar_data.drop(['timestamp'], axis=1, inplace=True)

    dollar_bar_data = dollar_bar_data.pct_change()
    dollar_bar_data['sma_1_mean'] = get_sma_mean(dollar_bar_data, 2)
    dollar_bar_data['sma_1_std'] = get_sma_std(dollar_bar_data, 2)
    dollar_bar_data['sma_5_mean'] = get_sma_mean(dollar_bar_data, 5)
    dollar_bar_data['sma_5_std'] = get_sma_std(dollar_bar_data, 5)
    dollar_bar_data['sma_10_mean'] = get_sma_mean(dollar_bar_data, 10)
    dollar_bar_data['sma_10_std'] = get_sma_std(dollar_bar_data, 10)
    dollar_bar_data['close'] = dollar_bar_data['close'].shift(-1)
    dollar_bar_data = dollar_bar_data.drop(['close', 'vwap', 'txn'], axis=1)
    return model.predict_proba(np.array(dollar_bar_data.iloc[-1]).reshape(1, -1))[:, 1:][0]

