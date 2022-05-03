import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker

from abc import ABC, abstractclassmethod

class IUser(ABC):

    @abstractclassmethod
    def strategy(self):
        ...


class User(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)

    def __init__(self, ticker):
        self.banker.create_account()
        self.ticker = ticker

    def strategy(self, sender, **kwargs):
        idx = kwargs['idx']
        date = kwargs['date']
        if idx == 0:
            self.banker.register(date=date, amounts=18000)
        self.broker.order(date=date, ticker='NVDA', price=100, quantity=10)
        print('user', idx, date, self.ticker)