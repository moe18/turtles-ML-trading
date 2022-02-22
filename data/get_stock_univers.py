import pandas as pd


def get_s_and_p_stocks():
    df = pd.read_csv('/Users/mordechaichabot/Projects/investment_framework/data/raw_data/s_and_p_data')

    return df
