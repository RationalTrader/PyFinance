from sklearn.preprocessing import StandardScaler

from DataSet import *


class DataScaling:

    def __init__(self):

        self.__scaler = StandardScaler()

    def scale(self, data: DataSet) -> DataSet:

        return data.transform(self.__scaler)
