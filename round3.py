from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
import math


def get_mid_price(orders: dict, is_weighted: bool = False):
    mid_price = 0
    num_quantities = 0
    prices = list(orders.keys())
    quantities = list(orders.values())
    for idx in range(len(orders)):
        if is_weighted:
            mid_price += prices[idx] * abs(quantities[idx])
            num_quantities += abs(quantities[idx])
        else:
            mid_price += prices[idx]
            num_quantities += 1

    mid_price /= num_quantities

    return mid_price


"""
Constants
"""
# Position Limits
PEARLS_POSITION_LIMITS = 19
BANANAS_POSITION_LIMITS = 20
COCONUT_POSITION_LIMITS = 600
PINA_POSITION_LIMITS = 800

"""
Product classes
"""


class Pearl:
    def __init__(self):
        self.avg_price = 0
        self.sum_price = 0
        self.time_step = 0

    def update_avg_price(self, price):
        self.sum_price += price
        self.time_step += 1
        self.avg_price = self.sum_price / self.time_step

class Banana:
    def __init__(self):
        self.prices_last_30 = []
        self.moving_average_5 = 0
        self.moving_average_30 = 0
        self.position = 0  # Neutral: 0/ Should buy: -1/ Should sell: +1

    def update_prices_last_30(self, price):
        self.prices_last_30.append(price)
        if len(self.prices_last_30) > 30:
            self.prices_last_30.pop(0)

    def update_moving_average(self):
        assert len(self.prices_last_30) == 30
        self.moving_average_5 = np.mean(self.prices_last_30[-5:])
        self.moving_average_30 = np.mean(self.prices_last_30)

    def optimal_position(self):
        # Neutral: 0/ Should buy: -1/ Should sell: +1
        if (self.position == -1) and (self.moving_average_5 < self.moving_average_30):
            self.position = + 1
            return self.position

        if (self.position == +1) and (self.moving_average_5 > self.moving_average_30):
            self.position = -1
            return self.position

        if self.position == 0:
            if self.moving_average_5 > self.moving_average_30:
                self.position = -1
                return self.position
            else:
                self.position = 1
                return self.position

def find_SMA(n, m, TP, TP_list):
    if m>n:
        SMA = np.mean(TP_list[m-n-1:m])
                    
    else:
        SMA = TP
    return SMA

def bollinger_band(n, m, SMA, TP_list, d):
    if m>n:
        UB = SMA + d*np.std(TP_list[m-n-1:m])
        LB = SMA - d*np.std(TP_list[m-n-1:m])
    else:
        SMA = TP_list[m]
        UB = SMA + d*np.std(TP_list)
        LB = SMA - d*np.std(TP_list)
    return UB, LB


# Initialize class
pearl = Pearl()
banana = Banana()

prev_position = 0

TP_listC = []

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        position = state.position
        print()
       

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            print(position.keys())
            print(position.values())
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                ordersP: List[Order] = []
                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]

                order_depth: OrderDepth = state.order_depths[product]

                # Main trading algorithm
                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                if (len(order_depth.sell_orders) > 0) and (
                        len(order_depth.buy_orders) > 0
                ):
                    current_mid_price = 1 / 2 * (best_ask + best_bid)
                    pearl.update_avg_price(current_mid_price)
                    # print(
                    #     f"current mid price: {current_mid_price}, avg mid price: {pearl.avg_price} \n"
                    # )

                max_buy_volume = abs(PEARLS_POSITION_LIMITS - current_position)
                max_sell_volume = -abs(-PEARLS_POSITION_LIMITS - current_position)

                best_ask = min(best_ask, math.floor(pearl.avg_price))
                best_bid = max(best_bid, math.ceil(pearl.avg_price))

                if state.timestamp >= 1000:
                    ordersP.append(Order(product, best_ask, max_buy_volume))
                    ordersP.append(Order(product, best_bid, max_sell_volume))
                    result[product] = ordersP

                    # print(
                    #     f"Product: {product}/ Position: {current_position}\n"
                    #     f"BUY at price {best_ask} with volume {max_buy_volume}\n"
                    #     f"Sell at price {best_bid} with volume {max_sell_volume}\n"
                    # )
                    # print("")

            elif product == 'BANANAS':
                ordersB: List[Order] = []

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]

                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                mid_price = (best_ask + best_bid) / 2
                max_buy_volume = abs(PEARLS_POSITION_LIMITS - current_position)
                max_sell_volume = -abs(-PEARLS_POSITION_LIMITS - current_position)

                banana.update_prices_last_30(mid_price)

                if state.timestamp > 3000:
                    banana.update_moving_average()
                    acceptable_price = banana.moving_average_5

                    ci = np.std(banana.prices_last_30) / math.sqrt(30)

                    best_ask = int(min(best_ask, acceptable_price - 3 * ci))
                    best_bid = int(max(best_bid, acceptable_price + 3 * ci))

                    ordersB.append(Order(product, best_ask, max_buy_volume))
                    ordersB.append(Order(product, best_bid, max_sell_volume))
                    result[product] = ordersB

                    # print(
                    #     f"\nProduct: {product}/ Position: {current_position}\n"
                    #     f"BUY at price {best_ask} with volume {max_buy_volume}\n"
                    #     f"Sell at price {best_bid} with volume {max_sell_volume}\n"
                    # )
                result[product] = ordersB

            elif product == 'COCONUTS':

                ordersC: list[Order] = []

                order_depthC: OrderDepth = state.order_depths[product]

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]
                
                TPC = float(min(order_depthC.sell_orders.keys()) + max(order_depthC.buy_orders.keys()))/2
                TP_listC.append(TPC)

                n = 20
                m = int(state.timestamp/100)
                print(f"current time is {m}")

                SMAC = find_SMA(n, m, TPC, TP_listC)

                UB, LB = bollinger_band(n, m, SMAC, TP_listC, 1.7)

                print(f"{product} TP: {TPC} UB: {UB} LB: {LB}")

                if TPC > UB:
                    LOT_SIZE = int((600 + current_position))
                    best_bid =  max(TPC - 0.2*(TPC-max(order_depthC.buy_orders.keys())), max(order_depthC.buy_orders, key=order_depthC.buy_orders.get))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))
                    
                elif TPC < LB:
                    LOT_SIZE = int((600 - current_position))
                    best_ask = int(min(min(order_depthC.sell_orders.keys()), 0.4*(min(order_depthC.buy_orders.keys())-TPC)+TPC))
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_ask, LOT_SIZE))
                    
             
                result[product] = ordersC

            # elif product == 'PINA_COLADAS':

            #     ordersPi: list[Order] = []

            #     order_depthPi: OrderDepth = state.order_depths[product]

            #     if (len(position) == 0) or (product not in position.keys()):
            #         current_position = 0
            #     else:
            #         current_position = position[product]

            #     c1 = 12
            #     c2 = 26
            #     c3 = 9

            #     m = int(state.timestamp / 100)

            #     TP2 = float(min(order_depthPi.sell_orders.keys()) + max(order_depthPi.buy_orders.keys())) / 2
            #     TP_list2.append(TP2)

            #     if m > c2:
            #         SMAlong2 = np.mean(TP_list2[m - c2 - 1:m])
            #     else:
            #         SMAlong2 = TP2

            #     SMAlong_list2.append(SMAlong2)

            #     #print(SMAlong2)

            #     if m > c1:
            #         SMAshort2 = np.mean(TP_list2[m - c1 - 1:m])

            #     else:
            #         SMAshort2 = TP2
            #     SMAshort_list2.append(SMAshort2)

            #     #print(SMAshort2)

            #     k2 = 2 / (c2 + 1)
            #     k1 = 2 / (c1 + 1)

            #     EMAlong2 = k2 * SMAlong2 + (1 - k2) * EMAlong_list2[m - 1]
            #     EMAlong_list2.append(EMAlong2)
            #     #print(EMAlong2)

            #     EMAshort2 = k1 * SMAshort2 + (1 - k1) * EMAshort_list2[m - 1]
            #     EMAshort_list2.append(EMAshort2)
            #     #print(EMAshort2)

            #     macd2 = EMAshort2 - EMAlong2
            #     macd_list2.append(macd2)

            #     if m > c3:
            #         macd_signal2 = np.mean(macd_list2[m - c3 - 1:m])
            #     else:
            #         macd_signal2 = macd_list2[m - 1]

            #     s2 = macd2 - macd_signal2

           
            #     print(f"TPPi {TP2} signal {s2} EMAshort {EMAshort2} EMAlong {EMAlong2} macd_signal {macd_signal2}")

            #     price_adjustment2 = np.std(SMAlong_list2[m-c2-1:m]) / math.sqrt(26)
            #     acceptable_price2 = TP2

            #     if macd2 - macd_signal2 > 0:
            #         LOT_SIZE = int((300 - current_position))
            #         best_ask = int(min(min(order_depthPi.sell_orders.keys()), acceptable_price2 + 3.3 * price_adjustment2))
            #         print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
            #         ordersPi.append(Order(product, best_ask, LOT_SIZE))

                    
            #     elif macd2 - macd_signal2 < 0:
            #         LOT_SIZE = int((300 + current_position))
            #         best_bid = int(max(max(order_depthPi.buy_orders.keys()), acceptable_price2 - 3 * price_adjustment2))
            #         print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
            #         ordersPi.append(Order(product, best_bid, -LOT_SIZE))

            #     result[product] = ordersPi

        return result