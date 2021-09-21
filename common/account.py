import sqlite3
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

    def _init_db(self, db_file) -> None:
        raise NotImplementedError

    def _save(self, db_file) -> None:
        raise NotImplementedError


class BankAccount(BaseAccount):
    def fetch(self):
        for txn in self._fetch():
            self.transactions.append(
                BankTransaction(
                    txn['date'],
                    txn['merchant'],
                    txn['amount']
                )
            )

    def _init_db(self, db_file) -> None:
        with sqlite3.connect(db_file) as con:
            cur = con.cursor()
            cur.execute(f""" CREATE TABLE IF NOT EXISTS {self.institution}(
                date TEXT,
                merchant TEXT,
                amount REAL);
            """)
            con.commit()

    def _save(self, db_file) -> None:
        with sqlite3.connect(db_file) as con:
            cur = con.cursor()
            for txn in self.transactions:
                cur.execute(f"""
                INSERT INTO {self.institution} VALUES(?, ?, ?)
                """,
                            (txn.date, txn.merchant, txn.amount))
            con.commit()


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

    def _init_db(self, db_file) -> None:
        with sqlite3.connect(db_file) as con:
            cur = con.cursor()
            cur.execute(f""" CREATE TABLE IF NOT EXISTS {self.institution}(
                date TEXT,
                merchant TEXT,
                cost REAL);
            """)
            con.commit()

    def _save(self, db_file) -> None:
        with sqlite3.connect(db_file) as con:
            cur = con.cursor()
            for txn in self.transactions:
                cur.execute(f"""
                INSERT INTO {self.institution} VALUES(?, ?, ?)
                """,
                            (txn.date, txn.symbol, txn.cost))
            con.commit()
