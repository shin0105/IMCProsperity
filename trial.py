from datamodel import Listing, OrderDepth, Trade, TradingState
import json
from typing import Dict, List
from json import JSONEncoder

position = {
	"100": 3,
	"200": -5,
    "300": 10
}

x =max(list(position.keys()))

print(x)
print(position[x])
