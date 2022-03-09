import pandas as pd
from yahooquery import Ticker
from sklearn.model_selection import train_test_split


from data.get_stock_univers import get_s_and_p_stocks
from data.sampeling import vol_sampling, dollar_bar


def get_sma_std(data, look_back):
    sma_n = data.close.rolling(window=look_back).std()
    return sma_n


def get_sma_mean(data, look_back):
    sma_n = data.close.rolling(window=look_back).mean()
    return sma_n


if __name__ == '__main__':
    universe = get_s_and_p_stocks()['Symbol']
    n = 10  # chunk row size
    list_df = [universe[i:i+n] for i in range(0, universe.shape[0], n)]

    stocks = Ticker(list_df[0])
    stock_hist = stocks.history(period='1mo', interval='5m')

    all_X_train = []
    all_X_test = []

    all_y_train = []
    all_y_test = []
    for df in list_df:

        stocks = Ticker(df)
        stock_hist = stocks.history(period='1mo', interval='5m')
        try:

            for stock_name in stock_hist.index.get_level_values(0).drop_duplicates(keep='first'):
                try:
                    dollar_bar_data = dollar_bar(stock_hist.loc[stock_name])
                    dollar_bar_data.drop(['timestamp'], axis=1, inplace=True)

                    dollar_bar_data = dollar_bar_data.pct_change()
                    dollar_bar_data['sma_1_mean'] = get_sma_mean(dollar_bar_data, 2)
                    dollar_bar_data['sma_1_std'] = get_sma_std(dollar_bar_data, 2)
                    dollar_bar_data['sma_5_mean'] = get_sma_mean(dollar_bar_data, 5)
                    dollar_bar_data['sma_5_std'] = get_sma_std(dollar_bar_data, 5)
                    dollar_bar_data['sma_10_mean'] = get_sma_mean(dollar_bar_data, 10)
                    dollar_bar_data['sma_10_std'] = get_sma_std(dollar_bar_data, 10)
                    dollar_bar_data['close'] = dollar_bar_data['close'].shift(-1)
                    dollar_bar_data.dropna(inplace=True)
                    X = dollar_bar_data.drop(['close', 'vwap', 'txn'], axis=1)
                    y = dollar_bar_data['close']

                    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2, shuffle=False)

                    all_X_train.append(X_train)
                    all_X_test.append(X_test)
                    all_y_test.append(y_test)
                    all_y_train.append(y_train)
                except ZeroDivisionError:
                    print(stock_name)
                    pass
        except:
            pass

    # TODO: add dates to save file
    pd.concat(all_X_train).to_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/X_train.parquet')
    pd.concat(all_X_test).to_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/X_test.parquet')
    pd.DataFrame(pd.concat(all_y_test)).to_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/y_test.parquet')
    pd.DataFrame(pd.concat(all_y_train)).to_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/y_train.parquet')


        ## TODO: find the point that you buy stratagy to do with prob
        # Kelly criterion
        # risk management
        # back test
        # paper trade




