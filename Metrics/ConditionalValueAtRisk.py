import numpy as np
import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Timeframe import Timeframe


class ConditionalValueAtRisk(FinancialMetric):

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00000):

        slices = self._annual_slices[timeframe]
        annualization_factor = np.sqrt(slices)

        theta = 0.01
        n = 100000
        t = int(n * theta)
        mean = returns.mean() * slices
        std = returns.std() * annualization_factor
        np.random.seed(70)
        simulations = np.random.normal(mean, std, size=(n,))
        vec = pd.DataFrame(simulations, columns=["simulations"])
        conditional_value_at_risk = -vec.sort_values(by="simulations").iloc[0:t, :].mean().values[0]

        return conditional_value_at_risk
