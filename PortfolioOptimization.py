import numpy as np
import pandas as pd

from scipy.optimize import minimize

from Criterions import *


class PortfolioOptimization:

    def __init__(self, criterion: PortfolioCriterion):

        self.__criterion = criterion

    def optimize(self, returns: pd.DataFrame) -> np.ndarray:

        symbol_count = returns.shape[1]
        x0 = np.ones(symbol_count)
        bounds = [(0, 1) for i in range(0, symbol_count)]

        optimization = minimize(self.__criterion.compute,
                                x0,
                                args=returns,
                                method="SLSQP",
                                bounds=bounds,
                                constraints=({'type': 'eq', 'fun': lambda x: sum(abs(x)) - 1}),
                                options={'disp': True})

        return optimization.x
