import pandas as pd
from .account import BankAccount, BrokerageAccount
from .interface import CsvInterface
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
