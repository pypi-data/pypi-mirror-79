from allokation.utils import (calculate_amount,
                              calculate_percentage_of_each_ticker,
                              calculate_total_for_each_ticker,
                              get_closing_price_from_yahoo,
                              get_percentage_of_stocks, get_target_date,
                              transpose_prices)


def allocate_money(available_money, tickers, percentages=None):
    if percentages and len(tickers) != len(percentages):
        raise Exception('Tickers and percentages must have the same lenght')

    percentage_multiplier = get_percentage_of_stocks(tickers=tickers, percentages=percentages)

    target_date = get_target_date()
    prices = get_closing_price_from_yahoo(tickers=tickers, date=target_date)
    df = transpose_prices(prices)

    df['amount'] = calculate_amount(df, available_money, percentage_multiplier)

    df['total'] = calculate_total_for_each_ticker(df)
    df['percentage'] = calculate_percentage_of_each_ticker(df)

    result = {}
    result['allocations'] = df.set_index('symbol').T.to_dict()
    result['total_value'] = df["total"].sum().round(2)

    return result
