from __future__ import annotations

import numpy as np
import pandas as pd

from DataSplit import *


class DataSet:

    def __init__(self, data: pd.DataFrame | pd.Series, split: DataSplit):

        self.__data = data
        self.__split = split

    @property
    def all(self) -> pd.DataFrame | pd.Series:
        return self.__data

    @property
    def training(self) -> pd.DataFrame | pd.Series:
        return self.__data.iloc[:self.__split.test_index]

    @property
    def test(self) -> pd.DataFrame | pd.Series:
        return self.__data.iloc[self.__split.test_index:self.__split.validation_index]

    @property
    def validation(self) -> pd.DataFrame | pd.Series:
        return self.__data.iloc[self.__split.validation_index:]

    def transform(self, transformer) -> DataSet:

        training = transformer.fit_transform(self.training)
        test = transformer.transform(self.test)
        validation = transformer.transform(self.validation)
        array = np.concatenate((training, test, validation), axis=0)
        data = pd.DataFrame(array, index=self.all.index)

        return DataSet(data, self.__split)
