import MetaTrader5 as Mt5

from enum import IntEnum


class Timeframe(IntEnum):
    M1 = Mt5.TIMEFRAME_M1
    M5 = Mt5.TIMEFRAME_M5
    M15 = Mt5.TIMEFRAME_M15
    M30 = Mt5.TIMEFRAME_M30
    H1 = Mt5.TIMEFRAME_H1
    H4 = Mt5.TIMEFRAME_H4
    D1 = Mt5.TIMEFRAME_D1
    W1 = Mt5.TIMEFRAME_W1
    MN = Mt5.TIMEFRAME_MN1
