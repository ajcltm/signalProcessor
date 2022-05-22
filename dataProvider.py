import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from Isql import connect, execute
import dataclasses
from typing import Protocol
import pandas_datareader.data as pdr
import yfinance as yf
from datetime import datetime
import pandas as pd
import time


class IDataProvider(Protocol):

    def get_data(self):
        pass


class FDataProvider:

    load_space = dict()

    def register(self, data:IDataProvider, dataTitle:str)->None:
        if not dataTitle in self.load_space:
            self.load_space[dataTitle] = []
        self.load_space[dataTitle].append(data.db)
    
    def get_data(self)->dataclasses:
        dataProviderClass = dataclasses.make_dataclass('DataProvider', ['date_universe'])
        prepare = dict()
        for dataTitle in self.load_space.keys():
            prepare[dataTitle] = pd.concat(self.load_space[dataTitle], axis=0)
        date_universe = list(prepare['priceData'].reset_index().date.drop_duplicates().to_dict().values())
        _dataProviderClass = dataclasses.make_dataclass(cls_name = '_DataProvider', fields = list(prepare.keys()), bases=(dataProviderClass,))
        return _dataProviderClass(**dict({'date_universe':date_universe}, **prepare))


class YahooOHLCV:

    def __init__(self, ticker:list, start:datetime, end:datetime)->None:
        self.tickerLst = ticker  # ['^KS11', '005930.KS']
        self.start = start
        self.end = end
        self.db = self.get_data()

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


class KrxOHLCV:

    def __init__(self, sqlToParquet:bool=False)->None:
        self.db = self.get_data(sqlToParquet=sqlToParquet)

    def get_data(self, sqlToParquet) -> pd.DataFrame:

        if sqlToParquet:
            self.sqlToParquet()

        return pd.read_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_20220518.parquet'))


    def sqlToParquet(self) -> None:
        
        db = connect.get_connector(kind='mysql', var='krxData')
        sql = 'select DATE, ISU_SRT_CD, ISU_ABBRV, TDD_OPNPRC, TDD_HGPRC, TDD_LWPRC, TDD_CLSPRC, ACC_TRDVAL from dailyData'
        ex = execute.Excuter(db)
        ex.execute(sql)
        df = pd.DataFrame(ex.c.fetchall(), columns=['date', 'ticker', 'name','open', 'close', 'high', 'low', 'volume'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index(['ticker', 'date'])
        df.to_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_20220518.parquet'))


class krxNOShare:

    def __init__(self, sqlToParquet:bool=False)->None:
        self.db = self.get_data(sqlToParquet=sqlToParquet)

    def get_data(self, sqlToParquet) -> None:

        if sqlToParquet:
            self.sqlToParquet()

        return pd.read_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_nshrs_20220518.parquet'))

    def sqlToParquet(self) -> None:
        db = connect.get_connector(kind='mysql', var='krxData')
        sql = 'select DATE, ISU_SRT_CD, LIST_SHRS from dailyData'
        ex = execute.Excuter(db)
        ex.execute(sql)
        df = pd.DataFrame(ex.c.fetchall(), columns=['date', 'ticker', 'n_of_shares'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index(['ticker', 'date'])
        df.to_parquet(Path.cwd().joinpath('signalProcessor', 'db', 'krxData_nshrs_20220518.parquet'))


if __name__ == '__main__':
    import pandas as pd
    from pathlib import Path
    stime = time.time()
    kohlcv = KrxOHLCV(sqlToParquet=False)
    s = datetime(2022,5,2)
    e = datetime(2022,5,12)
    yohlcv = YahooOHLCV(['NVDA'],s,e)
    knos = krxNOShare(sqlToParquet=False)
    fdp = FDataProvider()
    fdp.register(data=kohlcv, dataTitle='priceData')
    fdp.register(data=yohlcv, dataTitle='priceData')
    fdp.register(data=knos, dataTitle='nSharesData')
    dataPrivider = fdp.get_data()
    print(dataPrivider.date_universe[-5:])
    print(dataPrivider.priceData.tail())
    print(dataPrivider.nSharesData.tail())
    etime = time.time()
    print(f'{etime-stime:0.2f}seconds')