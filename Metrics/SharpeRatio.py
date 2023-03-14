import numpy as np
import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Timeframe import Timeframe


class SharpeRatio(FinancialMetric):

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00035):

        slices = self._annual_slices[timeframe]
        annualization_factor = np.sqrt(slices)

        mean = returns.mean()
        std = returns.std()

        sharpe = annualization_factor * (mean - spread) / std

        return sharpe
