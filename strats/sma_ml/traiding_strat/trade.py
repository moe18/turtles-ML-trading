# given
## prob: stock will go up
## outcome: how much of stock to buy (percent of prof)
## what to do if more then one signal is one
## how often to check to trade
## when to sell
    # stop if goes down
    # stop if goes up
    # stop if signal goes away
##

from joblib import dump, load
from yahooquery import Ticker
from strats.sma_ml.models.pred import make_prediction
import numpy as np
from broker.alpaca.util import *
import time
import alpaca_trade_api
import pandas as pd


def kelly_bet(p, loss, gain):
    q = 1-p
    return ((p/loss)-(q/gain))/25


def amount_of_shares(dollar_amount, stock_price):
    shares_to_buy = int(dollar_amount / stock_price)
    if shares_to_buy < 1:
        shares_to_buy = 1
    print(shares_to_buy)
    return shares_to_buy


def trade(model, stock_name, stock):
    stock_hist = stock.history(period='3d', interval='5m')
    current_price = stock_hist['close'].iloc[-1]

    proba = make_prediction(stock_name_trade, model, stock_hist)[0]
    sell_gain = .009
    stop_loss = -.009
    sell_gain_price = current_price * (1+sell_gain)
    stop_loss_price =current_price * (1+stop_loss)
    prob_sell_point = .55
    current_cash = get_current_cash()
    print('current_cash', current_cash)
    buy_thresh = .6

    invest_amount = current_cash * kelly_bet(proba, np.abs(stop_loss), sell_gain)

    if proba >= buy_thresh:
        print('BUY')
        print(proba)
        try:
            shares_owened = amount_of_shares(invest_amount, current_price)
            alp_buy(stock_name,
                    shares_owened,
                    sell_gain_price, stop_loss_price, current_price)
            time.sleep(300)
            hold = True
            while hold:
                stock_hist = stock.history(period='3d', interval='5m')
                current_price = stock_hist['close'].iloc[-1]
                proba = make_prediction(stock_name_trade, model, stock_hist)[0]
                if proba < .55:
                    hold = False
                else:
                    time.sleep(60)
            apl_sell(stock_name, shares_owened)
        except alpaca_trade_api.rest.APIError as e:
            print(e)
            pass
    elif proba <= prob_sell_point:
        print('sell',apl_get_current_holdings(stock_name))
        try:
            apl_sell(stock_name, apl_get_current_holdings(stock_name))
            print('SELL')

        except alpaca_trade_api.rest.APIError as e:
            print(e)
            pass


#pd.read_csv('/Users/mordechaichabot/Projects/investment_framework/data/raw_data/s_and_p_data')['Symbol'][:100]
model = load(
    '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/models/trained_models/rnd_f_model.joblib')

clean_limit_buys()
stock_names = pd.read_csv('/Users/mordechaichabot/Projects/investment_framework/data/raw_data/s_and_p_data')['Symbol'][:100]

while True:
        for stock_name_trade in stock_names:
            try:
                stock = Ticker(stock_name_trade)
                stock_hist = stock.history(period='3d', interval='5m')
                print(stock_hist)
                current_price = stock_hist['close'].iloc[-1]

                trade(model, stock_name_trade, stock)

            except Exception as e:
                pass
                print('error;', e)
        clean_limit_buys()
