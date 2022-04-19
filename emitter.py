from typing import Protocol, Callable
from datetime import datetime, timedelta
from blinker import signal

class Emitter(Protocol):
    
    def __init__(self, signal:signal) -> None:
        ...

    def emit(self) -> None:
        ...

class BTAlgoEmitter:

    def __init__(self, signal:signal, start:datetime, end:datetime) -> None:
        self.signalProcessor = signal
        self.date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]

    def emit(self) -> None:
        for idx, date in enumerate(self.date_generated):
            self.signalProcessor.send('anonymous', idx=idx, date=date)
