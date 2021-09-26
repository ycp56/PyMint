import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .transactions import BankTransaction, BrokerageTransaction
from .interface import CsvInterface


class BaseAccount:
    """ individual account for accounts"""

    def __init__(self, interface: CsvInterface, institution: str ) -> None:
        self.interface = interface
        self.institution = institution
        self.transactions = []
        self.positions = []

    def get_balance(self):
        raise NotImplementedError

    def _fetch(self):
        txn_lists = self.interface.parse()
        for txn_per_file in txn_lists:
            for txn in txn_per_file['transactions']:
                yield txn_per_file['file_path'], txn_per_file['file_date'], txn

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            txn.to_dict() for txn in self.transactions
        )

    def get_transactions(self, start_date=datetime(1990, 1, 1), end_date=datetime.today()):
        return [
            txn for txn in self.transactions
            if (txn.date >= start_date) and (txn.date <= end_date)
        ]


class BankAccount(BaseAccount):
    def fetch(self, ignore_error=True):
        for file_name, file_date, txn in self._fetch():
            try:
                self.transactions.append(
                    BankTransaction(
                        txn['date'],
                        txn['merchant'],
                        txn['amount']
                    )
                )
            except:
                if ignore_error:
                    pass
                else:
                    raise ValueError


class BrokerageAccount(BaseAccount):
    def fetch(self, ignore_error=True):
        for file_path, file_date, txn in self._fetch():
            try:
                self.transactions.append(
                    (
                        BrokerageTransaction(
                            txn.get('date', file_date),
                            txn['symbol'],
                            txn['quantity'],
                            txn['cost']
                        )
                    )
                )
            except:
                if ignore_error:
                    pass
                else:
                    raise ValueError
