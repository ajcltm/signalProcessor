import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
from abc import ABC, abstractclassmethod
from datetime import datetime
from emitter import Emitter, BTAlgoEmitter
from receiver import Receiver, BTAlgoReceiver
from users import User

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
        self.__e = BTAlgoEmitter(signal=sp, date_universe=self.__u.dataProvider.priceData.query.get_dateUniverse())

    def get_processor(self) -> Processor:
        return BTAlgo(emitter=self.__e, receiver=self.__r, user=self.__u)


if __name__ == '__main__':
    import sys
    parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    sys.path.append(parentPath) # 경로 추가
    from datetime import datetime
    from blinker import signal
    from users import User, SmallInvester
    from dataProvider import dataProvider
    import pandas as pd
    pd.options.display.float_format = '{:.02f}'.format

    dataProvider = dataProvider.AKrxKospiDataProviders().get_dataProviders()
    bt_algo = BTAlgoFactory(user=SmallInvester(dataProvider)).get_processor()
    bt_algo.execute()
    print(bt_algo.user.accountant.get_portfolio_table())