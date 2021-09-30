import pandas as pd
import numpy as np

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from .transactions import BankTransaction, BrokerageTransaction
from .interface import CsvInterface


class BaseAccount:
    """ individual account for accounts"""

    def __init__(self, interface: CsvInterface, institution: str) -> None:
        self.interface = interface
        self.institution = institution
        self.transactions = []
        self.positions = []
        self._balance_sheet = None

    def _account_type(self) -> str:
        return self.__class__.__name__

    def _fetch(self):
        txn_lists = self.interface.parse()
        for txn_per_file in txn_lists:
            for txn in txn_per_file['transactions']:
                yield txn_per_file['file_path'], txn_per_file['file_date'], txn

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            txn.to_dict() for txn in self.transactions
        )

    def get_transactions(self,
                         start_date=datetime(1990, 1, 1),
                         end_date=datetime.today(),
                         format='pandas' 
                         ) -> List[Union[BankTransaction, BrokerageTransaction]]:
        
        txns =  [
            txn for txn in self.transactions
            if (txn.date >= start_date) and (txn.date <= end_date)
        ]

        if format == 'pandas':
            return pd.DataFrame.from_records(
                txn.to_dict() for txn in txns 
                )
        else:
            return txns


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

    def get_balance(self, type="all", start_date="1990-01-01", end_date="2099-01-01"):
        if self._balance_sheet is None:
            self._balance_sheet = self.to_dataframe()

        if type == 'all':
            balance = self._balance_sheet.query("(date>=@start_date) & (date<=@end_date)")
        elif type == 'income':
            balance = self._balance_sheet.query("(date>=@start_date) & (date<=@end_date) & (amount>0)")
        elif type == 'spending':
            balance = self._balance_sheet.query("(date>=@start_date) & (date<=@end_date) & (amount<0)")
        else:
            raise ValueError('Unknown type!')
        return np.around(balance['amount'].sum(), 2)


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

    def get_balance(self, start_date="1990-01-01", end_date="2099-01-01"):
        if self._balance_sheet is None:
            self._balance_sheet = self.to_dataframe()
        balance = self._balance_sheet.query("(date>=@start_date) & (date<=@end_date)")
        return np.around(balance['cost'].sum(), 2)

