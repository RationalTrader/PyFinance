import pandas as pd

from Timeframe import *


class DataProvider:

    @property
    def name(self):
        raise NotImplementedError

    def get_symbols(self) -> list[str]:
        raise NotImplementedError

    def get_last_quote_time(self, symbol: str) -> pd.Timestamp:
        raise NotImplementedError

    def get_spread(self, symbol: str) -> float:
        raise NotImplementedError

    # returned data frame: "open": float, "high": float, "low": float, "close", "volume": int
    def get_rates(self, symbol: str, timeframe: Timeframe, count: int | None) -> pd.DataFrame:
        raise NotImplementedError

    def shutdown(self) -> None:
        pass
