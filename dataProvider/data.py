import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from Isql import connect, execute
from utility import time
from typing import Protocol
from datetime import datetime
import pandas as pd

import pandas_datareader.data as pdr
import yfinance as yf

class IData(Protocol):

    def get_data(self):
        ...

# price data

class SqlPriceData:

    def get_data(self):
        ...

class YahooOHLCV:

    def __init__(self, ticker:list, start:datetime, end:datetime)->None:
        self.tickerLst = ticker  # ['^KS11', '005930.KS']
        self.start = start
        self.end = end

    def get_data(self) -> pd.DataFrame:
        yf.pdr_override()
        dfs = []
        for ticker in self.tickerLst:
            df = pdr.get_data_yahoo(ticker, data_source='yahoo', start=self.start, end=self.end)
            df = df.assign(Ticker=ticker)
            dfs.append(df)
        __df = pd.concat(dfs)
        __df = __df.reset_index()
        __df = __df.sort_values(by='Date')
        __df.columns = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume', 'ticker']
        __df = __df.set_index(['ticker', 'date'])
        return __df


class KrxKospiOHLCV:

    def __init__(self, save_parquet:bool=False)->None:
        self.save_parquet = save_parquet

    def get_data(self) -> pd.DataFrame:

        if self.save_parquet:
            self.sqlToParquet()

        return pd.read_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData.parquet'))


    def sqlToParquet(self) -> None:
        
        db = connect.get_connector(kind='mysql', var='krxData')
        sql = "select DATE, ISU_SRT_CD, ISU_ABBRV, TDD_OPNPRC, TDD_HGPRC, TDD_LWPRC, TDD_CLSPRC, ACC_TRDVAL from dailydata where MKT_NM = 'KOSPI'"
        ex = execute.Excuter(db)
        ex.execute(sql)
        df = pd.DataFrame(ex.c.fetchall(), columns=['date', 'ticker', 'name','open', 'close', 'high', 'low', 'volume'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index(['ticker', 'date'])
        df.to_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData.parquet'))

# if need to conbine parquet data

class FParquetData:

    lst = []

    def register(self, dataProvider):
        self.lst.append(dataProvider.get_data())

    def get_data(self):
        df = pd.concat(self.lst, axis=0)
        df = df.sort_values(by='date')
        return df


# n of shares data

class SqlNOfSharesData:

    def get_db(self):
        ...

class KrxKospiNOShare:

    def __init__(self, save_parquet:bool=False)->None:
        self.save_parquet = save_parquet

    def get_data(self) -> None:

        if self.save_parquet:
            self.sqlToParquet()

        return pd.read_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_nshrs.parquet'))

    def sqlToParquet(self) -> None:
        db = connect.get_connector(kind='mysql', var='krxData')
        sql = "select DATE, ISU_SRT_CD, LIST_SHRS from dailyData where MKT_NM = 'KOSPI'"
        ex = execute.Excuter(db)
        ex.execute(sql)
        df = pd.DataFrame(ex.c.fetchall(), columns=['date', 'ticker', 'n_of_shares'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index(['ticker', 'date'])
        df.to_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_nshrs.parquet'))


if __name__ == '__main__':
    
    df = KrxKospiOHLCV(save_parquet=False).get_data()
    print(df.head())