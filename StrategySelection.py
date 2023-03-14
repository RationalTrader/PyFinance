from tqdm import tqdm

from DataEngineering import *
from DataReduction import *
from DataScaling import *
from DataSet import *
from DataSplit import *
from Metrics import *
from Predictors import *
from Providers import *
from Timeframe import *


class StrategySelection:

    def __init__(self, data_provider: DataProvider, data_engineering: DataEngineering, metric: FinancialMetric):

        self.__data_provider = data_provider
        self.__data_engineering = data_engineering
        self.__metric = metric

        self.__data_scaling = DataScaling()
        self.__data_reduction = DataReduction(3)

        self.timeframe = Timeframe.D1
        self.min_bar_count = 100
        self.max_bar_count = 1000
        self.training_ratio = 0.7
        self.test_ratio = 0.2

    def get_best_strategies(self, symbols: pd.DataFrame, predictors: set[DataPredictor]) -> pd.DataFrame:

        strategies = []
        print()

        for symbol in tqdm(symbols):

            rates = self.__data_provider.get_rates(symbol, self.timeframe, self.max_bar_count)

            if rates is None or len(rates) < self.min_bar_count:
                continue

            returns, low_returns, high_returns, features = self.__data_engineering.add_features(rates)

            data_split = DataSplit(returns, self.training_ratio, self.test_ratio)
            returns = DataSet(returns, data_split)
            features = DataSet(features, data_split)

            features = self.__data_scaling.scale(features)
            features = self.__data_reduction.reduce(features)

            x_train = features.training.to_numpy()
            y_train = returns.training
            x_test = features.all.to_numpy()

            for predictor in predictors:

                predictor.fit(x_train, y_train)
                positions = predictor.predict(x_test)
                predictions = positions * returns.all
                predictions = DataSet(predictions, data_split)
                metric = self.__metric.compute(predictions.test, self.timeframe)
                length = len(returns.all)
                strategies.append([symbol, predictor, metric, length])

        strategies = pd.DataFrame(strategies, columns=["symbol", "model", "metric", "length"])
        strategies = strategies.sort_values(by="metric", ascending=False)

        return strategies
