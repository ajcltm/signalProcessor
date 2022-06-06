import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker
import accountant
import advisor
import secretary


from abc import ABC, abstractclassmethod
from dataclasses import make_dataclass, field
from datetime import datetime



class IUser(ABC):

    @abstractclassmethod
    def strategy(self):
        ...


class User(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)

    def __init__(self, dataProvider, limit=None)->None:
        self.dataProvider = dataProvider
        self.banker.create_account(limit)

    def strategy(self, sender:str, **kwargs)->None:
        date = kwargs['date']
        if date == datetime(2005,4, 1) or date == datetime(2022, 4, 6):
            self.banker.register(date=date, amounts=50000)
        if date == datetime(2005, 4, 1) or date == datetime(2022, 4, 7):
            # tickerLst = ['QLD', 'NVDA', 'AMZN', 'ARVL']
            tickerLst = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL', 'A', 'AIG', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE']
            for i in tickerLst:
                try:
                    self.broker.order(date=date, ticker=i, price=self.dataProvider.db.at[(i, date), 'open'], quantity=10)
                except:
                    print(f'{i} problem...')
    
    def set_Accountant(self):
        self.secretary = accountant.Accountant(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)


class SmallInvester(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)
    recorder = make_dataclass('recorder', [
        ('date', datetime, field(default=None)), 
        ('oldMonth', datetime, field(default=None)),
        ('oldSmalls', datetime, field(default=None))
        ])


    def __init__(self, dataProvider, limit=None)->None:
        self.dataProvider = dataProvider
        self.banker.create_account(limit)
        self.accountant = accountant.Accountant(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)
        self.advisor = advisor.FAdvisor()
        self.secretary = secretary.Secretary(self.banker, self.broker, self.accountant, self.advisor, self.dataProvider, self.recorder)

    def strategy(self, sender:str, **kwargs)->None:
        self.recorder.date = kwargs['date']
        if self.recorder.date.month == 5 and self.recorder.oldMonth != 5 :
            strategy = self.advisor.get_advisor(selector='SmallSelector', allocator='OneUnitAllocator', dataProvider=self.dataProvider)
            smalls = strategy.selector.select(self.recorder.date)
            ticker_weight = strategy.allocator.allocate(smalls, self.recorder.date)
            needMoney = 0
            self.secretary.prepareOrder().get_old_orders()
            # if needToSell:
            #     for ticker in needToSell:
            #         price = self.dataProvider.priceData.query.get_price_at_tickerAndDate(ticker, self.recorder.date, 'close')
            #         needMoney -= price
            #         self.broker.order(self.recorder.date, ticker, price, -1)

            # for ticker in neetToBuy:
            #     price = self.dataProvider.priceData.query.get_price_at_tickerAndDate(ticker, self.recorder.date, 'close')
            #     needMoney += price
            #     self.broker.order(self.recorder.date, ticker, price, 1)

            # if not needMoney == 0:
            #     self.banker.register(date=self.recorder.date, amounts=needMoney)
            # self.recorder.oldSmalls = smalls
        self.recorder.oldMonth = self.recorder.date.month