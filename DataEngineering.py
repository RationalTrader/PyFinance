import pandas as pd

from Features import Feature


class DataEngineering:

    def __init__(self, features: set[Feature]):

        self.__feature_columns = []
        self.__features = features

    def add_features(self, rates: pd.DataFrame) -> (pd.Series, pd.DataFrame):

        self.__feature_columns.clear()

        self.__add_returns(rates)

        self.__add_previous_return(rates)

        for feature in self.__features:

            rates[feature.name] = feature.compute(rates, "return t-1")
            self.__feature_columns.append(feature.name)

        rates = rates.dropna()

        returns = rates["return"]
        low_returns = rates["low_return"]
        high_returns = rates["high_return"]
        features = rates[self.__feature_columns]

        return returns, low_returns, high_returns, features

    @staticmethod
    def __add_returns(rates: pd.DataFrame):

        close = rates["close"]
        previous_close = close.shift(1)

        rates["return"] = (close - previous_close) / previous_close

        low = rates["low"]
        rates["low_return"] = (low - previous_close) / previous_close

        high = rates["high"]
        rates["high_return"] = (high - previous_close) / previous_close

    def __add_previous_return(self, rates: pd.DataFrame):

        rates["return t-1"] = rates["return"].shift(1)
        self.__feature_columns.append("return t-1")

    def __add_mean(self, rates: pd.DataFrame, column: str, period: int):

        mean_column = "mean " + str(period)
        rates[mean_column] = rates[column].rolling(period).mean()
        self.__feature_columns.append(mean_column)

    def __add_std(self, rates: pd.DataFrame, column: str, period: int):

        mean_column = "std " + str(period)
        rates[mean_column] = rates[column].rolling(period).std()
        self.__feature_columns.append(mean_column)
