import pandas as pd
import numpy as np
from scipy.stats import normaltest


def get_bar_stats(agg_trades):
    vwap = agg_trades.apply(lambda x: np.average(x.close, weights=x.volume)).to_frame('vwap')
    ohlc = agg_trades.close.ohlc()
    vol = agg_trades.volume.sum().to_frame('vol')
    txn = agg_trades.volume.size().to_frame('txn')
    return pd.concat([ohlc, vwap, vol, txn], axis=1)


def vol_sampling(data):
    data['cumul_vol'] = data.volume.cumsum()
    trades_per_min = data.volume.sum() / (60 * 7.5 * 25)
    by_vol = data.groupby(data.cumul_vol.div(trades_per_min).round().astype(int))
    data.reset_index(inplace=True)
    vol_bars = pd.concat([by_vol.date.last().to_frame('index'), get_bar_stats(by_vol)], axis=1)
    return vol_bars


def dollar_bar(trades):
    value_per_min = trades.volume.mul(trades.close).sum() / (60 * 7.5)  # min per trading day
    trades['cumul_val'] = trades.volume.mul(trades.close).cumsum()
    df = trades.reset_index()
    by_value = df.groupby(df.cumul_val.div(value_per_min).round().astype(int))
    dollar_bars = pd.concat([by_value.date.last().to_frame('timestamp'), get_bar_stats(by_value)], axis=1)
    print(normaltest(dollar_bars.vwap.dropna()))
    return dollar_bars


