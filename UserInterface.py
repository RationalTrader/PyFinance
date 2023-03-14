import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from DataSet import DataSet


# noinspection PyMethodMayBeStatic
class UserInterface:

    def display_asset_selection(self, symbols: pd.DataFrame):

        print()
        print("> Asset selection:")
        print(symbols)

    def display_strategies(self, strategies: pd.DataFrame):

        print()
        print("> Best strategies:")
        print(strategies)

    def display_asset_combination(self, strategies: pd.DataFrame):

        print()
        print("> Asset combination:")
        print(strategies["symbol"])

    def display_period(self, data_frame: pd.DataFrame, name: str):

        idx = data_frame.index
        period = idx.to_period("D")
        first = period[0]
        last = period[len(period) - 1]
        print("> " + name + ": " + str(first) + ":" + str(last))

    def display_periods(self, data_frame: DataSet):

        print()
        print("> Periods:")
        self.display_period(data_frame.training, "- training  ")
        self.display_period(data_frame.test, "- test      ")
        self.display_period(data_frame.validation, "- validation")

    def display_predictions(self, predictions: pd.DataFrame):

        predictions.cumsum().plot(figsize=(15, 8))
        plt.show()

    def display_risk_contributions(self, strategies: pd.DataFrame, risk_contributions: np.ndarray):

        print()
        print("> Risk contributions:")
        percentages = np.round(risk_contributions, 3) * 100
        contributions = pd.DataFrame(percentages, index=strategies["symbol"], columns=["%"])
        print(contributions["%"])
        print()

    def display_backtest_metrics(self, metrics: dict[str, float]):

        beta = metrics["beta"]
        alpha = metrics["alpha"]
        sharpe = metrics["sharpe"]
        sortino = metrics["sortino"]
        var = metrics["value_at_risk"]
        cvar = metrics["conditional_value_at_risk"]
        var_ratio = cvar / var
        drawdown = metrics["max_drawdown"]

        print(f"""
          -----------------------------------------------------------------------------
          Beta: {np.round(beta, 3)} \t Alpha: {np.round(alpha * 100, 2)} %\t \
          Sharpe: {np.round(sharpe, 3)} \t Sortino: {np.round(sortino, 3)}
        -----------------------------------------------------------------------------
          VaR: {np.round(var * 100, 2)} %\t cVaR: {np.round(cvar * 100, 2)} % \t \
          VaR/cVaR: {np.round(var_ratio, 3)} \t Drawdown: {np.round(drawdown * 100, 2)} %
        -----------------------------------------------------------------------------""")

    def display_cumulative_return(self, returns: pd.Series, benchmark: pd.Series):

        plt.style.use('seaborn-v0_8')
        font = {'weight': 'bold', "size": "300"}
        plt.rc('font', **font)

        plt.figure(figsize=(15, 8))
        plt.plot(returns.cumsum() * 100, color="#035593", linewidth=3)
        plt.plot(benchmark.cumsum() * 100, color="#068C72", linewidth=3)
        plt.title("CUMULATIVE RETURN", size=15)
        plt.ylabel("Cumulative return %", size=15)
        plt.xticks(size=15, fontweight="bold")
        plt.yticks(size=15, fontweight="bold")
        plt.legend(["Strategy", "Benchmark"])
        plt.show()

    def display_drawdown(self, returns: pd.Series):

        cumulative_returns = (returns + 1).cumprod()
        running_max = np.maximum.accumulate(cumulative_returns.dropna())
        drawdown = cumulative_returns / running_max - 1

        plt.style.use('seaborn-v0_8')
        font = {'weight': 'bold', "size": "300"}
        plt.rc('font', **font)

        plt.figure(figsize=(15, 8))
        plt.fill_between(drawdown.index, drawdown * 100, 0, color="#CE5151")
        plt.plot(drawdown.index, drawdown * 100, color="#930303", linewidth=3)
        plt.title("DRAWDOWN", size=15)
        plt.ylabel("Drawdown %", size=15)
        plt.xticks(size=15, fontweight="bold")
        plt.yticks(size=15, fontweight="bold")
        plt.show()

    def display_parameters(self, tp: float, sl: float, lv: float):

        print()
        tp = np.round(tp * 100, 2)
        print("Take profit: " + str(tp) + " %")
        sl = np.round(sl * 100, 2)
        print("Stop loss:   " + str(sl) + " %")
        lv = np.round(lv, 2)
        print("Leverage:    " + str(lv))

