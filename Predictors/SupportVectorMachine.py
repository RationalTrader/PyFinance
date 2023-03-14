from sklearn.svm import SVC
from sklearn.svm import SVR

from .DataPredictor import *


class SupportVectorMachine(DataPredictor):

    def __init__(self, is_regression=False):

        if is_regression:
            name = "SVR"
            model = SVR()
        else:
            name = "SVC"
            model = SVC(C=1.5)

        super().__init__(name, model)
