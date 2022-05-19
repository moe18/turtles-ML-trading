from yahooquery import Ticker


def get_stock_history_data(stock_name, start=None, end=None, period=None, interval=None):
    """
    gets stock history for `stock_name`
    :param stock_name:
    :param start:
    :param end:
    :param period:
    :param interval:
    :return:
    """
    ticker = Ticker(stock_name)
    df = ticker.history(stock_name, start=start, end=end, period=period, interval=interval)

    return df

