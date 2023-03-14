import pandas as pd

from Timeframe import Timeframe


class FinancialMetric:

    _annual_slices = {
        Timeframe.M1: 252 * 24 * 60,
        Timeframe.M5: 252 * 24 * 12,
        Timeframe.M15: 252 * 24 * 4,
        Timeframe.M30: 252 * 24 * 2,
        Timeframe.H1: 252 * 24,
        Timeframe.H4: 252 * 6,
        Timeframe.D1: 252,
        Timeframe.W1: 52,
        Timeframe.MN: 12
    }

    def compute(self, returns: pd.Series, timeframe: Timeframe, spread: float):
        raise NotImplementedError
