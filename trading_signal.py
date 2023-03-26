from typing import List, Tuple
import numpy as np

from constants import BOLLINGER_BAND, GOLDEN_CROSS, GOLDEN_AND_BOLLINGER


def trading_signal_wrapper(signal_type: str = BOLLINGER_BAND):
    if signal_type == GOLDEN_CROSS:
        return golden_cross
    elif signal_type == BOLLINGER_BAND:
        return bollinger_band
    elif signal_type == GOLDEN_AND_BOLLINGER:
        return golden_and_bollinger
    else:
        raise NotImplementedError(f"{signal_type} is not implemented")


def golden_cross(
    prices: List[int], sma: int = 20, lma: int = 60,
) -> Tuple[np.array, np.array]:
    """
    Return the index of trading signals (Index list of buy signal, Index list of sell signal)

    :param prices: List of product prices
    :param sma: The number of timestamps on which we find short moving average
    :param lma: The number of timestamps on which we find short moving average
    :return: Index of trading signals
    """

    short_ma = []
    long_ma = []
    for idx in range(len(prices)):
        short_ma_idx = max(0, idx - sma + 1)
        short_ma.append(float(np.mean(prices[short_ma_idx : idx + 1])))

        long_ma_idx = max(0, idx - lma + 1)
        long_ma.append(float(np.mean(prices[long_ma_idx : idx + 1])))
    short_ma = np.array(short_ma)
    long_ma = np.array(long_ma)

    trend = short_ma - long_ma
    uptrend_bool_array = trend >= 0

    buy_signal = []
    sell_signal = []

    for idx in range(1, len(uptrend_bool_array)):
        if True: #uptrend_bool_array[idx] != uptrend_bool_array[idx - 1]:
            if uptrend_bool_array[idx]:  # When trend changes from downtrend to uptrend
                buy_signal.append(idx)
            else:
                sell_signal.append(idx)

    return np.array(buy_signal), np.array(sell_signal)


def bollinger_band(
    prices: List[int], ma: int = 50, k: int = 2.0,
):  # ma denotes the number of timestamps on which we calculate the moving average
    # k denotes the width of bollinger band

    prices = np.array(prices)
    moving_averages = []
    ub = []  # Upper bound of bollinger band
    lb = []  # Lower bound of bollinger band

    for idx in range(len(prices)):
        start_idx = max(0, idx - ma + 1)

        moving_average = np.mean(prices[start_idx : idx + 1])
        moving_averages.append(moving_average)
        std = np.std(prices[start_idx : idx + 1])

        ub.append(moving_average + k * std)
        lb.append(moving_average - k * std)

    buy_signal = np.where(prices <= lb)[0]
    sell_signal = np.where(prices >= ub)[0]

    return buy_signal, sell_signal


def golden_and_bollinger(prices: List[int]):
    golden_buy_signals, golden_sell_signals = golden_cross(prices)
    bollinger_buy_signals, bollinger_sell_signals = bollinger_band(prices)

    return (
        np.intersect1d(golden_buy_signals, bollinger_buy_signals),
        np.intersect1d(golden_sell_signals, bollinger_sell_signals),
    )


