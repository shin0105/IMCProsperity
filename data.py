import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('./island-data-bottle-round-1/island-data-bottle-round-1/prices_round_1_day_0.csv', sep=';')

df_pearls = df[df["product"]=='PEARLS']
print(df_pearls.head())
df_bananas = df[df['product']=='BANANAS']

plt.plot(df_bananas['ask_volume_1']*150, c='red')
plt.plot(df_bananas['mid_price'], c='blue')
plt.show()

