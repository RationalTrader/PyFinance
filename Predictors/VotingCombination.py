from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import VotingRegressor

from .DataPredictor import *


class VotingCombination(DataPredictor):

    def __init__(self, is_regression=False):

        if is_regression:
            name = "VotReg"
            tree = DecisionTreeRegressor(max_depth=6, random_state=70)
            svr = SVR(epsilon=1.5)
            lin = LinearRegression()
            model = VotingRegressor(estimators=[('lr', lin), ("tree", tree), ("svr", svr)])
        else:
            name = "VotCla"
            tree = DecisionTreeClassifier(max_depth=6, random_state=70)
            svr = SVC()
            lin = LogisticRegression()
            model = VotingClassifier(estimators=[('lr', lin), ("tree", tree), ("svr", svr)])

        super().__init__(name, model)
