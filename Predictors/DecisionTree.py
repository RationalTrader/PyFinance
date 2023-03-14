from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

from .DataPredictor import *


class DecisionTree(DataPredictor):

    def __init__(self, is_regression=False, max_depth=6, random_state=70):

        if is_regression:
            name = "TreeReg"
            model = DecisionTreeRegressor(max_depth=max_depth, random_state=random_state)
        else:
            name = "TreeCla"
            model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)

        super().__init__(name, model)
