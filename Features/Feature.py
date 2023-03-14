import pandas as pd


class Feature:

    @property
    def name(self) -> str:
        raise NotImplementedError

    def compute(self, rates: pd.DataFrame, column: str):
        raise NotImplementedError
