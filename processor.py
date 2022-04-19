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
