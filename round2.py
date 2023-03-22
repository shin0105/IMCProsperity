from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        position = state.position
        #print(current_position)
        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':
                
                ordersB: list[Order] = []
            
                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]
                

                print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
                ordersB.append(Order(product, best_ask, -best_ask_volume))
                result[product] = ordersB

            elif product == 'PEARLS':
                
                ordersP: list[Order] = []
                
                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]
                

                print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
                ordersP.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersP

            elif product == 'COCONUTS':

                ordersC: list[Order] = []

                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]
                

                print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
                ordersC.append(Order(product, best_ask, -best_ask_volume))
             
                result[product] = ordersC

            elif product == 'PINA_COLADAS':
                
                ordersPi: list[Order] = []
                
                order_depth: OrderDepth = state.order_depths[product]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = -10

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]
                

                print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
                ordersPi.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersPi

        return result