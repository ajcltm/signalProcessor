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
        return PrepareOrder(self.broker, self.accountant)


class PrepareOrder:

    def __init__(self, banker, broker, accountant):
        self.banker = banker
        self.broker = broker
        self.accountant = accountant

    def get_order_paper(self, new_tickers_weight):
        old_orders = self.get_old_orders()
        if not old_orders:
            return new_tickers_weight

    def get_old_orders(self):
        if not self.broker.assets_transaction :
            return None
        old_assets = self.accountant.assetsOrganizer.get_assets_values_history().to_dict(orient='records')[0]
        return old_assets


