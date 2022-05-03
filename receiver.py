from typing import Protocol, Callable
from blinker import signal

class Receiver(Protocol):

    def __init__(self, signal:signal, strategy:Callable[[], None]) -> None:
        ...

    def receive(self) -> None:
        ...

class BTAlgoReceiver:

    def __init__(self, signal:signal, strategy:Callable[[], None]) -> None:
        self.signalProcessor = signal
        self.strategy = strategy

    def receive(self) -> None:
        self.signalProcessor.connect(self.strategy)
