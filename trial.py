from datamodel import Listing, OrderDepth, Trade, TradingState
import json
from typing import Dict, List
from json import JSONEncoder
import numpy as np

position = {
	"100": 3,
	"200": -5,
    "300": 10
}

x =max(list(position.keys()))

print(x)
print(position[x])

a={1:2, 3:4}
print(a[3])

b=[1,1,1,1]
print(np.std(b))