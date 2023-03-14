import pandas as pd

from Providers import DataProvider


class AssetSelection:

    def __init__(self, data_provider: DataProvider):

        self.__data_provider = data_provider

        self.max_last_quote_delta = pd.Timedelta(7, "d")
        self.max_spread = 0.1 / 100

    def filter(self, symbols: list[str]) -> pd.DataFrame:

        last_quotes = []
        spreads = []

        now = pd.Timestamp.now('UTC')

        for symbol in symbols:

            last_quote = self.__data_provider.get_last_quote_time(symbol)
            last_quotes.append(last_quote)

            spread = self.__data_provider.get_spread(symbol)
            spreads.append(spread)

        features = pd.DataFrame([symbols, last_quotes, spreads])
        features = features.transpose()
        features = features.rename(columns={0: "symbol", 1: "last_quote", 2: "spread"})

        features = features.loc[lambda row: (now - features["last_quote"] < self.max_last_quote_delta) &
                                            (features["spread"] < self.max_spread)]

        return features[["symbol", "spread"]]
