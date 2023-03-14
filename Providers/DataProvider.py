import pandas as pd

from Timeframe import *


class DataProvider:

    _index = ["symbol", "sector", "description", "spread"]

    # returned data frame: "Symbol": str, "Sector": str, "Description": str, "Spread": float
    def get_symbols(self) -> pd.DataFrame:
        raise NotImplementedError

    def get_last_quote_time(self, symbol: str) -> pd.Timestamp:
        raise NotImplementedError

    def get_spread(self, symbol: str) -> float:
        raise NotImplementedError

    # returned data frame: "open": float, "high": float, "low": float, "close", "volume": int
    def get_rates(self, symbol: str, timeframe: Timeframe, count: int | None) -> pd.DataFrame:
        raise NotImplementedError
