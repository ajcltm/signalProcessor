import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker
import dataProvider

from abc import ABC, abstractclassmethod
from datetime import datetime

class IUser(ABC):

    @abstractclassmethod
    def strategy(self):
        ...


class User(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)
    # secretary = 

    def __init__(self, dataProvider)->None:
        self.dataProvider = dataProvider
        self.banker.create_account()

    def strategy(self, sender:str, **kwargs)->None:
        date = kwargs['date']
        if date == datetime(2022, 3, 31) or date == datetime(2022, 4, 6):
            self.banker.register(date=date, amounts=18000)
        if date == datetime(2022, 4, 1) or date == datetime(2022, 4, 7):
            self.broker.order(date=date, ticker='NVDA', price=100, quantity=10)
            self.broker.order(date=date, ticker='QLD', price=100, quantity=10)
        print('user', date)