import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Metrics import Beta
from Timeframe import Timeframe


class Alpha(FinancialMetric):

    def __init__(self, beta: Beta):

        self.__beta = beta

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00000):
        beta = self.__beta.compute(returns, timeframe, spread)
        slices = self._annual_slices[timeframe]
        mean_return = self.__beta.returns.mean() * slices
        mean_benchmark = self.__beta.benchmark.mean() * slices

        return mean_return - beta * mean_benchmark
