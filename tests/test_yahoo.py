import pytest
import pandas as pd
from datetime import datetime
from data.yahoo import get_stock_history_data


def test_get_stock_history_data():
    data = get_stock_history_data('spy')
    assert len(get_stock_history_data('spy')) > 1
    assert isinstance(data, pd.DataFrame)
    assert datetime.now().year == data.index[1][1].year

    data = get_stock_history_data('spy', start='2021-01-01', end='2021-09-01', interval='1d')
    assert len(get_stock_history_data('spy')) > 1
    assert isinstance(data, pd.DataFrame)
    assert datetime.now().year != data.index[1][1].year
