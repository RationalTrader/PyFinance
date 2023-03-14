from __future__ import annotations

import numpy as np
import pandas as pd


class DataSplit:

    def __init__(self, data: pd.DataFrame | pd.Series, training_ratio=0.70, test_ratio=0.20):

        data_count = len(data)

        self.__test_index = int(data_count * training_ratio)
        self.__validation_index = int(data_count * (training_ratio + test_ratio))

    @property
    def test_index(self) -> int:
        return self.__test_index

    @property
    def validation_index(self) -> int:
        return self.__validation_index
