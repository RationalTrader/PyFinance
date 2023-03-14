from Features import Feature


class Mean(Feature):

    def __init__(self, period: int):

        self.__period = period

    @property
    def name(self):

        return "mean " + str(self.__period)

    def compute(self, rates, column):

        return rates[column].rolling(self.__period).mean()
