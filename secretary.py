import pandas as pd

class Secratary:

    def __init__(self, dataProvider):
        self.dataProvider = dataProvider

    def get_funds_change(self, cash_transaction):
        df = self.get_funds_history(cash_transaction)
        df = self.get_funds_full_history(df)
        return df
    
    def get_assets_values(self, assets_transaction):
        df = self.get_assets_values_history(assets_transaction)
        df = self.get_assets_values_full_history(df)
        df = self.get_daily_assests_values(df)
        return df

    def get_funds_history(self, cash_transaction:list):
        df = pd.DataFrame(cash_transaction)
        df = df.loc[~(df.loc[:, 'offer']=='broker')]
        return df

    def get_funds_full_history(self, funds_history):
        date_df = pd.DataFrame(self.dataProvider.date_universe, columns=['date'])
        df = pd.merge(left=date_df, right=funds_history, on='date', how='left')
        df = df.fillna(0)
        return df

    def get_assets_values_history(self, assets_transaction):
        df = pd.DataFrame(assets_transaction)
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
        print(assets_values_full_history)
        _dict = assets_values_full_history.to_dict('records')
        container_dict = []
        close_dict = []
        value = 0
        date=None
        idx =None
        for i in _dict:
            temp = {}
            for key in i.keys():
                if key == 'date':
                    date = i[key]
                    temp['date'] = date
                    idx = self.dataProvider.get_idx(date)
                else :
                    close = self.dataProvider.db[idx][date][key]['close']
                    value += close * i[key]
                    close_dict.append(close)
            temp['value'] = value
            container_dict.append(temp)
            value = 0
        df = pd.DataFrame(container_dict)
        return df, close_dict

    def get_assests_values_full_history(self, daily_assests_values):
        daily_assests_values

        # df['close'] = close_container
        # close_container = []
        # for i in assets_transaction:
        #     
        #     close = self.dataProvider.db[idx][i.date][i.ticker]['close']
        #     close_container.append(close)