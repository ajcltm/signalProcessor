import sys
from pathlib import Path
sys.path.append(Path.cwd().joinpath('signalProcessor'))
import data, query
import dataclasses
from datetime import datetime

class FDataProvider:

    def __init__(self, data:data.IData, query:query.IPriceQuery):
        self.data = data.get_data()
        self.query = query(self.data)


class FDataProviders:

    set_dict = dict()

    def register(self, dataProvider, name):
        self.set_dict[name] = dataProvider

    def get_dataProviders(self, date_universe_data='priceData'):
        parent_class = dataclasses.make_dataclass('parent_class', ['date_universe'])
        dc = dataclasses.make_dataclass('dataProvider', list(self.set_dict.keys()), bases=(parent_class,))
        date_universe = list(self.set_dict[date_universe_data].data.reset_index().date.drop_duplicates().to_dict().values())
        return dc(**dict({'date_universe':date_universe}, **self.set_dict))


# application
class AKrxKospiDataProviders:

    def get_dataProviders(self):
        fdps = FDataProviders()

        # price dataProvider

        # krx kospi price data
        k = data.KrxKospiOHLCV()
        priceDataProvider = FDataProvider(data = k, query=query.FPriceQuery().get_query('parquet'))
        
        # n of shares dataProvider
        nOfSharesDataProvider = FDataProvider(data = data.KrxKospiNOShare(), query=query.FNOfSharesQuery().get_query('parquet'))
        fdps.register(priceDataProvider, 'priceData')
        fdps.register(nOfSharesDataProvider, 'nOfShares')

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
    dataProvider=AKrxKospiDataProviders().get_dataProviders()
    print(dataProvider.priceData.data.tail())
    print(dataProvider.priceData.query.get_by_date(date=datetime(2022, 4, 1)))
    print(dataProvider.nOfShares.query.get_by_date(date=datetime(2022, 5, 3)))
    print(dataProvider.date_universe[-10:])