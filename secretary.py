import pandas as pd

class Secretary:

    def __init__(self, banker, broker, accountant, advisor, dataProvider, recorder):
        self.banker = banker
        self.broker = broker
        self.accountant = accountant
        self.advisor = advisor
        self.dataProvider = dataProvider
        self.recorder = recorder

    def prepareOrder(self):
        return PrepareOrder(self.banker, self.broker, self.accountant, self.dataProvider, self.recorder)


class PrepareOrder:

    def __init__(self, banker, broker, accountant, dataProvider, recorder):
        self.banker = banker
        self.broker = broker
        self.accountant = accountant
        self.dataProvider = dataProvider
        self.recorder = recorder

    def get_order_plan(self, new_tickers_weight, cash='current_cash'):
        if cash == 'current_cash':
            cash = self.banker.account.cash
        old_tickers_amounts = self.get_old_tickers_amounts()
        df = pd.merge(left=new_tickers_weight, right=old_tickers_amounts, left_on='ticker', right_on='ticker', how='outer')
        df = df.fillna(0)
        df = df.assign(allocated_cash=df['weight']*cash)
        df = df.assign(price=df.apply(lambda row: self.dataProvider.priceData.query.get_price_at_tickerAndDate(row['ticker'], self.recorder.date, 'open'), axis=1))
        df = df.assign(target_amounts = divmod(df.allocated_cash, df.price)[0])
        df = df.assign(order_plan_amounts = df.target_amounts-df.old_amounts)
        return df.set_index('ticker').to_dict()['order_plan_amounts']

    def get_old_tickers_amounts(self):
        if not self.broker.assets_transaction :
            return pd.DataFrame({'ticker':[], 'old_amounts':[]})
        old_assets = self.accountant.assetsOrganizer.get_assets_values_history().set_index('date').to_dict(orient='records')[0]
        old_tickers_amounts = pd.DataFrame({'ticker':old_assets.keys(), 'old_amounts':old_assets.values()})
        return old_tickers_amounts


