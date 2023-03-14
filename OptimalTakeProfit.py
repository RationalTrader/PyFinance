import numpy as np
import pandas as pd

from Metrics import FinancialMetric
from Timeframe import Timeframe


class OptimalTakeProfit:

    def __init__(self, metric: FinancialMetric):

        self.__metric = metric

        self.timeframe = Timeframe.D1

    def find_best_tp(self, returns, high_returns, spread=0.00035):

        tp_values = np.linspace(0, 10, 50)

        metrics = pd.DataFrame([self.__compute_metric(tp, returns, high_returns, spread) for tp in tp_values],
                               index=tp_values, columns=["sharpe"])

        return metrics["sharpe"].idxmax() / 100

    def __compute_metric(self, tp: float, returns, high_returns, spread: float):

        tp = tp / 100

        pf = pd.concat((returns, high_returns), axis=1).dropna()
        pf.columns = ["return", "high"]

        pf["return"] = np.where(pf["high"] > tp, tp, pf["return"])

        return self.__metric.compute(pf["return"], self.timeframe, spread)
