import pandas as pd

from sklearn.base import *


class DataPredictor:

    def __init__(self, name: str, model):

        self.__name = name
        self.__model = model

    def __str__(self):

        return self.__name

    @property
    def name(self):

        return self.__name

    @property
    def is_regressor(self):

        return is_regressor(self.__model)

    def fit(self, x_train: pd.DataFrame, y_train: pd.DataFrame):

        if not self.is_regressor:
            y_train = np.round(y_train + 0.5)

        self.__model.fit(x_train, y_train)

    def predict(self, x_test: pd.DataFrame) -> np.ndarray:

        predictions = self.__model.predict(x_test)

        if not self.is_regressor:
            predictions = np.where(predictions == 0, -1, 1)

        # predictions = pd.DataFrame(predictions, index=x_test.index)

        return predictions
