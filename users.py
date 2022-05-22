import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import banker
import broker
import secretary


from abc import ABC, abstractclassmethod
from datetime import datetime
import pandas as pd
import FinanceDataReader as fdr


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
    
    def set_secretary(self):
        self.secretary = secretary.Secratary(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)


class SmallInvester(IUser):

    banker = banker.Banker()
    broker = broker.GoodBroker(banker)

    def __init__(self, dataProvider, limit=None)->None:
        self.dataProvider = dataProvider
        self.banker.create_account(limit)

        self.oldMonth = None
        self.oldSmalls = None

    def strategy(self, sender:str, **kwargs)->None:
        date = kwargs['date']
        if date.month == 7 and self.oldMonth != 7 :
            smalls = self.get_small_ticker(date)
            needToSell, neetToBuy = self.reBalance(smalls)
            needMoney = 0
            if needToSell:
                for ticker in needToSell:
                    price = self.dataProvider.priceData.at[(ticker, date), 'close']
                    needMoney += price
                    self.broker.order(date, ticker, price, -1)

            for ticker in neetToBuy:
                price = self.dataProvider.priceData.at[(ticker, date), 'close']
                needMoney += price
                self.broker.order(date, ticker, price, 1)

            if not needMoney == 0:
                self.banker.register(date=date, amounts=needMoney)
            self.oldMonth = date.month
            self.oldSmalls = smalls

    def get_small_ticker(self, date):
        idx = pd.IndexSlice
        priceData = self.dataProvider.priceData.loc[idx[:, date], ['open']]
        nOShares = self.dataProvider.nSharesData.loc[idx[:, date], ['n_of_shares']]
        result = pd.merge(left=priceData, right=nOShares, left_index=True, right_index=True)
        result['totalValue'] = result['open'] * result['n_of_shares']
        result = result.sort_values(by='totalValue')
        result = result.reset_index()
        result = result.loc[result.loc[:,'open']>0]
        return result.ticker.to_list()[-50:]

    def reBalance(self, smalls):
        if self.oldSmalls:
            needToSell = [ticker for ticker in self.oldSmalls if not ticker in smalls]
            neetToBuy = [ticker for ticker in smalls if not ticker in self.oldSmalls]
            return needToSell, neetToBuy
        return None, smalls


    def set_secretary(self):
        self.secretary = secretary.Secratary(self.banker.account.cash_transaction, self.broker.assets_transaction, self.dataProvider)
