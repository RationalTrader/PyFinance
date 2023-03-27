from DataEngineering import *
from DataPlot import DataPlot
from DataReduction import *
from DataScaling import *
from DataSet import *
from DataSplit import *
from Metrics import SharpeRatio
from Predictors import *
from Providers import *
from Timeframe import *
from UserInterface import UserInterface


class StrategyCombination:

    def __init__(self, data_provider: DataProvider, data_engineering: DataEngineering):

        self.__data_provider = data_provider
        self.__data_engineering = data_engineering

        self.__data_scaling = DataScaling()
        self.__data_reduction = DataReduction(3)

        self.timeframe = Timeframe.D1
        self.max_bar_count = 1000
        self.training_ratio = 0.7
        self.test_ratio = 0.2

    def combine(self, strategies: pd.DataFrame) -> (DataSet, DataSet, DataSet):

        all_returns = pd.DataFrame()
        all_low_returns = pd.DataFrame()
        all_high_returns = pd.DataFrame()

        for index, strategy in strategies.iterrows():

            symbol = strategy["symbol"]
            model = strategy["model"]

            is_debug = False  # symbol == "USDTRY"

            rates = self.__data_provider.get_rates(symbol, self.timeframe, self.max_bar_count)

            returns, low_returns, high_returns, features = self.__data_engineering.add_features(rates)

            symbol_data_split = DataSplit(returns, self.training_ratio, self.test_ratio)
            returns = DataSet(returns, symbol_data_split)
            features = DataSet(features, symbol_data_split)

            x = self.__data_scaling.scale(features)
            x = self.__data_reduction.reduce(x)
            y = returns

            x_train = x.training
            y_train = y.training

            x_prediction = x.all
            y_prediction = returns.all

            voting = VotingCombination(model.is_regressor)
            voting.fit(x_train, y_train)
            positions = voting.predict(x_prediction)

            predictions = positions * y_prediction
            low_predictions = np.where(positions > 0, low_returns, -high_returns)
            low_predictions = pd.Series(low_predictions, index=predictions.index)
            high_predictions = np.where(positions > 0, high_returns, -low_returns)
            high_predictions = pd.Series(high_predictions, index=predictions.index)

            if is_debug:

                rtn = returns.validation

                x_prediction = x.validation
                y_prediction = returns.validation

                prd = VotingCombination(model.is_regressor)
                prd.fit(x_train, y_train)
                p_prd = voting.predict(x_prediction)
                prd = p_prd * y_prediction

                lin = LinearModel(is_regression=False)
                lin.fit(x_train, y_train)
                p_lin = lin.predict(x_prediction)
                lin = p_lin * y_prediction

                svm = SupportVectorMachine(is_regression=False)
                svm.fit(x_train, y_train)
                p_svm = svm.predict(x_prediction)
                svm = p_svm * y_prediction

                tree = DecisionTree(is_regression=False, max_depth=6, random_state=70)
                tree.fit(x_train, y_train)
                p_tree = tree.predict(x_prediction)
                tree = p_tree * y_prediction

                ui = UserInterface()
                ui.display_periods(returns)

                sharpe = SharpeRatio()
                print()
                print("> Sharpe")
                print("returns = " + str(sharpe.compute(rtn)))
                print("predictions = " + str(sharpe.compute(prd)))
                print("linear = " + str(sharpe.compute(lin)))
                print("SVM = " + str(sharpe.compute(svm)))
                print("tree = " + str(sharpe.compute(tree)))

                plot = DataPlot()
                plot.add_plot("returns", rtn.cumsum() * 100, 'b')
                plot.add_plot("predictions", prd.cumsum() * 100, 'g')
                plot.add_plot("linear", lin.cumsum() * 100, 'r')
                plot.add_plot("SVM", svm.cumsum() * 100, 'c')
                plot.add_plot("tree", tree.cumsum() * 100, 'm')
                plot.show()

            all_returns[symbol] = predictions
            all_low_returns[symbol] = low_predictions
            all_high_returns[symbol] = high_predictions

        all_returns = all_returns.dropna()
        data_split = DataSplit(all_returns, self.training_ratio, self.test_ratio)
        all_returns = DataSet(all_returns, data_split)

        all_low_returns = all_low_returns.dropna()
        data_split = DataSplit(all_low_returns, self.training_ratio, self.test_ratio)
        all_low_returns = DataSet(all_low_returns, data_split)

        all_high_returns = all_high_returns.dropna()
        data_split = DataSplit(all_high_returns, self.training_ratio, self.test_ratio)
        all_high_returns = DataSet(all_high_returns, data_split)

        return all_returns, all_low_returns, all_high_returns
