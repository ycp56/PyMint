from dataclasses import dataclass
from typing import List, Optional

from .transactions import BankTransaction, BrokerageTransaction
from .interface import CsvInterface


class BaseAccount:
    """ individual account for accounts"""
    def __init__(self, interface: CsvInterface, institution: str) -> None:
        self.interface = interface
        self.institution = institution
        self.transactions = []

    def get_balance(self):
        raise NotImplementedError

    def _fetch(self) -> List[dict]:
        txn_lists = self.interface.parse()
        for txn_per_file in txn_lists:
            for txn in txn_per_file['transactions']:
                yield txn


class BankAccount(BaseAccount):
    def fetch(self):
        for txn in self._fetch():
            self.transactions.append(
                BankTransaction(
                    txn['date'],
                    txn['amount'],
                    txn['merchant']
                )
            )


class BrokerageAccount(BaseAccount):
    def fetch(self):
        for txn in self._fetch():
            self.transactions.append(
                (
                    txn['date'],
                    txn['symbol'],
                    txn['cost']
                )
            )
