from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

TP_list = []
SMAshort_list = [0]
SMAlong_list = [0]
EMAshort_list = [0]
EMAlong_list = [0]
macd_list = []


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

                # print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
                ordersP.append(Order(product, best_ask, -best_ask_volume))

                result[product] = ordersP

            elif product == 'COCONUTS':

                ordersC: list[Order] = []

                order_depth: OrderDepth = state.order_depths[product]

                if len(position) == 0:
                    current_position = 0
                else:
                    current_position = position[product]
 
                n1 = 12
                n2 = 26
                n3 = 9

                m = int(state.timestamp/100)

                TP = float(min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                TP_list.append(TP)

                if m>n2:
                    SMAlong = np.mean(TP_list[n2-m-1:n2])
                    
                else:
                    SMAlong = TP_list[m-1]
                SMAlong_list.append(SMAlong)

                if m>n2:
                    SMAshort = np.mean(TP_list[n1-m-1:n1])
                    
                else:
                    SMAshort = TP_list[m-1]
                SMAshort_list.append(SMAshort)
                
                k = 2/(n1+1)

                EMAlong = k*SMAlong + (1-k)*EMAlong_list[m-1]
                EMAlong_list.append(EMAlong)

                EMAshort = k*SMAshort + (1-k)*EMAshort_list[m-1]
                EMAshort_list.append(EMAshort)

                macd = EMAshort - EMAlong
                macd_list.append(macd)
                
                if m>n3:
                    macd_signal = np.mean(macd_list[n3-m-1:n3])
                else:
                    macd_signal = macd_list[m-1]
                
                if macd - macd_signal > 0:
                    LOT_SIZE = int((800 - current_position))
                    best_ask = 0.2*(min(order_depth.sell_orders.keys())-TP) + TP
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_ask, LOT_SIZE))
                elif macd - macd_signal < 0:
                    LOT_SIZE = int((800 + current_position))
                    best_bid = TP - 0.2*(TP-max(order_depth.buy_orders.keys()))
                    print(f"{product} and {current_position} SELL at price {best_ask} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))

             
                result[product] = ordersC

            # elif product == 'PINA_COLADAS':
                
            #     ordersPi: list[Order] = []
                
            #     order_depth: OrderDepth = state.order_depths[product]

            #     best_ask = min(order_depth.sell_orders.keys())
            #     best_ask_volume = -10

            #     # if len(position) == 0:
            #     #     current_position = 0
            #     # else:
            #     #     current_position = position[product]
                

            #     print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
            #     ordersPi.append(Order(product, best_ask, -best_ask_volume))

            #     result[product] = ordersPi

        return result