from typing import Protocol

class IAccount(Protocol):

    def deposit(self):
        ...

    def withdraw(self):
        ...


class Account:

    def __init__(self) -> None:
        self.cash = 0
        self.cash_transaction = []

    def deposit(self, amount:int):
        self.cash += amount
    
    def withdraw(self, amount:int):
        if amount > self.cash:
            raise ValueError("Insufficient funds")
        self.cash -= amount