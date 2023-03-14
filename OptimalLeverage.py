import numpy as np
import pandas as pd

from Metrics import FinancialMetric, MaxDrawdown
from Timeframe import Timeframe


class OptimalLeverage:

    def __init__(self):

        self.__max_draw_down = MaxDrawdown()

        self.max_draw_down = 20

    def find_best_leverage(self, returns, low_returns, high_returns, tp, sl):

        pf = pd.concat((returns, low_returns, high_returns), axis=1).dropna()
        pf.columns = ["return", "low", "high"]

        pf["return"] = np.where(pf["high"] > tp, tp, pf["return"])
        pf["return"] = np.where(pf["low"] < -sl, -sl, pf["return"])

        max_draw_down = self.__max_draw_down.compute(pf["return"])

        return self.max_draw_down / 100 / max_draw_down

    def __compute_metric(self, tp: float, returns, high_returns, spread: float):

        tp = tp / 100

        pf = pd.concat((returns, high_returns), axis=1).dropna()
        pf.columns = ["return", "high"]

        pf["return"] = np.where(pf["high"] > tp, tp, pf["return"])

        return self.__metric.compute(pf["return"], self.timeframe, spread)
