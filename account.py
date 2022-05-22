from typing import Protocol

class IAccount(Protocol):

    def deposit(self):
        ...

    def withdraw(self):
        ...


class Account:

    def __init__(self, limit=None) -> None:
        self.limit = limit
        self.cash = 0
        self.cash_transaction = []

    def deposit(self, amount:int):
        self.cash += amount
    
    def withdraw(self, amount:int):
        if self.limit:
            assert amount - self.cash > self.limit, "You cannot withdraw cash over limit."
        self.cash -= amount