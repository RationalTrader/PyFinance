import pandas as pd
import yfinance as yf

from Providers.DataProvider import DataProvider

from Timeframe import Timeframe


class YfDataProvider(DataProvider):

    def __init__(self):

        self.__timeframes = {
            Timeframe.M1: "1m",
            Timeframe.M5: "5m",
            Timeframe.M15: "15m",
            Timeframe.M30: "30m",
            Timeframe.H1: "1h",
            Timeframe.D1: "1d",
            Timeframe.W1: "1wk",
            Timeframe.MN: "1mo"
        }

    @property
    def name(self):

        return "Yahoo Finance"

    def get_symbols(self):

        pass

        # dow = si.tickers_dow()
        # nasdaq = si.tickers_nasdaq()
        # sp500 = si.tickers_sp500()
        # other = si.tickers_other()
        # ibovespa = si.tickers_ibovespa()
        # ftse100 = si.tickers_ftse100()
        # ftse250 = si.tickers_ftse250()
        # nifty50 = si.tickers_nifty50()
        # niftybank = si.tickers_niftybank()
        #
        # dow = set(dow)
        # nasdaq = set(nasdaq)
        # sp500 = set(sp500)
        # other = set(other)
        # ibovespa = set(ibovespa)
        # ftse100 = set(ftse100)
        # ftse250 = set(ftse250)
        # nifty50 = set(nifty50)
        # niftybank = set(niftybank)
        #
        # ticker_names = set.union(dow, nasdaq, sp500, other, ibovespa, ftse100, ftse250, nifty50, niftybank)
        #
        # tickers = []
        # sectors = []
        # descriptions = []
        # spreads = []
        #
        # for ticker_name in ticker_names:
        #     ticker = ticker_name
        #     sector = None
        #     description = None
        #     spread = None
        #
        #     tickers.append(ticker)
        #     sectors.append(sector)
        #     descriptions.append(description)
        #     spreads.append(spread)
        #
        # df = pd.DataFrame([tickers, sectors, descriptions, spreads], index=self._index)
        #
        # return df.transpose()

    def get_last_quote_time(self, symbol):
        raise NotImplementedError

    def get_spread(self, symbol):
        raise NotImplementedError

    def get_rates(self, symbol, timeframe, count):

        interval = self.__timeframes[timeframe]
        rates = yf.download(symbol, auto_adjust=True, interval=interval)

        if count is not None:
            rates = rates.tail(count)

        rates = rates.filter(items=["Open", "High", "Low", "Close", "Volume"])

        rates = rates.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"})

        return rates
