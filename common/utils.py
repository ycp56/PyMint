import pandas as pd
from .account import BankAccount, BrokerageAccount
from .interface import CsvInterface
from typing import List
from datetime import date, timedelta

# Process bank data


def get_bank_account(config):
    csv_interface = CsvInterface(
        config['file_dir'], config['file_pattern'], config['column_map'], config['datetime_format'], config['filename_date_regex'])
    account = BankAccount(interface=csv_interface,
                          institution=config['institution'])
    account.fetch()
    return account


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

    return pd.concat((spending, income, cashflow), axis=1)


def get_brokerage_account(config):
    csv_interface = CsvInterface(
        config['file_dir'], config['file_pattern'], config['column_map'], config['datetime_format'], config['filename_date_regex'])
    account = BrokerageAccount(interface=csv_interface,
                               institution=config['institution'])
    account.fetch()
    return account
