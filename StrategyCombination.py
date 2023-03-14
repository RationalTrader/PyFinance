from DataEngineering import *
from DataReduction import *
from DataScaling import *
from DataSet import *
from DataSplit import *
from Predictors import *
from Providers import *
from Timeframe import *


class StrategyCombination:

    def __init__(self, data_provider: DataProvider, data_engineering: DataEngineering):

        self.__data_provider = data_provider
        self.__data_engineering = data_engineering

        self.__data_scaling = DataScaling()
        self.__data_reduction = DataReduction(3)

        self.timeframe = Timeframe.D1
        self.max_bar_count = 1000
        self.training_ratio = 0.7
        self.test_ratio = 0.2

    def combine(self, strategies: pd.DataFrame) -> (DataSet, DataSet, DataSet):

        all_returns = pd.DataFrame()
        all_low_returns = pd.DataFrame()
        all_high_returns = pd.DataFrame()

        for index, strategy in strategies.iterrows():

            symbol = strategy["symbol"]
            model = strategy["model"]

            rates = self.__data_provider.get_rates(symbol, self.timeframe, self.max_bar_count)

            returns, low_returns, high_returns, features = self.__data_engineering.add_features(rates)

            symbol_data_split = DataSplit(returns, self.training_ratio, self.test_ratio)
            returns = DataSet(returns, symbol_data_split)
            features = DataSet(features, symbol_data_split)

            features = self.__data_scaling.scale(features)
            features = self.__data_reduction.reduce(features)

            x_train = features.training
            y_train = returns.training
            x_test = features.all

            voting = VotingCombination(model.is_regressor)
            voting.fit(x_train, y_train)
            positions = voting.predict(x_test)

            predictions = positions * returns.all
            low_predictions = np.where(positions > 0, low_returns, -high_returns)
            low_predictions = pd.Series(low_predictions, index=predictions.index)
            high_predictions = np.where(positions > 0, high_returns, -low_returns)
            high_predictions = pd.Series(high_predictions, index=predictions.index)

            all_returns[symbol] = predictions
            all_low_returns[symbol] = low_predictions
            all_high_returns[symbol] = high_predictions

        all_returns = all_returns.dropna()
        data_split = DataSplit(all_returns, self.training_ratio, self.test_ratio)
        all_returns = DataSet(all_returns, data_split)

        all_low_returns = all_low_returns.dropna()
        data_split = DataSplit(all_low_returns, self.training_ratio, self.test_ratio)
        all_low_returns = DataSet(all_low_returns, data_split)

        all_high_returns = all_high_returns.dropna()
        data_split = DataSplit(all_high_returns, self.training_ratio, self.test_ratio)
        all_high_returns = DataSet(all_high_returns, data_split)

        return all_returns, all_low_returns, all_high_returns
