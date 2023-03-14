import numpy as np
import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Timeframe import Timeframe


class SortinoRatio(FinancialMetric):

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00000):

        slices = self._annual_slices[timeframe]
        annualization_factor = np.sqrt(slices)

        mean = returns.mean()
        downward = returns[returns < 0]
        std = downward.std()

        sortino = annualization_factor * (mean - spread) / std

        return sortino
