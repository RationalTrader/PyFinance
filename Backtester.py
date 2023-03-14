import pandas as pd

from Metrics import *
from Providers import DataProvider
from Timeframe import Timeframe


class Backtester:

    def __init__(self, data_provider: DataProvider, benchmark_symbol: str):

        self.__is_initialized = False
        self.__data_provider = data_provider
        self.__benchmark_symbol = benchmark_symbol
        self.__day_grouper = pd.Grouper(key='time', freq='d')

    def __initialize(self) -> None:

        benchmark = self.__data_provider.get_rates(self.__benchmark_symbol, Timeframe.D1, None)
        benchmark = benchmark["close"]
        benchmark = benchmark.pct_change(1)
        benchmark = benchmark.tz_localize(None)

        self.__benchmark = benchmark

        self.__beta = Beta(self.__data_provider, benchmark)
        self.__alpha = Alpha(self.__beta)
        self.__sharpe_ratio = SharpeRatio()
        self.__sharpe_ratio.is_debug = True
        self.__sortino_ratio = SortinoRatio()
        self.__max_drawdown = MaxDrawdown()
        self.__valueAtRisk = ValueAtRisk()
        self.__conditionalValueAtRisk = ConditionalValueAtRisk()

        self.__is_initialized = True

    def analyse(self, returns: pd.Series) -> dict[str, pd.Series | float]:

        if not self.__is_initialized:

            self.__initialize()

        returns = returns.reset_index(drop=False)
        returns.groupby(self.__day_grouper).sum()
        returns = returns.set_index("time")
        returns = returns.squeeze()

        all_returns = pd.concat((returns, self.__benchmark), axis=1)
        all_returns = all_returns.dropna()

        portfolio = all_returns.iloc[:, 0]
        benchmark = all_returns.iloc[:, 1]

        metrics = {
            "returns": portfolio,
            "benchmark": benchmark,
            "beta": self.__beta.compute(returns),
            "alpha": self.__alpha.compute(returns),
            "sharpe": self.__sharpe_ratio.compute(returns, Timeframe.D1, spread=0.00000),
            "sortino": self.__sortino_ratio.compute(returns),
            "max_drawdown": self.__max_drawdown.compute(returns),
            "value_at_risk": self.__valueAtRisk.compute(returns),
            "conditional_value_at_risk": self.__conditionalValueAtRisk.compute(returns)
        }

        return metrics
