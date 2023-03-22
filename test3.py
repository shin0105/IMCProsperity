from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

position_limit = []
last_buy =[0]
last_sell =[0]
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
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                current_position =list(state.position.values())

                if len(current_position) == 0:
                    current_position.append(0)
                    
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                TP = float(min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                TP_list.append(TP)
                n = int(state.timestamp/100)
                m=30
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

                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]

                if current_position[0] ==0:
                    if TP > UB:
                        print("BANANAS" "SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        last_sell.append(best_bid)
                        last_sell.pop(0)
                    elif TP < LB:
                        print("BANANAS" "BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))
                        last_buy.append(best_ask)
                        last_buy.pop(0)
              
                if last_buy[0] < best_bid and current_position[0] >0:
                    print("BANANAS" "SELL", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_volume))
                    last_sell.append(best_bid)
                    last_sell.pop(0)
                    
                if last_sell[0] > best_ask and current_position[0] <0:
                    print("BANANAS" "BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_volume))
                    last_buy.append(best_ask)
                    last_buy.pop(0)

                print(f'lastbuy {last_buy[0]} lastsell {last_sell[0]} position {current_position[0]}')
                # Add all the above orders to the result dict
                result[product] = orders
            else:
                print('PEARLS')
        return result
    
    