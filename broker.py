import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import transactionModels as tm

from abc import ABC, abstractclassmethod

class IBroker(ABC):

    @abstractclassmethod
    def order(self):
        pass

    @abstractclassmethod
    def sell(self):
        pass


class GoodBroker:

    def __init__(self, banker):

        self.banker = banker
        self.assets_transaction = []

    def order(self, date, ticker:str, price:float, quantity:int):
        self.assets_transaction.append(tm.assets_transaction(date=date, ticker=ticker, price=price, quantity=quantity))
        self.banker.register(date, name='broker', amounts=price*quantity*(-1))


