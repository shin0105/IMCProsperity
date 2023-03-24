import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show_signal(logfile):
    signal2 = []
    signal1 = []
    with open(logfile) as f:
            for line in f.readlines():
                words = line.split(' ')
                if 'signal2' in words:
                    pin_idx = words.index('signal2') + 1
                    signal2.append(float(words[pin_idx]))
                if 'signal1' in words:
                    co_idx = words.index('signal1') + 1
                    signal1.append(float(words[co_idx]))
            
    signal1 = np.array(signal1)
    signal2 = np.array(signal2)
    return signal1, signal2

def plot_prices(file, n):
    df = pd.read_csv(file, sep=';')
    team = df['product'][:n].values
    plt.figure()
    for name in team:
        plt.plot(df[df['product'] == name]['mid_price'], label = name )

    plt.title('mid_prices')
    plt.legend()
    plt.show()
    return df
     

signal1, signal2 = show_signal('.\simulation_round2.log')
df = pd.read_csv('.\simulation_round2.csv', sep=';')

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('POL', color=color)
ax1.plot(df[df['product'] == 'PINACOLADA']['timestamp'], df[df['product'] == 'PINACOLADA']['profit_and_loss'], color=color)
#ax1.set_ylim(7940, 8120)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('PINACOLADA', color=color)  # we already handled the x-label with ax1
ax2.plot(df[df['product'] == 'PINA_COLADAS']['timestamp'], df[df['product'] == 'PINA_COLADAS']['mid_price'], color=color)
ax2.set_ylim(14800, 15300)
ax2.tick_params(axis='y', labelcolor=color)

ax3 = ax1.twinx() 

color = 'tab:red'
ax3.set_ylabel('PINACOLADA signal', color=color)  # we already handled the x-label with ax1
ax3.plot(df[df['product'] == 'PINA_COLADAS']['timestamp'], signal2, color=color)
ax3.axhline(y=0,c='black')
ax3.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

    
