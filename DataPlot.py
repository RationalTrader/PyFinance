import pandas as pd
from matplotlib import pyplot as plt


class DataPlot:

    def __init__(self, title="Return", x_label="Time", y_label="Percentage"):

        self.__legend = []

        plt.style.use('seaborn-v0_8')
        font = {'weight': 'bold', "size": "300"}
        plt.rc('font', **font)
        plt.figure(figsize=(15, 8))
        plt.xticks(size=15, fontweight="bold")
        plt.yticks(size=15, fontweight="bold")

        plt.title(title, size=15)
        plt.xlabel(x_label, size=15)
        plt.ylabel(y_label, size=15)

    def add_plot(self, name: str, values: pd.Series, color='b', width=1):

        self.__legend.append(name)
        plt.plot(values, color=color, linewidth=width)

    def show(self):

        plt.legend(self.__legend)
        plt.show()
