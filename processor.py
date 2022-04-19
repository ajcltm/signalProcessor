import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
from emitter import Emitter
from receiver import Receiver

class Processor:
    
    def __init__(self, emitter:Emitter, receiver:Receiver):
        self.emitter = emitter
        self.receiver = receiver
        self.receiver.receive()
    
    def execute(self):
        self.emitter.emit()


if __name__ == '__main__':
    import sys
    parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    sys.path.append(parentPath) # 경로 추가
    from datetime import datetime
    from blinker import signal
    from signalProcessor import receiver, emitter, processor

    class I:
        def __init__(self, ticker):
            self.ticker = ticker

        def strategy(self, sender, **kwargs):
            idx = kwargs['idx']
            date = kwargs['date']
            print(idx, date, self.ticker)

    sp = signal('BTAlgo')

    r = receiver.BTAlgoReceiver(signal=sp, strategy=I('NVDA').strategy)
    start, end = datetime(2022, 4, 1), datetime(2022, 4, 19)
    e = emitter.BTAlgoEmitter(signal=sp, start=start, end=end)

    processor.Processor(emitter=e, receiver=r).execute()
