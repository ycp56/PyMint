import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .transactions import BankTransaction, BrokerageTransaction
from .interface import CsvInterface


class BaseAccount:
    """ individual account for accounts"""

    def __init__(self, interface: CsvInterface, institution: str, database_file: str) -> None:
        self.interface = interface
        self.institution = institution
        self.database = database_file
        self.transactions = []

    def get_balance(self):
        raise NotImplementedError

    def _fetch(self) -> List[dict]:
        txn_lists = self.interface.parse()
        for txn_per_file in txn_lists:
            for txn in txn_per_file['transactions']:
                yield txn

    def _init_db(self) -> None:
        raise NotImplementedError

    def _save(self) -> None:
        raise NotImplementedError

    def _clean(self) -> None:
        with sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute(f""" DROP TABLE IF EXISTS {self.institution}""")
            con.commit()

    def get_transactions(self, start_date=datetime(1990, 1, 1), end_date=datetime.today()):
        with sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute(f""" 
                SELECT *
                FROM {self.institution}
                WHERE (date >= {start_date}) AND (date <= {end_date})
                ORDER BY date
            """)

    def get_income(self, start_date, end_date, frequency='month'):
        raise NotImplementedError

    def get_spending(self, start_date, end_date, frequency='month'):
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

    def _init_db(self) -> None:
        with sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute(f""" CREATE TABLE IF NOT EXISTS {self.institution}(
                date TIMESTAMP,
                merchant TEXT,
                amount REAL);
            """)
            con.commit()

    def _save(self) -> None:
        with sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES) as con:
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

    def _init_db(self) -> None:
        with sqlite3.connect(self.database) as con:
            cur = con.cursor()
            cur.execute(f""" CREATE TABLE IF NOT EXISTS {self.institution}(
                date TEXT,
                merchant TEXT,
                cost REAL);
            """)
            con.commit()

    def _save(self) -> None:
        with sqlite3.connect(self.database) as con:
            cur = con.cursor()
            for txn in self.transactions:
                cur.execute(f"""
                INSERT INTO {self.institution} VALUES(?, ?, ?)
                """,
                            (txn.date, txn.symbol, txn.cost))
            con.commit()
