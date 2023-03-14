from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

from .DataPredictor import *


class LinearModel(DataPredictor):

    def __init__(self, is_regression=False):

        if is_regression:
            name = "LinReg"
            model = LinearRegression()
        else:
            name = "LogReg"
            model = LogisticRegression()

        super().__init__(name, model)
