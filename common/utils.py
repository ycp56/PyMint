import pandas as pd
from .account import BankAccount, BrokerageAccount, CardAccount
from .interface import CsvInterface
from .ticker import get_prev_close, get_price_history
from typing import List
from datetime import date, timedelta

# -----------------------------------------------------------------------------
#            Utility functions to process bank data
# -----------------------------------------------------------------------------


def _get_bank_account(config):
    csv_interface = CsvInterface(
        config['file_dir'], config['file_pattern'], config['column_map'], config['datetime_format'], config['filename_date_regex'])
    account = BankAccount(interface=csv_interface,
                          institution=config['institution'])
    account.fetch()
    return account


def get_bank_account(bank_configs):
    return [_get_bank_account(c) for c in bank_configs]


def bank_summary(bank_accounts: List[BankAccount],
                 start_date=date.today()-timedelta(days=364),
                 end_date=date.today(), freq='M'):
    spending = pd.concat(
        (acct.get_spending(start_date=start_date, end_date=end_date, freq=freq)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('spending')
    income = pd.concat(
        (acct.get_income(start_date=start_date, end_date=end_date, freq=freq)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('income')
    cashflow = pd.concat(
        (acct.get_cashflow(start_date=start_date, end_date=end_date, freq=freq)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('cashflow')
    balance = pd.concat(
        (acct.get_balance(start_date=start_date, end_date=end_date, freq=freq)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('balance')

    date_format = {
        'D': "%Y-%m-%d",
        'M': "%Y-%m"
    }
    # plotly dash doesn't support PeriodIndex type - convert it to datetime
    bk_sum_res = pd.concat((spending, income, cashflow, balance), axis=1)
    bk_sum_res.index = bk_sum_res.index.strftime(date_format[freq]).rename('date')
    bk_sum_res = bk_sum_res.reset_index().fillna(0.)
    return bk_sum_res


# -----------------------------------------------------------------------------
#            Utility functions to process card data
# -----------------------------------------------------------------------------
def _get_card_account(config):
    csv_interface = CsvInterface(
        config['file_dir'], config['file_pattern'], config['column_map'], config['datetime_format'], config['filename_date_regex'])
    account = CardAccount(interface=csv_interface,
                          institution=config['institution'])
    account.fetch()
    return account


def get_card_account(card_configs):
    return [_get_card_account(c) for c in card_configs]


def card_summary(card_accounts: List[CardAccount],
                 start_date=date.today()-timedelta(days=364),
                 end_date=date.today(), freq='M'):
    spending = pd.concat(
        (acct.get_spending(start_date=start_date, end_date=end_date, by_category=True)
         for acct in card_accounts), axis=1
        ).sum(axis=1).rename('spending')

    # plotly dash doesn't support PeriodIndex type - convert it to datetime
    return spending 



# -----------------------------------------------------------------------------
#            Utility functions to process brokerage data
# -----------------------------------------------------------------------------

def _get_brokerage_account(config):
    csv_interface = CsvInterface(
        config['file_dir'], config['file_pattern'], config['column_map'], config['datetime_format'], config['filename_date_regex'])
    account = BrokerageAccount(interface=csv_interface,
                               institution=config['institution'])
    account.fetch()
    return account


def get_brokerage_account(brokerage_configs):
    return [_get_brokerage_account(c) for c in brokerage_configs]


def add_prev_close(df_brokerage_summary, cash_symbol=[]):
    all_tickers = [ticker for ticker in df_brokerage_summary['symbol']
                   if ticker not in cash_symbol]
    ticker_data = [get_prev_close(ticker) for ticker in all_tickers]
    ticker_data = [{'symbol': symbol, 'prev_close': prev_close}
                   for symbol, _, prev_close in ticker_data if symbol is not None] + \
        [{'symbol': symbol, 'prev_close': 1.0} for symbol in cash_symbol]

    prev_close = pd.DataFrame.from_records(ticker_data)
    df_brokerage_summary = df_brokerage_summary.merge(
        prev_close, on='symbol', how='left'
    )
    df_brokerage_summary['value'] = df_brokerage_summary['prev_close'] * \
        df_brokerage_summary['quantity']
    df_brokerage_summary['PnL'] = df_brokerage_summary['value'] - \
        df_brokerage_summary['cost']
    df_brokerage_summary['return'] = df_brokerage_summary['PnL'] / \
        df_brokerage_summary['cost']
    return df_brokerage_summary


def _format(df, formatters):
    for col, func in formatters.items():
        if col in df:
            df[col] = df[col].apply(func)
    return df


def brokerage_summary(brokerage_accounts: List[BrokerageAccount],
                      cash_symbol=['QACDS'],
                      enrich=True):
    cost = pd.concat(acct.to_dataframe()[
                     ['symbol', 'quantity', 'cost']
                     ] for acct in brokerage_accounts).astype(
                         {
                             'quantity': 'float'
                         }
    )
    cost = cost.groupby(by='symbol').sum().reset_index()
    cost['average_price'] = cost['cost'] / cost['quantity']
    if enrich:
        cost = add_prev_close(cost, cash_symbol=cash_symbol)
        return _format(
            cost,
            formatters={
                'cost': '{:.2f}'.format,
                'prev_close': '{:.2f}'.format,
                'average_price': '{:.2f}'.format,
                'value': '{:.2f}'.format,
                'PnL': '{:.2f}'.format,
                'return': '{:.2%}'.format,
            }).rename(
                columns={
                    'symbol': 'Symbol',
                    'quantity': "Quantity",
                    'cost': 'Cost',
                    'average_price': 'Average Price',
                    'prev_close': 'Previous Close Price',
                    'value': 'Value',
                    'PnL': 'PnL',
                    'return': 'Return'
                }
        )
    else:
        return cost


def portfolio_trend(brokerage_accounts: List[BrokerageAccount],
                    cash_symbol=['QACDS'],
                    enrich=True):
    portfolio = pd.concat(acct.to_dataframe()[
        ['symbol', 'quantity']
    ] for acct in brokerage_accounts).astype(
        {
            'quantity': 'float'
        }
    )

    portfolio = portfolio.groupby(by='symbol').sum().reset_index()
    price_history = [get_price_history(ticker)
                     for ticker in portfolio['symbol']]
    price_history = pd.concat(
        pd.DataFrame(
            {
                'date': pd.to_datetime(timestamp, unit='s').date,
                'symbol': symbol,
                'price': price
            }
        ) for symbol, timestamp, price in price_history if symbol is not None
    )

    price_history = price_history.merge(portfolio, on='symbol', how='left')
    price_history['value'] = (price_history['price']
                              * price_history['quantity']).round(2)
    return price_history[['date', 'value']].groupby(by='date').sum().reset_index()
