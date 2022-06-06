from abc import ABC, abstractclassmethod
import pandas as pd

# price query
class IPriceQuery(ABC):

    def __init__(self, data):
        self.data = data

    @abstractclassmethod
    def get_dateUniverse(self):
        pass

    @abstractclassmethod
    def get_tickerUniverse(self):
        pass

    @abstractclassmethod
    def get_tickerInfo_columnBase(self):
        pass

    @abstractclassmethod
    def get_price_at_tickerAndDate(self, ticker, date):
        pass

    @abstractclassmethod
    def get_info_by_date(self, date):
        pass

class SqlPriceQuery(IPriceQuery):

    def get_by_date(self, date):
        self.data
        pass


class ParquetPriceQuery(IPriceQuery):

    def __init__(self, date):
        super().__init__(date)
        self.unstacked = self.data.reset_index().pivot(index='date', columns='ticker', values='close')

    def get_dateUniverse(self):
        return list(self.data.reset_index().date.drop_duplicates().to_dict().values())

    def get_tickerUniverse(self):
        return self.data.index.get_level_values(1).to_list()

    def get_tickerInfo_columnBase(self, tickers, valueName):
        # df = self.data.reset_index()
        # return df.pivot(index='date', columns='ticker', values=valueName)[tickers]
        return self.unstacked[tickers]

    def get_tickerInfo_columnBase_(self, tickers, valueName):
        df = pd.DataFrame(self.get_dateUniverse(), columns=['date'])
        for i in tickers:
            if not i == 'date':
                idx = pd.IndexSlice
                df = pd.merge(left=df, right=self.data.loc[idx[i, :], valueName], on='date', how='left')
                df = df.fillna(0)
        df = df.set_index('date')
        df.columns = tickers
        return df

    def get_price_at_tickerAndDate(self, ticker, date, valueName='close'):
        try:
            return self.data.at[(ticker, date), valueName]
        except:
            return 0
    
    def get_info_by_date(self, date, valueName):
        idx = pd.IndexSlice
        return self.data.loc[idx[:, date], [valueName]]

class FPriceQuery:

    def get_query(self, kind:str)->IPriceQuery:

        dic_ = {'mysql': SqlPriceQuery, 'parquet':ParquetPriceQuery}

        return dic_.get(kind)


# n of shares query

class INOfSharesQuery(ABC):

    def __init__(self, data):
        self.data = data

    def get_by_date(date):
        ...

class SqlNOfSharesQuery(INOfSharesQuery):

    def get_by_date(self, date):
        self.data
        pass


class ParquetNOfSharesQuery(INOfSharesQuery):

    def get_info_by_date(self, date, valueName):
        idx = pd.IndexSlice
        return self.data.loc[idx[:, date], [valueName]]


class FNOfSharesQuery:

    def get_query(self, kind:str)->INOfSharesQuery:

        dic_ = {'mysql': SqlNOfSharesQuery, 'parquet':ParquetNOfSharesQuery}

        return dic_.get(kind)