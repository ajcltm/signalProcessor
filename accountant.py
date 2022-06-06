import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from utility import time


class Accountant:

    def __init__(self, cash_transaction, assets_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.assets_transaction = assets_transaction
        self.dataProvider = dataProvider

        self.fundingOrganizer = FundingOrganizer(self.cash_transaction, self.dataProvider)
        self.cashOrganizer = CashOrganizer(self.cash_transaction, self.dataProvider)
        self.assetsOrganizer = AssetsOrganizer(self.assets_transaction, self.dataProvider)

    @time.timeMeasure
    def get_funding_table(self):
        return self.fundingOrganizer.get_table()

    @time.timeMeasure
    def get_cash_table(self):
        return self.cashOrganizer.get_table()

    @time.timeMeasure
    def get_assets_table(self):
        return self.assetsOrganizer.get_table()

    @time.timeMeasure
    def get_portfolio_table(self):
        funding_table = self.get_funding_table()
        cash_table = self.get_cash_table()
        assets_table = self.get_assets_table()
        if assets_table.empty:
            return pd.DataFrame()
        df = pd.merge(left=assets_table[['date', 'assets_value']], right=funding_table, on='date', how='left')
        df = pd.merge(left=df, right=cash_table, on='date', how='left')
        df = df.fillna(0)
        df.amounts = df.amounts.cumsum()
        df.rename(columns={'amounts':'cash_value'}, inplace=True)
        df = df[['date', 'funding', 'cash_value', 'assets_value']]
        df.columns = ['date', 'funding', 'closeCashValue', 'closeAssetsValue']
        df['closeTotalValue'] = df.closeCashValue + df.closeAssetsValue
        df['openCashValue'] = df.closeCashValue.shift(1)
        df['openAssetsValue'] = df.closeAssetsValue.shift(1)
        df = df.fillna(0)
        df['openTotalValue'] = df.openCashValue + df.openAssetsValue
        df = df[['date', 'funding', 'openCashValue', 'closeCashValue', 'openAssetsValue', 'closeAssetsValue', 'openTotalValue', 'closeTotalValue']]
        df['portfolioReturn'] = (df.closeTotalValue) / (df.openTotalValue+df.funding) -1
        return df


class FundingOrganizer:

    def __init__(self, cash_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.dataProvider = dataProvider

    def get_table(self):
        df = self.get_funding_history()
        return df

    def get_funding_history(self):
        if not self.cash_transaction:
            return pd.DataFrame()
        df = pd.DataFrame(self.cash_transaction)
        df = df.loc[~(df.loc[:, 'offer']=='broker')]
        df = df.groupby('date').sum()
        df = df.reset_index()
        df.columns = ['date','funding']
        return df


class CashOrganizer:

    def __init__(self, cash_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.dataProvider = dataProvider

    def get_table(self):
        df = self.get_cash_history()
        return df

    def get_cash_history(self):
        if not self.cash_transaction:
            return pd.DataFrame()
        df = pd.DataFrame(self.cash_transaction)
        df = df.groupby('date').sum()
        return df


class AssetsOrganizer:

    def __init__(self, assets_transaction, dataProvider):
        self.assets_transaction = assets_transaction
        self.dataProvider = dataProvider

    def get_table(self):
        df = self.get_assets_values_history()
        df = self.get_assets_values_full_history(df)
        df = self.get_daily_assests_values(df)
        return df

    def get_assets_values_history(self):
        df = pd.DataFrame(self.assets_transaction)
        if not self.assets_transaction:
            return pd.DataFrame()
        df = df.groupby(['date', 'ticker']).sum()
        df = df.reset_index()
        df = df.pivot(index='date', columns='ticker', values='quantity')
        df = df.reset_index()
        return df

    def get_assets_values_full_history(self, assets_values_history):
        if assets_values_history.empty:
            return pd.DataFrame()
        date_df = pd.DataFrame(self.dataProvider.priceData.query.get_dateUniverse(), columns=['date'])
        df = pd.merge(left=date_df, right=assets_values_history, on='date', how='left')
        df = df.fillna(0)
        df = df.set_index('date')
        df = df.cumsum()
        df = df.reset_index()
        return df

    @time.timeMeasure
    def get_daily_assests_values(self, assets_values_full_history):
        if assets_values_full_history.empty:
            return pd.DataFrame()
        df = assets_values_full_history
        cols = df.columns
        tickers = [i for i in cols if not i == 'date']
        df_ = self.dataProvider.priceData.query.get_tickerInfo_columnBase(tickers=tickers, valueName='close')
        assets_value = np.sum(df.set_index('date').values * df_.fillna(0).values, axis=1)
        df = pd.merge(left=df, right=df_, on='date', how='left')
        df['assets_value'] = assets_value
        return df