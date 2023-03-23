from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
import math


"""
Utils
"""


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


# Initialize class
pearl = Pearl()


class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        position = state.position
        print(position)
        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == "BANANAS":
                ordersB: List[Order] = []

                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]

                # print(
                #     f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}"
                # )
                ordersB.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersB

            elif product == "PEARLS":
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
                    print(
                        f"current mid price: {current_mid_price}, avg mid price: {pearl.avg_price} \n"
                    )

                max_buy_volume = abs(PEARLS_POSITION_LIMITS - current_position)
                max_sell_volume = -abs(-PEARLS_POSITION_LIMITS - current_position)

                best_ask = min(best_ask, math.floor(pearl.avg_price))
                best_bid = max(best_bid, math.ceil(pearl.avg_price))

                if state.timestamp >= 1000:
                    ordersP.append(Order(product, best_ask, max_buy_volume))
                    ordersP.append(Order(product, best_bid, max_sell_volume))
                    result[product] = ordersP

                    print(
                        f"Product: {product}/ Position: {current_position}\n"
                        f"BUY at price {best_ask} with volume {max_buy_volume}\n"
                        f"Sell at price {best_bid} with volume {max_sell_volume}\n"
                    )
                    print("")

            elif product == "COCONUTS":

                ordersC: List[Order] = []

                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]

                # print(
                #     f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}"
                # )
                ordersC.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersC

            elif product == "PINA_COLADAS":

                ordersPi: List[Order] = []

                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]

                # print(
                #     f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}"
                # )
                ordersPi.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersPi

        return result
