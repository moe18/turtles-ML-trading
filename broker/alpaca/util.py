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


def alp_buy(stock_name, qty, top_limit, lower_limit, current_price):
    api.submit_order(
        symbol=stock_name,
        side='buy',
        type='market',
        qty=qty,
        time_in_force='day',
        order_class='bracket',
        take_profit=dict(
            limit_price=top_limit,
        ),
        stop_loss=dict(
            stop_price=lower_limit,
            limit_price=lower_limit,
        )
    )


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


