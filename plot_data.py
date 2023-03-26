from pandas import read_csv
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import os

from trading_signal import trading_signal_wrapper
from constants import GOLDEN_CROSS, BOLLINGER_BAND, GOLDEN_AND_BOLLINGER


def plot_moving_average(
    csv_file: str,
    products: List[str],
    windows: List[int] = [10, 50],
    num_samples: int = 9900,
):
    data = read_csv(csv_file, sep=";")
    assert num_samples <= 10000

    for product in products:
        product_data = data[data["product"].isin([product])]
        timestamps = list(range(0, len(product_data) * 100, 100))
        prices = product_data["mid_price"]

        moving_averages_dict = {}
        for window in windows:
            moving_averages = []
            for idx in range(num_samples):
                window_idx = max(idx - window, 0)
                moving_averages.append(float(np.mean(prices[window_idx:idx])))
            moving_averages_dict[window] = moving_averages

        plt.figure(figsize=(20, 10))
        plt.title(f"{product} on {csv_file}")
        plt.plot(timestamps[:num_samples], prices[:num_samples], label="Middle Price")
        for window in windows:
            moving_averages = moving_averages_dict[window]
            plt.plot(
                timestamps[:num_samples],
                moving_averages,
                label=f"Running average_{window}",
            )
        plt.xlabel("timestamps")
        plt.ylabel("prices")
        plt.legend()
        plt.show()


def plot_trading_signals(csv_file: str, products: List[str], trading_signal_type: str = BOLLINGER_BAND, is_plot_ma: bool=True):
    data = read_csv(csv_file, sep=";")
    for product in products:
        product_data = data[data["product"].isin([product])]
        timestamps = np.array(range(0, len(product_data) * 100, 100))
        prices = np.array(product_data["mid_price"])

        trading_signal = trading_signal_wrapper(trading_signal_type)
        buy_signal, sell_signal = trading_signal(prices)
        plt.figure(figsize=(20, 10))
        plt.title(f"{product} on {csv_file}")

        # Plot prices, buy signals, and sell signals
        plt.plot(timestamps, prices, 'b-', alpha=0.3, label="Middle Price")
        plt.scatter(timestamps[buy_signal], prices[buy_signal], c="red", s=30, label="Buy signal")
        plt.scatter(timestamps[sell_signal], prices[sell_signal], c="green", s=30, label="Sell signal")
        signal_idcs = np.sort(np.concatenate([buy_signal, sell_signal]))
        plt.plot(timestamps[signal_idcs], prices[signal_idcs])

        # Plot moving averages
        if is_plot_ma:
            k = 30  # Hard-coded
            moving_averages = []
            for idx in range(len(prices)):
                start_idx = max(0, idx - k + 1)
                moving_averages.append(float(np.mean(prices[start_idx: idx + 1])))
            plt.plot(timestamps, prices, 'y-', alpha=0.3, label="Moving Averages of Middle Price")

        plt.xlabel("timestamps")
        plt.ylabel("prices")
        plt.legend()
        plt.show()



if __name__ == "__main__":
    path = os.path.join("island-data-bottle-round-2", "prices_round_2_day_-1.csv")
    plot_moving_average(csv_file=path, products=["BANANAS"], windows = [30], num_samples=10000)
    plot_trading_signals(path, ["BANANAS"], trading_signal_type=GOLDEN_AND_BOLLINGER)
