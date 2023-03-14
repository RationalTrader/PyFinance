import MetaTrader5 as Mt5
import pandas as pd

from colorama import Fore
from datetime import datetime

from Providers.DataProvider import DataProvider
from Providers.MetaTrader import Mt5Terminal


class Mt5DataProvider(DataProvider):

    def __init__(self, terminal: Mt5Terminal):

        self.__terminal = terminal

    def get_symbols(self):

        self.__assure_initialization()

        symbols = Mt5.symbols_get()
        symbols = list(symbols)

        ticker_list = []

        for symbol in symbols:

            ticker = symbol.name
            ticker_list.append(ticker)

        return ticker_list

    def get_last_quote_time(self, symbol):

        self.__assure_initialization()

        symbol_info = Mt5.symbol_info(symbol)
        last_quote = pd.to_datetime(symbol_info.time, utc=True, unit='s')

        return last_quote

    def get_spread(self, symbol):

        self.__assure_initialization()

        tick_info = Mt5.symbol_info_tick(symbol)

        if tick_info is None:
            return None

        ask = tick_info.ask
        bid = tick_info.bid

        if bid == 0:
            return None

        return (ask - bid) / bid

    def get_rates(self, symbol, timeframe, count):

        self.__assure_initialization()

        date_from = datetime.utcnow()
        rates = Mt5.copy_rates_from(symbol, timeframe, date_from, count)

        if rates is None:

            error = Mt5.last_error()
            message = "MetaTrader error: " + str(error)
            print("\n" + Fore.RED + message)

            raise Exception(message)

        rates = pd.DataFrame(rates)
        rates["time"] = pd.to_datetime(rates["time"], unit="s")
        rates = rates.set_index("time")
        rates = rates.iloc[:len(rates) - 1]

        rates = rates.filter(items=["open", "high", "low", "close", "tick_volume"])
        rates = rates.rename(columns={"tick_volume": "volume"})

        return rates

    def __assure_initialization(self):

        if not self.__terminal.is_initialized():
            self.__terminal.initialize()
