from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

position_limit = []
TP_list = []

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                bid_volume_sum = np.sum(list(order_depth.buy_orders.values()))
                ask_volume_sum = np.sum(list(order_depth.sell_orders.values()))

                current_position =list(state.position.values())

                if len(current_position) == 0:
                    current_position.append(0)

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                #acceptable_price = 1

                if bid_volume_sum > ask_volume_sum and current_position[0] < 20:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = 20 - current_position[0]
                    print("BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, best_ask_volume))

                elif ask_volume_sum > bid_volume_sum and current_position[0] > -20:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = 20 + current_position[0]
                    print("SELL", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_volume))


                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result