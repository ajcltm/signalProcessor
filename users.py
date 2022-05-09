import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker
import secretary


from abc import ABC, abstractclassmethod
from datetime import datetime

class IUser(ABC):

    @abstractclassmethod
    def strategy(self):
        ...


class User(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)

    def __init__(self, dataProvider)->None:
        self.dataProvider = dataProvider
        self.banker.create_account()

    def strategy(self, sender:str, **kwargs)->None:
        date = kwargs['date']
        if date == datetime(2005, 3, 31) or date == datetime(2022, 4, 6):
            self.banker.register(date=date, amounts=50000)
        if date == datetime(2005, 4, 1) or date == datetime(2022, 4, 7):
            idx = self.dataProvider.get_idx(date)
            data = self.dataProvider.db[idx]
            self.broker.order(date=date, ticker='NVDA', price=data[date]['NVDA']['open'], quantity=10)
            self.broker.order(date=date, ticker='AMZN', price=data[date]['AMZN']['open'], quantity=10)
    
    def set_secretary(self):
        self.secretary = secretary.Secratary(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)