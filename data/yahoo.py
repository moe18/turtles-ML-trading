from yahooquery import Ticker


def get_stock_history_data(stock_name, start=None, end=None, period='ytd', interval='1d'):
    """
    gets stock history for `stock_name`
    :param stock_name: str; name of stock
    :param start: str or datetime format; yyyy-mm-dd
    :param end: str or datetime format; yyyy-mm-dd
    :param period: str; length of time ['1d', '5d', '7d', '60d', '1mo', '3mo', '6mo', '1y',
                                       '2y', '5y', '10y', 'ytd', 'max']
    :param interval: str; time between date points ['1m', '2m', '5m', '15m', '30m', '60m',
                                                   '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    :return: pd.DataFrame columns = open, high, low, close, volume, dividend
    """
    ticker = Ticker(stock_name)
    df = ticker.history(start=start, end=end, period=period, interval=interval)

    return df

