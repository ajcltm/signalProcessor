import pandas as pd

class Secratary:

    def __init__(self, cash_transaction, assets_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.assets_transaction = assets_transaction
        self.dataProvider = dataProvider

    def get_funding_table(self):
        return FundingOrganizer(self.cash_transaction, self.dataProvider).get_table()

    def get_cash_table(self):
        return CashOrganizer(self.cash_transaction, self.dataProvider).get_table()

    def get_assets_table(self):
        return AssetsOrganizer(self.assets_transaction, self.dataProvider).get_table()

    def get_portfolio_table(self):
        funding_table = self.get_funding_table()
        cash_table = self.get_cash_table()
        assets_table = self.get_assets_table()[['date', 'assets_value']]
        df = pd.merge(left=funding_table, right=cash_table, on='date', how='left')
        df = pd.merge(left=df, right=assets_table, on='date', how='left')
        df.columns = ['date', 'funding', 'closeCashValue', 'closeAssetsValue']
        df['closeTotalValue'] = df.closeCashValue + df.closeAssetsValue
        df['openCashValue'] = df.closeCashValue.shift(1)
        df['openAssetsValue'] = df.closeAssetsValue.shift(1)
        df['openTotalValue'] = df.openCashValue + df.openAssetsValue
        df = df.fillna(0)
        df = df[['date', 'funding', 'openCashValue', 'closeCashValue', 'openAssetsValue', 'closeAssetsValue', 'openTotalValue', 'closeTotalValue']]
        df['portfolioReturn'] = (df.closeTotalValue) / (df.openTotalValue+df.funding) -1
        return df

class FundingOrganizer:

    def __init__(self, cash_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.dataProvider = dataProvider

    def get_table(self):
        df = self.get_funding_history()
        df = self.get_funding_full_history(df)
        return df

    def get_funding_history(self):
        df = pd.DataFrame(self.cash_transaction)
        df = df.loc[~(df.loc[:, 'offer']=='broker')]
        df = df.groupby('date').sum()
        return df

    def get_funding_full_history(self, funding_history):
        date_df = pd.DataFrame(self.dataProvider.date_universe, columns=['date'])
        df = pd.merge(left=date_df, right=funding_history, on='date', how='left')
        df = df.fillna(0)
        df.columns = ['date','funding']
        return df


class CashOrganizer:

    def __init__(self, cash_transaction, dataProvider):
        self.cash_transaction = cash_transaction
        self.dataProvider = dataProvider

    def get_table(self):
        df = self.get_cash_history()
        df = self.get_cash_full_history(df)
        return df

    def get_cash_history(self):
        df = pd.DataFrame(self.cash_transaction)
        df = df.groupby('date').sum()
        return df

    def get_cash_full_history(self, cash_history):
        date_df = pd.DataFrame(self.dataProvider.date_universe, columns=['date'])
        df = pd.merge(left=date_df, right=cash_history, on='date', how='left')
        df = df.fillna(0)
        df = df.set_index('date')
        df = df.loc[:, 'amounts'].cumsum()
        df = df.reset_index()
        df.columns = ['date', 'cash_value']
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
        df = df.pivot(index='date', columns='ticker', values='quantity')
        df = df.reset_index()
        return df

    def get_assets_values_full_history(self, assets_values_history):
        date_df = pd.DataFrame(self.dataProvider.date_universe, columns=['date'])
        df = pd.merge(left=date_df, right=assets_values_history, on='date', how='left')
        df = df.fillna(0)
        df = df.set_index('date')
        df = df.cumsum()
        df = df.reset_index()
        return df

    def get_daily_assests_values(self, assets_values_full_history):
        df = assets_values_full_history
        cols = df.columns
        df['assets_value'] = 0
        price = []
        for i in cols:
            if not i == 'date':
                for dic in self.dataProvider.db:
                    close = list(dic.values())[0][i]['close']
                    price.append(close)
                df[f'{i}_p'] = price
                df['assets_value'] += df[i]*df[f'{i}_p']
                price = []
        return df
        


        # _dict = assets_values_full_history.to_dict('records')
        # container_dict = []
        # close_dict = []
        # value = 0
        # date=None
        # idx =None
        # for i in _dict:
        #     temp = {}
        #     for key in i.keys():
        #         if key == 'date':
        #             date = i[key]
        #             temp['date'] = date
        #             idx = self.dataProvider.get_idx(date)
        #         else :
        #             close = self.dataProvider.db[idx][date][key]['close']
        #             value += close * i[key]
        #             close_dict.append(close)
        #     temp['value'] = value
        #     container_dict.append(temp)
        #     value = 0
        # df = pd.DataFrame(container_dict)
        # return df, close_dict