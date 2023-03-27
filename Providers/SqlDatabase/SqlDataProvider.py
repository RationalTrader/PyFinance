import sqlite3

import pandas as pd

from colorama import *

from Providers.DataProvider import DataProvider


class SqlDataProvider(DataProvider):

    def __init__(self, provider: DataProvider):

        self.__provider = provider

        self.__is_symbols_up_to_date = False
        self.__provider_symbols = []

        self.spread_delta = pd.Timedelta(60, "d")

    @property
    def name(self):

        return "SQL lite v." + sqlite3.version

    def get_symbols(self):

        self.__assure_symbols_up_to_date()

        symbols = self.__get_db_symbols()
        no_data_symbols = [symbol for symbol in symbols if symbol not in self.__provider_symbols]

        if no_data_symbols:

            message = "No data for " + str(len(no_data_symbols)) + " symbols from " + self.__provider.name
            print("\n" + Fore.RED + message)
            print(no_data_symbols)
            print(Style.RESET_ALL)

        return symbols

    def get_last_quote_time(self, symbol):

        self.__assure_symbols_up_to_date()

        if symbol in self.__provider_symbols:

            last_quote = self.__provider.get_last_quote_time(symbol)
            self.__set_db_last_quote_time(symbol, last_quote)

        else:

            last_quote = self.__get_db_last_quote_time(symbol)

        return last_quote

    def get_spread(self, symbol):

        is_up_to_date = False
        now = pd.Timestamp.now('UTC')
        last_spread_update = self.__get_db_last_spread_update(symbol)

        if last_spread_update is not None:

            delta = now - last_spread_update

            if delta < self.spread_delta:

                is_up_to_date = True

        if is_up_to_date:

            spread = self.__get_db_spread(symbol)

        else:

            spread = self.__provider.get_spread(symbol)
            self.__set_db_spread(symbol, spread)
            self.__set_db_last_spread_update(symbol, now)

        return spread

    def get_rates(self, symbol, timeframe, count):

        return self.__provider.get_rates(symbol, timeframe, count)

    def shutdown(self):

        self.__provider.shutdown()

    def __assure_initialization(self):

        self.__connection = sqlite3.connect("cache.db")

        sql_create_symbols = """ CREATE TABLE IF NOT EXISTS symbols (
            symbol text PRIMARY KEY, 
            last_quote text, 
            spread real,
            spread_update text); """

        self.__connection.execute(sql_create_symbols)

    def __assure_symbols_up_to_date(self):

        if self.__is_symbols_up_to_date:

            return

        self.__assure_initialization()

        self.__provider_symbols = self.__provider.get_symbols()
        self.__set_db_symbols(self.__provider_symbols)

        self.__is_symbols_up_to_date = True

    def __get_db_symbols(self) -> list[str]:

        cursor = self.__connection.cursor()
        sql_get_symbols = """ SELECT symbol FROM symbols """
        cursor.execute(sql_get_symbols)
        db_symbols = cursor.fetchall()
        db_symbols = [symbol for row in db_symbols for symbol in row]

        return db_symbols

    def __set_db_symbols(self, symbols: list[str]) -> None:

        sql_add_row = """ INSERT OR IGNORE INTO symbols(symbol) VALUES(?) """
        cursor = self.__connection.cursor()
        cursor.executemany(sql_add_row, zip(symbols))
        self.__connection.commit()

    def __get_db_last_quote_time(self, symbol: str) -> None | pd.Timestamp:

        sql_get_last_quote = """ SELECT last_quote FROM symbols WHERE symbol=? """
        cursor = self.__connection.cursor()
        cursor.execute(sql_get_last_quote, (symbol,))
        last_quote = cursor.fetchone()
        last_quote = last_quote[0]

        if not last_quote:

            return None

        last_quote = pd.to_datetime(last_quote, utc=True)

        return last_quote

    def __set_db_last_quote_time(self, symbol: str, last_quote: pd.Timestamp) -> None:

        sql_set_last_quote = """ UPDATE symbols SET last_quote=? WHERE symbol=? """
        cursor = self.__connection.cursor()
        last_quote = last_quote.strftime('%Y-%m-%d %X')
        cursor.execute(sql_set_last_quote, (last_quote, symbol))
        self.__connection.commit()

    def __get_db_last_spread_update(self, symbol: str) -> None | pd.Timestamp:

        sql_get_last_spread_update = """ SELECT spread_update FROM symbols WHERE symbol=? """
        cursor = self.__connection.cursor()
        cursor.execute(sql_get_last_spread_update, (symbol,))
        last_update = cursor.fetchone()
        last_update = last_update[0]

        if not last_update:

            return None

        last_update = pd.to_datetime(last_update, utc=True)

        return last_update

    def __set_db_last_spread_update(self, symbol: str, last_update: pd.Timestamp):

        sql_set_last_spread_update = """ UPDATE symbols SET spread_update=? WHERE symbol=? """
        cursor = self.__connection.cursor()
        last_update = last_update.strftime('%Y-%m-%d %X')
        cursor.execute(sql_set_last_spread_update, (last_update, symbol))
        self.__connection.commit()

    def __get_db_spread(self, symbol: str) -> float:

        sql_get_spread = """ SELECT spread FROM symbols WHERE symbol=? """
        cursor = self.__connection.cursor()
        cursor.execute(sql_get_spread, (symbol,))
        spread = cursor.fetchone()
        spread = spread[0]

        return spread

    def __set_db_spread(self, symbol: str, spread: float) -> None:

        sql_set_spread = """ UPDATE symbols SET spread=? WHERE symbol=? """
        cursor = self.__connection.cursor()
        cursor.execute(sql_set_spread, (spread, symbol))
        self.__connection.commit()
