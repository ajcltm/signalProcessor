from typing import Protocol, Callable
from datetime import datetime, timedelta
from blinker import signal
from tqdm import tqdm

class Emitter(Protocol):
    
    def __init__(self, signal:signal) -> None:
        ...

    def emit(self) -> None:
        ...

class BTAlgoEmitter:

    def __init__(self, signal:signal, date_universe) -> None:
        self.signalProcessor = signal
        self.date_universe = date_universe

    def emit(self) -> None:
        for date in tqdm(self.date_universe):
            self.signalProcessor.send('anonymous', date=date)
