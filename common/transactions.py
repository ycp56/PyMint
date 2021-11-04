from dataclasses import dataclass
from typing import Optional


@dataclass
class BankTransaction:
    date: str
    merchant: str
    amount: float
    balance: float

    def __post_init__(self):
        try:
            self.amount = float(self.amount.replace(',', ''))
            self.balance = float(self.balance.replace(',', ''))
        except ValueError:
            raise ValueError("Unexpected Format")
    
    def to_dict(self):
        return {
            "date": self.date,
            "merchant": self.merchant,
            "amount": self.amount,
            "balance": self.balance,
        }


@dataclass
class CardTransaction:
    date: str
    merchant: str
    category: str
    type: str
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
            "category": self.category,
            "type": self.type,
            "amount": self.amount,
        }


@dataclass
class BrokerageTransaction:
    date: str
    symbol: str
    quantity: str
    cost: float

    def __post_init__(self):
        try:
            self.cost = float(self.cost.replace(',', '').replace('$',''))
        except ValueError:
            raise ValueError("Unexpected Format")

    def to_dict(self):
        return {
            "date": self.date,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "cost": self.cost,
        }