import datetime

import numpy as np
import pandas as pd

from Criterions import *
from Features import *
from Metrics import *
from OptimalLeverage import OptimalLeverage
from OptimalStopLoss import OptimalStopLoss
from OptimalTakeProfit import OptimalTakeProfit
from Predictors import *
from Providers import *
from Timeframe import *

from AssetSelection import AssetSelection
from Backtester import Backtester
from DataEngineering import DataEngineering
from PortfolioOptimization import PortfolioOptimization
from StrategyCombination import StrategyCombination
from StrategySelection import StrategySelection
from UserInterface import UserInterface

settings = {
    "last_quote_delta": datetime.timedelta(days=7),
    "max_spread": 100.0 / 100,

    "symbols": ["USDTRY", "XPDUSD", "EURRUB", "GBPSEK", "USDNOK"],

    "features": {
        Mean(15),
        Mean(60),
        StandardDeviation(15),
        StandardDeviation(60)
    },

    "timeframe": Timeframe.D1,
    "min_bar_count": 600,
    "max_bar_count": 3500,

    "selection_metric": SharpeRatio(),

    "training_ratio": 0.70,
    "test_ratio": 0.20,
    "predictors": {
        LinearModel(is_regression=False),
        SupportVectorMachine(is_regression=False),
        DecisionTree(is_regression=False, max_depth=6, random_state=70),
        # LinearModel(is_regression=True),
        # SupportVectorMachine(is_regression=True),
        # DecisionTree(is_regression=True, max_depth=6, random_state=70)
    },

    "portfolio_criterion": MeanVariance(),
    "benchmark": "^GSPC",
    "max_draw_down": 20,

    "adjust_tp_sl": False
}


if __name__ == '__main__':

    ui = UserInterface()

    terminal = Mt5Terminal()
    data_provider = Mt5DataProvider(terminal)
    benchmark_provider = YfDataProvider()

    asset_selection = AssetSelection(data_provider)
    asset_selection.max_last_quote_delta = settings["last_quote_delta"]
    asset_selection.max_spread = settings["max_spread"]

    data_engineering = DataEngineering(settings["features"])

    strategy_selection = StrategySelection(data_provider, data_engineering, settings["selection_metric"])
    strategy_selection.timeframe = settings["timeframe"]
    strategy_selection.min_bar_count = settings["min_bar_count"]
    strategy_selection.max_bar_count = settings["max_bar_count"]
    strategy_selection.training_ratio = settings["training_ratio"]
    strategy_selection.test_ratio = settings["test_ratio"]

    strategy_combination = StrategyCombination(data_provider, data_engineering)
    strategy_combination.timeframe = settings["timeframe"]
    strategy_combination.max_bar_count = settings["max_bar_count"]
    strategy_combination.training_ratio = settings["training_ratio"]
    strategy_combination.test_ratio = settings["test_ratio"]

    portfolioOptimization = PortfolioOptimization(settings["portfolio_criterion"])
    backtester = Backtester(benchmark_provider, settings["benchmark"])

    take_profit = OptimalTakeProfit(settings["selection_metric"])
    take_profit.timeframe = settings["timeframe"]

    stop_loss = OptimalStopLoss(settings["selection_metric"])
    stop_loss.timeframe = settings["timeframe"]

    leverage = OptimalLeverage()
    leverage.max_draw_down = settings["max_draw_down"]

    try:

        # assets selection

        symbols = settings["symbols"]

        if symbols is None:

            symbols = data_provider.get_symbols()
            symbols = asset_selection.filter(symbols)
            ui.display_asset_selection(symbols)
            symbols = symbols["symbol"]

        # strategies selection

        strategies = strategy_selection.get_best_strategies(symbols, settings["predictors"])
        strategies = strategies.head(35)
        ui.display_strategies(strategies)

        strategies = strategies.drop_duplicates(subset="symbol")
        strategies = strategies.head(5)
        ui.display_asset_combination(strategies)

        # predictions combination

        returns, low_returns, high_returns = strategy_combination.combine(strategies)
        ui.display_periods(returns)
        ui.display_predictions(returns.test)

        # portfolio optimization

        risk_contributions = portfolioOptimization.optimize(returns.test)
        ui.display_risk_contributions(strategies, risk_contributions)

        # backtest

        portfolio_returns = np.multiply(returns.validation, risk_contributions).sum(axis=1)
        backtest = backtester.analyse(portfolio_returns)
        ui.display_backtest_metrics(backtest)
        ui.display_cumulative_return(backtest["returns"], backtest["benchmark"])
        ui.display_drawdown(backtest["returns"])

        if settings["adjust_tp_sl"]:

            # take profit, stop loss and leverage

            test_returns = np.multiply(returns.test, risk_contributions).sum(axis=1)
            test_low_returns = np.multiply(low_returns.test, risk_contributions).sum(axis=1)
            test_high_returns = np.multiply(high_returns.test, risk_contributions).sum(axis=1)

            tp = take_profit.find_best_tp(test_returns, test_high_returns)
            sl = stop_loss.find_best_sl(test_returns, test_low_returns)
            lv = leverage.find_best_leverage(test_returns, test_low_returns, test_high_returns, tp, sl)
            ui.display_parameters(tp, sl, lv)

            # adjusted backtest

            returns = np.multiply(returns.validation, risk_contributions).sum(axis=1)
            low_returns = np.multiply(low_returns.validation, risk_contributions).sum(axis=1)
            high_returns = np.multiply(high_returns.validation, risk_contributions).sum(axis=1)

            spread = 0.00035
            pf = pd.concat((low_returns, returns, high_returns), axis=1).dropna() - spread
            pf.columns = ["low", "return", "high"]

            pf["return"] = np.where(pf["high"] > tp, tp, pf["return"])
            pf["return"] = np.where(pf["low"] < -sl, -sl, pf["return"])

            backtest = backtester.analyse(pf["return"] * lv)
            ui.display_backtest_metrics(backtest)
            ui.display_cumulative_return(backtest["returns"], backtest["benchmark"])
            ui.display_drawdown(backtest["returns"])

    finally:
        terminal.shutdown()
