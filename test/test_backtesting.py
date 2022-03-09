import pandas as pd
from backtest.backtest import backtest_returns

backtest_returns(pd.Series([.01, .02, -.03, .01, .1, 1, -.4]), [.55,0.4,.1,.2,2,0,.05])

