import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker
import secretary


from abc import ABC, abstractclassmethod
from datetime import datetime

import FinanceDataReader as fdr


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
        if date == datetime(2005,4, 1) or date == datetime(2022, 4, 6):
            self.banker.register(date=date, amounts=50000)
        if date == datetime(2005, 4, 1) or date == datetime(2022, 4, 7):
            # tickerLst = ['QLD', 'NVDA', 'AMZN', 'ARVL']
            tickerLst = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL', 'A', 'AIG', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE']
            for i in tickerLst:
                try:
                    print('here')
                    self.broker.order(date=date, ticker=i, price=self.dataProvider.db.at[(i, date), 'open'], quantity=10)
                except:
                    print(f'{i} problem...')
    
    def set_secretary(self):
        self.secretary = secretary.Secratary(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)