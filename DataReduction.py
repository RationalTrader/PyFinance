from sklearn.decomposition import PCA

from DataSet import *


class DataReduction:

    def __init__(self, n_components: int):

        self.__pca = PCA(n_components)

    def reduce(self, data: DataSet) -> DataSet:

        return data.transform(self.__pca)
