import pandas as pd
from .account import BankAccount, BrokerageAccount
from .interface import CsvInterface
from .ticker import get_prev_close, get_price_history
from typing import List
from datetime import date, timedelta

# Process bank data


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
                 end_date=date.today()):
    spending = pd.concat(
        (acct.get_spending(start_date=start_date, end_date=end_date)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('spending')
    income = pd.concat(
        (acct.get_income(start_date=start_date, end_date=end_date)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('income')
    cashflow = pd.concat(
        (acct.get_cashflow(start_date=start_date, end_date=end_date)
         for acct in bank_accounts), axis=1
    ).sum(axis=1).rename('cashflow')

    # plotly dash doesn't support PeriodIndex type - convert it to datetime
    bk_sum_res = pd.concat((spending, income, cashflow), axis=1)
    bk_sum_res.index = bk_sum_res.index.strftime("%Y-%m")
    bk_sum_res = bk_sum_res.reset_index()
    return bk_sum_res


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


def format(df, formatters):
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
        return format(
            cost,
            formatters={
                'cost': '{:.2f}'.format,
                'prev_close': '{:.2f}'.format,
                'average_price': '{:.2f}'.format,
                'value': '{:.2f}'.format,
                'PnL': '{:.2f}'.format,
                'return': '{:.2%}'.format,
            }).rename(
                columns = {
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
