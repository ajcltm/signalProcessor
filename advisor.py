from typing import Protocol
from matplotlib import ticker
import pandas as pd

class ISelector(Protocol):

    def select(self, dataProvider):
        ...


class SmallSelector:

    def __init__(self, dataProvider):
        self.dataProvider = dataProvider

    def select(self, date):
        priceData = self.dataProvider.priceData.query.get_info_by_date(date, 'open')
        nOShares = self.dataProvider.nOfSharesData.query.get_info_by_date(date, 'n_of_shares')
        result = pd.merge(left=priceData, right=nOShares, left_index=True, right_index=True)
        result['totalValue'] = result['open'] * result['n_of_shares']
        result = result.sort_values(by='totalValue')
        result = result.reset_index()
        result = result.loc[result.loc[:,'open']>0]
        return result.ticker.to_list()[-50:]


class FSelector:

    def __init__(self):
        self.selector_options = {'SmallSelector':SmallSelector}

    def get_selector(self, selector_name:str)->ISelector:
        return self.selector_options.get(selector_name)


class IAllocator(Protocol):

    def allocate(self, dataProvider):
        ...


class OneUnitAllocator:

    def __init__(self, dataProvider):
        self.datsaProvider = dataProvider

    def allocate(self, buy_tickers, date):
        n_of_tickers = len(buy_tickers)
        dict_ = dict(ticker=buy_tickers, weight=[1/n_of_tickers for i in range(n_of_tickers)])
        return pd.DataFrame(dict_)


class FAllocator:

    def __init__(self):
        self.allocator_options = {'OneUnitAllocator':OneUnitAllocator}

    def get_allocator(self, allocator_name:str):
        return self.allocator_options.get(allocator_name)



class IAdvisor:

    def __init__(self, selector:ISelector, allocator:IAllocator, dataProvider):
        ...

    def get_tickersNWeight(self):
        ...


class Advisor:

    def __init__(self, selector:ISelector, allocator:IAllocator, dataProvider):
        self.selector = selector(dataProvider)
        self.allocator = allocator(dataProvider)


class FAdvisor:

    def get_advisor(self, selector:str, allocator:str, dataProvider)->IAdvisor:
        selector = FSelector().get_selector(selector)
        allocator = FAllocator().get_allocator(allocator)
        return Advisor(selector, allocator, dataProvider)