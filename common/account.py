from dataclasses import dataclass
from typing import Optional

from transactions import BankTransaction, BrokerageTransaction


@dataclass
class BaseAccount:
    """ individual account for accounts"""
    integration: int
    accountId: Optional[str]
    institution: Optional[str]
    accountType: str


class BankAccount(BaseAccount):
    currentBalance: float
    availableBalance: float
    transactions: Optional[BankTransaction]


class BrokerageAccount(BaseAccount):
    currentBalance: float
    availableBalance: float
    transactions: Optional[BrokerageTransaction]
