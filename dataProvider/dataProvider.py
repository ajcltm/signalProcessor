from dataProvider import data, query
import dataclasses
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from utility import time

class FDataProvider:

    def __init__(self, data:data.IData, query:query.IPriceQuery):
        self.data = data.get_data()
        self.query = query(self.data)


class FDataProviders:

    set_dict = dict()

    def register(self, dataProvider, name):
        self.set_dict[name] = dataProvider

    def get_dataProviders(self):
        dc = dataclasses.make_dataclass('dataProvider', list(self.set_dict.keys()))
        return dc(**self.set_dict)


# application
class AKrxKospiDataProviders:

    @time.timeMeasure
    def get_dataProviders(self):
        fdps = FDataProviders()

        # price dataProvider

        # krx kospi price data
        k = data.KrxKospiOHLCV()
        priceDataProvider = FDataProvider(data = k, query=query.FPriceQuery().get_query('parquet'))
        
        # n of shares dataProvider
        nOfSharesDataProvider = FDataProvider(data = data.KrxKospiNOShare(), query=query.FNOfSharesQuery().get_query('parquet'))
        fdps.register(priceDataProvider, 'priceData')
        fdps.register(nOfSharesDataProvider, 'nOfSharesData')

        return fdps.get_dataProviders()

class SParquetKrxKospiYahooCombineDataProviders:

    def __init__(self, ticker:list, start:datetime, end:datetime):
        self.tickerLst = ticker  # ['^KS11', '005930.KS']
        self.start = start
        self.end = end

    def get_dataProviders(self):
        fdps = FDataProviders()

        # price dataProvider

        # yahoo price data
        y = data.YahooOHLCV(self.ticker, self.start, self.end)
        # krx kospi price data
        k = data.KrxKospiOHLCV()

        # combine data
        fpd = data.FParquetData()
        fpd.register(y)
        fpd.register(k)

        priceDataProvider = FDataProvider(data = fpd, query=query.FPriceQuery().get_query('parquet'))

        # n of shares dataProvider
        nOfSharesDataProvider = FDataProvider(data = data.KrxKospiNOShare(), query=query.FNOfSharesQuery().get_query('parquet'))
        fdps.register(priceDataProvider, 'priceData')
        fdps.register(nOfSharesDataProvider, 'nOfShares')

        return fdps.get_dataProviders()


if __name__ == '__main__':
    from datetime import datetime
    import time
    dataProvider=AKrxKospiDataProviders().get_dataProviders()
    s = time.time()
    df=dataProvider.priceData.data.reset_index()
    print(df.pivot(index='date', columns='ticker', values='close').iloc[-10:,-5:])
    e = time.time()
    print(f'{e-s:0.4f}')