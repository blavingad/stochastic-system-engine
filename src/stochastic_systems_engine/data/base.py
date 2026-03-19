from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

# define the rule that every data loader must follow, it says "what must be done", not "how do to it"
# it guarantess that any loader will be strucured as it follows: load_history(symbol, start, end)
class PriceDataLoader(ABC):
    
    @abstractmethod
    def load_history(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        raise NotImplementedError