import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_prices(file, n):
    df = pd.read_csv(file, sep=';')
    team = df['product'][:n].values
    plt.figure()
    for name in team:
        plt.plot(df[df['product'] == name]['mid_price'], label = name )

    plt.title('mid_prices')
    plt.legend()
    plt.show()

plot_prices('.\island-data-bottle-round-2\prices_round_2_day_1.csv', 4)
