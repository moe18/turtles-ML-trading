from broker.alpaca.util import alp_buy_market, apl_sell
from data.yahoo import get_stock_history_data


class TradeStocks:

    def __init__(self):
        self.cash = 10000
        self.order_type = None
        self.stock_name = None
        self.amount_to_buy = None
        self.amount_to_sell = None
        self.qty = None
        self.transaction_cost = None
        self.stop_limit = None
        self.interval = None
        self.look_back = None
        self.history_start = None
        self.history_end = None


    def get_data(self):
        data  = get_stock_history_data(self.stock_name, start=self.history_start, end=self.history_end,
                               period=self.look_back, interval=self.interval)
        return data


    def get_order_type(self):
        return None


    def get_order_amount(self):
        return None

