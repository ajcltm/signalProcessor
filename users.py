from typing import Protocol

class User(Protocol):

    def strategy(self):
        ...

class I:
    def __init__(self, ticker):
        self.ticker = ticker

    def strategy(self, sender, **kwargs):
        idx = kwargs['idx']
        date = kwargs['date']
        print(idx, date, self.ticker)