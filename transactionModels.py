from dataclasses import dataclass
from datetime import datetime

@dataclass
class cash_transaction:
    date: datetime
    offer: str
    amounts: int

@dataclass
class assets_transaction:
    date: datetime
    ticker: str
    price: float
    quantity: int