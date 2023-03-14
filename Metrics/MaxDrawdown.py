import numpy as np
import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Timeframe import Timeframe


class MaxDrawdown(FinancialMetric):

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00000):

        cumulative_returns = (returns + 1).cumprod()
        cumulative_returns = cumulative_returns.dropna()
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = ((cumulative_returns / running_max) - 1)

        return -drawdown.min()
