from abc import ABC, abstractclassmethod

class IUser(ABC):

    @abstractclassmethod
    def strategy(self):
        ...


class User(IUser):

    broker : 
    account : 

class I:
    def __init__(self, ticker):
        self.ticker = ticker

    def strategy(self, sender, **kwargs):
        idx = kwargs['idx']
        date = kwargs['date']
        print(idx, date, self.ticker)