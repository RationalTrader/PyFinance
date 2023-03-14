import numpy as np
import pandas as pd

from Metrics.FinancialMetric import FinancialMetric
from Providers import DataProvider
from Timeframe import Timeframe


class Beta(FinancialMetric):

    def __init__(self, data_provider: DataProvider, benchmark: pd.Series):

        self.__data_provider = data_provider
        self.__benchmark = benchmark
        self.returns = None
        self.benchmark = None

    def compute(self, returns: pd.Series, timeframe=Timeframe.D1, spread=0.00000):

        # returns = returns.squeeze()
        all_returns = pd.concat((returns, self.__benchmark), axis=1)
        all_returns = all_returns.dropna()
        self.returns = all_returns.iloc[:, 0]
        self.benchmark = all_returns.iloc[:, 1]

        cov = np.cov(all_returns, rowvar=False)[0][1]
        var = np.cov(all_returns, rowvar=False)[1][1]

        return cov / var
