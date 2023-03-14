import numpy as np
import pandas as pd

from Metrics import FinancialMetric
from Timeframe import Timeframe


class OptimalStopLoss:

    def __init__(self, metric: FinancialMetric):

        self.__metric = metric

        self.timeframe = Timeframe.D1

    def find_best_sl(self, returns, low_returns, spread=0.00035):

        sl_values = np.linspace(0, 10, 50)

        metrics = pd.DataFrame([self.__compute_metric(sl, returns, low_returns, spread) for sl in sl_values],
                               index=sl_values, columns=["sharpe"])

        return metrics["sharpe"].idxmax() / 100

    def __compute_metric(self, sl: float, returns, low_returns, spread: float):

        sl = sl / 100

        pf = pd.concat((returns, low_returns), axis=1).dropna()
        pf.columns = ["return", "low"]

        pf["return"] = np.where(pf["low"] < -sl, -sl, pf["return"])

        return self.__metric.compute(pf["return"], self.timeframe, spread)
