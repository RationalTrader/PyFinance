import numpy as np

from .PortfolioCriterion import *


class MeanVariance(PortfolioCriterion):

    def compute(self, weights, data):

        c_lambda = 3
        w = 1
        w_bar = 1 + 0.25 / 100

        weighted_returns = np.multiply(data, weights)
        total_returns = weighted_returns.sum(axis=1)

        mean = np.mean(total_returns, axis=0)
        std = np.std(total_returns, axis=0)

        criterion = w_bar ** (1 - c_lambda) / (1 + c_lambda)
        criterion += w_bar ** (-c_lambda) * w * mean
        criterion -= c_lambda / 2 * w_bar ** (-1 - c_lambda) * w ** 2 * std ** 2

        return -criterion
