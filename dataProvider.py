from abc import ABC, abstractclassmethod
from pandas_datareader import get_data_famafrench

import pandas_datareader.data as pdr
import yfinance as yf
from datetime import datetime
import pandas as pd


class DataProvider(ABC):

    @abstractclassmethod
    def set_db(self):
        pass

    # @abstractclassmethod
    # def get_idx(self):
    #     pass



class YahooProvider(DataProvider):

    def __init__(self, ticker:list, start:datetime, end:datetime)->None:
        self.tickerLst = ticker  # ['^KS11', '005930.KS']
        self.start = start
        self.end = end
        self.db = self.set_db()
        self.date_universe = [list(i.keys())[0] for i in self.db]

    def set_db(self):
        __df = self.get_df()
        df_dict = __df.to_dict(orient='records')

        row_dict = {df_dict[0].get('Date'):{}}
        db = []
        old_date = df_dict[0].get('Date')
        for row in df_dict:
            date = row.get('Date')
            ticker = row.get('Ticker')
            if not date == old_date:
                db.append(row_dict)
                row_dict = {}
                row_dict[date] = {}
                old_date = date
            row_dict[date][ticker] = {
                'open':row.get('Open'), 'high':row.get('High'), 'low':row.get('Low'), 'close': row.get('Close'),
                'adjClose':row.get('Adj Close'), 'volume':row.get('Volume')}
        return db    

    def get_df(self):
        yf.pdr_override()
        dfs = []
        for ticker in self.tickerLst:
            df = pdr.get_data_yahoo(ticker, data_source='yahoo', start=self.start, end=self.end)
            df = df.assign(Ticker=ticker)
            dfs.append(df)
        __df = pd.concat(dfs)
        __df = __df.reset_index()
        __df = __df.sort_values(by='Date')
        return __df

    def get_idx(self, date:datetime):
        try :
            idx = self.date_universe.index(date)
        except:
            idx = None
        return idx


if __name__ == '__main__':
    s = datetime(2015,4,1)
    e = datetime(2022,4,8)
    tickerLst = ['QLD', 'NVDA', 'AMZN', 'ARVL']
    yp = YahooProvider(ticker=tickerLst, start=s, end=e)
    db = yp.db
    # print(db)

    print(db[-1])
    idx = yp.get_idx(datetime(2022,4,6))
    print(db[idx])