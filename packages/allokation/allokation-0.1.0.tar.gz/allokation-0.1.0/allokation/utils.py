from datetime import date, timedelta

import pandas as pd
from pandas_datareader import data as web


def get_percentage_of_stocks(tickers, percentages=None):
    if percentages:
        return pd.Series(percentages)/100

    return 1/(len(tickers))


def get_target_date(base_date=date.today()):
    weekdays = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]

    target_date = base_date
    weekday = weekdays[target_date.weekday()]
    if weekday == 'saturday':
        target_date = target_date - timedelta(days=1)
    elif weekday == 'sunday':
        target_date = target_date - timedelta(days=2)

    return target_date


def get_closing_price_from_yahoo(tickers, date):
    result = web.get_data_yahoo(tickers, date)
    return result['Adj Close']


def transpose_prices(prices):
    df = pd.DataFrame()
    df['symbol'] = prices.columns
    df['price'] = prices.values[0]
    df = df.round(2)
    return df


def calculate_amount(df, available_money, percentage_multiplier):
    return (available_money * percentage_multiplier / df['price']).round(0)


def calculate_total_for_each_ticker(df):
    return df['price']*df['amount']


def calculate_percentage_of_each_ticker(df):
    return df['total']/df['total'].sum() * 100
