import MetaTrader5 as Mt5


class Mt5Terminal:

    def __init__(self):

        self.__is_initialized = False

    def is_initialized(self) -> bool:

        return self.__is_initialized

    def initialize(self) -> None:

        if not self.__is_initialized:
            self.__is_initialized = Mt5.initialize()

        if not self.__is_initialized:
            error = Mt5.last_error()
            raise Exception("MetaTrader initialization failed: " + str(error))

    def shutdown(self) -> None:

        if self.is_initialized:
            Mt5.shutdown()
            self.__is_initialized = False
