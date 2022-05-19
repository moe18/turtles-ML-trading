from broker.alpaca.util import alp_buy_market, apl_sell


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

    def buy_stock(self):
        alp_buy_market(self.stock_name, self.qty)

    def sell_stock(self):
        apl_sell(self.stock_name, self.amount_to_sell)