from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:

    def __init__(self):
        self.daily_prices = dict()
        self.one_day = 10
        self.k = 0.5

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}
        k = self.k
        one_day = self.one_day

        for product in state.order_depths.keys():

            if product == 'BANANAS':
                
                seq = state.timestamp/100
                current_day = seq // one_day

                if seq % one_day == 0:  # at the start of the day
                    bid_prices = state.order_depths[product].buy_orders.keys()
                    ask_prices = state.order_depths[product].sell_orders.keys()
                    mid_price = (bid_prices[0] + ask_prices[0])/2
                    self.daily_prices['start of %d' % current_day] = mid_price
                    
                elif seq % one_day == one_day - 1:  # at the end of the day
                    bid_prices = state.order_depths[product].buy_orders.keys()
                    ask_prices = state.order_depths[product].sell_orders.keys()
                    mid_price = (bid_prices[0] + ask_prices[0])/2
                    self.daily_prices['end of %d' % current_day] = mid_price

                if current_day == 0:
                    return {}  # do nothing in the first day

                else:
                    
                     delta = self.daily_prices['end of %d' % current_day-1] - self.daily_prices['start of %d' % current_day-1]
                     bid_prices = state.order_depths[product].buy_orders.keys()
                     ask_prices = state.order_depths[product].sell_orders.keys()
                     mid_price = (bid_prices[0] + ask_prices[0])/2

                     buy_condition = mid_price > self.daily_prices['start of %d' % current_day] + k * delta

                     if buy_condition:
                        orders: list[Order] = []
                        order_depth: OrderDepth = state.order_depths[product]
                        best_ask = min(order_depth.buy_orders.keys())
                        best_ask_volume = order_depth.buy_orders[best_ask]
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        print("BUY", str(-best_ask_volume) + "x", best_ask)

                result[product] = orders
                return result