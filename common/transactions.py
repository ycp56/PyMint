from dataclasses import dataclass
from typing import Optional


@dataclass
class BankTransaction:
    date: str
    merchant: str
    amount: float

    def __post_init__(self):
        try:
            self.amount = float(self.amount.replace(',', ''))
        except ValueError:
            raise ValueError("Unexpected Format")
    
    def to_dict(self):
        return {
            "date": self.date,
            "merchant": self.merchant,
            "amount": self.amount,
        }


@dataclass
class BrokerageTransaction:
    date: str
    symbol: str
    cost: float

    def __post_init__(self):
        try:
            self.amount = float(self.amount.replace(',', ''))
        except ValueError:
            raise ValueError("Unexpected Format")

    def to_dict(self):
        return {
            "date": self.date,
            "symbol": self.merchant,
            "cost": self.amount,
        }