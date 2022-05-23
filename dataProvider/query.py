from abc import ABC, abstractclassmethod
import pandas as pd

# price query
class IPriceQuery(ABC):

    def __init__(self, data):
        self.data = data

    @abstractclassmethod
    def get_by_date(self, date):
        pass


class SqlPriceQuery(IPriceQuery):

    def get_by_date(self, date):
        self.data
        pass


class ParquetPriceQuery(IPriceQuery):

    def get_by_date(self, date):
        idx = pd.IndexSlice
        return self.data.loc[idx[:, date], :]


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

class SqlNOfSharesQuery(IPriceQuery):

    def get_by_date(self, date):
        self.data
        pass


class ParquetNOfSharesQuery(IPriceQuery):

    def get_by_date(self, date):
        idx = pd.IndexSlice
        return self.data.loc[idx[:, date], :]


class FNOfSharesQuery:

    def get_query(self, kind:str)->INOfSharesQuery:

        dic_ = {'mysql': SqlNOfSharesQuery, 'parquet':ParquetNOfSharesQuery}

        return dic_.get(kind)