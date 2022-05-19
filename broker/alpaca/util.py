from broker.alpaca._config import APCA_API_BASE_URL, APCA_KEY, APCA_SECRET_KEY

import alpaca_trade_api as tradeapi
import time
import alpaca_trade_api

api = tradeapi.REST(
    APCA_KEY,
    APCA_SECRET_KEY,
    APCA_API_BASE_URL
)
account = api.get_account()


def get_current_cash():
    return float(account.cash)


def prof_change():

    balance_change = float(account.equity) - float(account.last_equity)

    return balance_change


def alp_buy_market(stock_name, qty):
    api.submit_order(
        symbol=stock_name,
        side='buy',
        type='market',
        qty=qty,
        time_in_force='day'
    )


def alp_buy_limit(stock_name, qty, limit_price):
    api.submit_order(symbol=stock_name,
                     qty=qty,
                     side='buy',
                     time_in_force='gtc',
                     type='limit',
                     limit_price=limit_price)


def alp_buy_upper_lower_limit(stock_name, qty, upper_limit, lower_limit, buy_price):
    api.submit_order(symbol=stock_name,
                     qty=qty,
                     side='buy',
                     time_in_force='gtc',
                     type='limit',
                     limit_price=buy_price,
                     order_class='bracket',
                     stop_loss=dict(stop_price=lower_limit),
                     take_profit=dict(limit_price=upper_limit))


def find_order_id(orders, stock_name):
    for i in orders:
        if i.symbol == stock_name:
            return i.id


def clean_limit_buys():
    for i in api.list_orders():
        if i.side == 'buy':
            api.cancel_order(i.id)


def apl_sell(stock_name, qty):
    try:
        api.cancel_order(find_order_id(api.list_orders(), stock_name))
    except:
        pass
    api.submit_order(
        symbol=stock_name,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day',
    )


def apl_current_positions():
    return api.list_positions()


def apl_get_current_holdings(stock_name):
    return api.get_position(stock_name).qty


def cancel_all_orders():
    api.cancel_all_orders()


