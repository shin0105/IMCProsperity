from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

position_limit = []
SMA_list = []

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

                TP = float(min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                TP_list.append(TP)
                n = int(state.timestamp/100)
                m=50
                d = 2
            
                if n>m:
                    SMA = np.mean(TP_list[n-m-1:n])
                    UB = SMA + d*np.std(TP_list[n-m-1:n])
                    MB = np.sum(TP_list[n-m-1:n])/m
                    LB = SMA - d*np.std(TP_list[n-m-1:n])
                    
                else:
                    SMA = TP_list[n-1]
                    UB = SMA + d*np.std(TP_list)
                    MB = TP_list[n-1]
                    LB = SMA - d*np.std(TP_list)

                current_position =list(state.position.values())

                if len(current_position) == 0:
                    current_position.append(0)

                print(f'TP {TP} UB {UB} LB {LB} MB {MB} and position {current_position[0]}')
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                #acceptable_price = 1

                if TP > UB and current_position[0] > -20:
                    # best_index1 = np.argmax(list(order_depth.buy_orders.values()))
                    # best_bid = list(order_depth.buy_orders.keys())[best_index1]
                    # bid_volume = 20 + current_position[0]
                    # print("SELL", str(bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -bid_volume))
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = 20 + current_position[0]
                    print("SELL", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_volume))
                elif TP < LB and current_position[0] < 20:
                    # best_index2 = np.argmax(list(order_depth.sell_orders.values()))
                    # best_ask = list(order_depth.sell_orders.keys())[best_index2]
                    # ask_volume = 20 - current_position[0]
                    # print("BUY", str(ask_volume) + "x", best_ask)
                    # orders.append(Order(product, best_ask, ask_volume))
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = 20 - current_position[0]
                    print("BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, best_ask_volume))



                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result