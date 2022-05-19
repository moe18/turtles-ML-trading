
from joblib import dump, load
from yahooquery import Ticker
from strats.sma_ml.models.pred import make_prediction
import numpy as np
from broker.alpaca.util import *
import time
import alpaca_trade_api
import pandas as pd
import asyncio


# Notes: this should be a multy classification peoblem where the model predicts how much the stock will go up but in
# buckets


class SmaBuy:
    def __init__(self):
        self.sell_gain = None
        self.stop_loss = None
        self.stock_universe = None
        self.buy_thresh = .6
        self.sell_thresh = None
        self.model = None
        self.prob_sell_point = .55
        self.CURRENT_CASH = 100000

    @staticmethod
    def kelly_bet(p, loss, gain):
        q = 1 - p
        return ((p / loss) - (q / gain)) / 25

    @staticmethod
    def amount_of_shares(dollar_amount, stock_price):
        shares_to_buy = int(dollar_amount / stock_price)
        if shares_to_buy < 1:
            shares_to_buy = 1
        return shares_to_buy

    def trade(self, model, stock_name, stock):
        stock_hist = stock.history(period='3d', interval='5m')
        current_price = stock_hist['close'].iloc[-1]

        proba = make_prediction(stock_name, model, stock_hist)[0]
        sell_gain = self.sell_gain
        stop_loss = self.stop_loss
        sell_gain_price = current_price * (1 + sell_gain)
        stop_loss_price = current_price * (1 + stop_loss)
        prob_sell_point = self.prob_sell_point
        current_cash = self.CURRENT_CASH
        buy_thresh = self.buy_thresh

        invest_amount = current_cash * self.kelly_bet(proba, np.abs(stop_loss), sell_gain)

        if proba >= buy_thresh:
            try:
                shares_owened = self.amount_of_shares(invest_amount, current_price)
                alp_buy(stock_name,
                        shares_owened,
                        sell_gain_price, stop_loss_price, current_price)
                self.CURRENT_CASH -= invest_amount
                hold = True
                while hold:
                    stock_hist = stock.history(period='3d', interval='5m')
                    proba = make_prediction(stock_name, model, stock_hist)[0]
                    if proba < .55:
                        hold = False
                    else:
                        time.sleep(60)
                apl_sell(stock_name, shares_owened)
            except alpaca_trade_api.rest.APIError as e:
                print(e)
                pass
        elif proba <= prob_sell_point:
            num_sell_shares = apl_get_current_holdings(stock_name)
            print('sell', num_sell_shares)
            try:
                apl_sell(stock_name, num_sell_shares)
                print('SELL')
                share_price = stock_hist['close'].iloc[-1]
                self.CURRENT_CASH += (share_price * num_sell_shares)

            except alpaca_trade_api.rest.APIError as e:
                print(e)
                pass

    @staticmethod
    def kelly_bet(p, loss, gain):
        q = 1-p
        kelly_co = p - (q/(gain/loss))
        if kelly_co < .5:
            return ((p/loss)-(q/gain))
        else:
            return .1

    @staticmethod
    def amount_of_shares(dollar_amount, stock_price):
        shares_to_buy = int(dollar_amount / stock_price)
        if shares_to_buy < 1:
            shares_to_buy = 1
        return shares_to_buy

    def run_trading_bot(self):
        model = load(
            '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/models/trained_models/rnd_f_model.joblib')

        clean_limit_buys()
        stock_names = pd.read_csv('/Users/mordechaichabot/Projects/investment_framework/data/raw_data/s_and_p_data')[
                          'Symbol'][:100]

        while True:
            for stock_name_trade in stock_names:
                try:
                    stock = Ticker(stock_name_trade)
                    stock_hist = stock.history(period='3d', interval='5m')
                    print(stock_hist)
                    current_price = stock_hist['close'].iloc[-1]

                    self.trade(model, stock_name_trade, stock)

                except Exception as e:
                    pass
                    print('error;', e)
            clean_limit_buys()


def main():
    pass
