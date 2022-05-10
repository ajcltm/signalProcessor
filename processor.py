import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
from abc import ABC, abstractclassmethod
from datetime import datetime
from emitter import Emitter, BTAlgoEmitter
from receiver import Receiver, BTAlgoReceiver
from users import User
from dataProvider import DataProvider

class Processor(ABC):
        
    @abstractclassmethod
    def execute(self):
        pass

class BTAlgo(Processor):
    def __init__(self, emitter:Emitter, receiver:Receiver, user:User) -> None:
        self.emitter = emitter
        self.receiver = receiver
        self.user = user
        self.receiver.receive()
    
    def execute(self):
        self.emitter.emit()

class BTAlgoFactory:
    def __init__(self, user:User)->None:
        sp = signal('BTAlgo')
        self.__u = user
        self.__r = BTAlgoReceiver(signal=sp, strategy=user.strategy)
        self.__e = BTAlgoEmitter(signal=sp, date_universe=self.__u.dataProvider.date_universe)

    def get_processor(self) -> Processor:
        return BTAlgo(emitter=self.__e, receiver=self.__r, user=self.__u)


if __name__ == '__main__':
    import sys
    parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    sys.path.append(parentPath) # 경로 추가
    from datetime import datetime
    from blinker import signal
    from users import User
    from secretary import Secratary
    from dataProvider import DataProvider, YahooProvider
    import pandas as pd
    import FinanceDataReader as fdr

    df_spx = fdr.StockListing('S&P500')
    # print(df_spx)
    tickerLst = df_spx.Symbol.to_list()
    start, end = datetime(2005, 4, 1), datetime(2022, 4, 19)
    print(tickerLst[:20])
    # tickerLst = ['QLD', 'NVDA', 'AMZN', 'ARVL']
    dataProvider = YahooProvider(ticker=tickerLst[:20], start=start, end=end)
    bt_algo = BTAlgoFactory(user=User(dataProvider)).get_processor()
    bt_algo.execute()
    print(pd.DataFrame(bt_algo.user.broker.assets_transaction))
    print(pd.DataFrame(bt_algo.user.banker.account.cash_transaction))
    print(bt_algo.user.banker.account.cash)
    bt_algo.user.set_secretary()
    print(bt_algo.user.secretary.get_funding_table())
    print(bt_algo.user.secretary.get_cash_table())
    print(bt_algo.user.secretary.get_assets_table())
    print(bt_algo.user.secretary.get_portfolio_table())


