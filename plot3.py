import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('bollinger.csv', sep=';')

time = df[df['product']=='COCONUTS']['timestamp']
price = df[df['product']=='COCONUTS']['mid_price']
profit = df[df['product']=='COCONUTS']['profit_and_loss']

def show_signal(logfile):
    UB = []
    LB = []
    max_bid = []
    min_ask = []
    with open(logfile) as f:
            for line in f.readlines():
                words = line.split(' ')
                if 'UB' in words:
                    ub_idx = words.index('UB') + 2
                    UB.append(float(words[ub_idx]))
                if 'UB' in words:
                    lb_idx = words.index('UB') + 5
                    LB.append(float(words[lb_idx]))
                if 'UB' in words:
                    min_idx = words.index('min_ask') + 2
                    min_ask.append(float(words[min_idx]))
                if 'UB' in words:
                    max_idx = words.index('max_bid') + 2
                    max_bid.append(float(words[max_idx]))
            
    UB = np.array(UB)
    LB = np.array(LB)
    max_bid = np.array(max_bid)
    min_ask = np.array(min_ask)
    return UB, LB, max_bid, min_ask

UB, LB, max_bid, min_ask = show_signal('bollinger.log')

print(UB.shape)
print(time.shape)
print(LB.shape)

fig, ax1 = plt.subplots()

color = 'tab:green'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('POL', color=color)
ax1.plot(time, profit, color=color)
#ax1.set_ylim(0, 10000)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('price', color=color)  # we already handled the x-label with ax1
ax2.plot(time, price, color=color)
ax2.plot(time, UB, color = 'red')
ax2.plot(time, LB, color = 'orange')
ax2.plot(time, min_ask, color = 'cyan')
ax2.plot(time, max_bid, color = 'purple')
#ax2.set_ylim(14500, 15000)
ax2.tick_params(axis='y', labelcolor=color)

plt.show()