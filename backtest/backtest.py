import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def cumulative_return(f_invest, i_invest):
    """

    :param f_invest: final value of investment
    :param i_invest: initial investment
    :return: Cumulative returns
    """
    c_return = (f_invest - i_invest) / i_invest
    return c_return


def annualised_returns(cumulative_returns, length):
    annual_return = (1+cumulative_returns**(365/length)) - 1
    return annual_return


def annualised_volatility(cumulative_std, length):
    ann_vol = cumulative_std * np.sqrt(length)
    return ann_vol


def sharpe_ratio(prof_return, prof_std, risk_free_rate=.015):
    return (prof_return - risk_free_rate) / prof_std


def max_draw_down(returns):
    return (min(returns)-max(returns))/max(returns)


def backtest_returns(returns, orders, i_invest=5000):
    """

    :param returns: PD sieries return from each trade
    :param orders: PD siries buy and sell orders
    :param i_invest: initial investment
    :return:
    """
    strategy_returns = returns * orders
    cumulative_returns = (strategy_returns + 1).cumprod()
    cumulative_returns.plot(figsize=(10, 7))
    plt.title('Cumulative Strategy Returns')
    plt.show()

    f_invest_returns = i_invest * cumulative_returns
    f_invest = f_invest_returns[3]
    cumulative_return_p = cumulative_return(i_invest, f_invest)
    print('cumulative_return:', cumulative_return_p)
    print('cumulative_return_std:', cumulative_returns.std())

    f_invest_returns.plot(figsize=(10, 7))
    plt.title('Cash amount')
    plt.show()
    print(cumulative_return_p)
    annual_result = annualised_returns(cumulative_return_p, len(cumulative_returns))
    print(annual_result)

    ann_vol = annualised_volatility(np.std(cumulative_returns), len(cumulative_returns))
    print(ann_vol)

    print(sharpe_ratio(annual_result, np.std(cumulative_returns)))

    print(max_draw_down(strategy_returns),'%')




