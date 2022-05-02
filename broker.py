from abc import ABC, abstractclassmethod

class IBroker(ABC):

    @abstractclassmethod
    def order(self):
        pass

    @abstractclassmethod
    def sell(self):
        pass


class GoodBroker:

    def __init__(self, bank:dict):

        self.bank = bank
        self.assets = {}

    def set_(self, sender, **kwargs):
        self.idx = kwargs['idx']
        self.date = kwargs['date']

    def order(self, ticker:str, price:float, quantity:int):
        if not ticker in self.assets:
            self.assets[ticker] = []
        self.assets[ticker].append({'price':price, 'quantity':quantity})
        self.bank.regiser('broker', price*quantity)


