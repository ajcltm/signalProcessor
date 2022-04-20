import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
from abc import ABC, abstractclassmethod
from datetime import datetime
from emitter import Emitter, BTAlgoEmitter
from receiver import Receiver, BTAlgoReceiver
from users import User, I

class Processor(ABC):
    def __init__(self, emitter:Emitter, receiver:Receiver, user:User, dataProvider) -> None:
        self.emitter = emitter
        self.receiver = receiver
        self.user = user
        self.receiver.receive(user.strategy)
        self.dataProvider = dataProvider
        
    @abstractclassmethod
    def execute(self):
        self.emitter.emit()

class BTAlgo(Processor):
    def __init__(self, emitter:Emitter, receiver:Receiver, user:User) -> None:
        self.emitter = emitter
        self.receiver = receiver
        self.user = user
        self.receiver.receive()
    
    def execute(self):
        self.emitter.emit()

class BTAlgoFactory:
    def __init__(self, user:User, start:datetime, end:datetime):
        sp = signal('BTAlgo')
        r = BTAlgoReceiver(signal=sp, strategy=user.strategy)
        e = BTAlgoEmitter(signal=sp, start=start, end=end)

        self.BTAlgo = BTAlgo(emitter=e, receiver=r, user=user)

    def execute(self):
        self.BTAlgo.execute()


if __name__ == '__main__':
    import sys
    parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    sys.path.append(parentPath) # 경로 추가
    from datetime import datetime
    from blinker import signal
    from users import User, I
    
    start, end = datetime(2022, 4, 1), datetime(2022, 4, 19)
    
    BTAlgoFactory(user=I('NVDA'), start=start, end=end).execute()