from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
import math

position_limit = []
last_buy =[0]
last_sell =[0]
TP_list = []

TP_list = []
SMAshort_list = []
SMAlong_list = []
EMAshort_list = [1142]
EMAlong_list = [592.5]
macd_list = []

TP_list1 = []
SMAshort_list1 = [0]
SMAlong_list1 = [0]
EMAshort_list1 = [0]
EMAlong_list1 = [0]
macd_list1 = []

TP_list2 = []
SMAshort_list2 = [0]
SMAlong_list2 = [0]
EMAshort_list2 = [0]
EMAlong_list2 = [0]
macd_list2 = []


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
            position = state.position
            # Check if the current product is the 'PEARLS' product, only then run the order logic
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
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        last_sell.append(best_bid)
                        last_sell.pop(0)
                    elif TP < LB:
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))
                        last_buy.append(best_ask)
                        last_buy.pop(0)
              
                if last_buy[0] < best_bid and current_position[0] >0:
                    print("SELL", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_volume))
                    last_sell.append(best_bid)
                    last_sell.pop(0)
                    
                if last_sell[0] > best_ask and current_position[0] <0:
                    print("BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_volume))
                    last_buy.append(best_ask)
                    last_buy.pop(0)

                print(f'lastbuy {last_buy[0]} lastsell {last_sell[0]} position {current_position[0]}')
                # Add all the above orders to the result dict
                result[product] = orders

            elif product == 'COCONUTS':

                ordersC: list[Order] = []

                order_depthC: OrderDepth = state.order_depths[product]

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]

    

                n1 = 12
                n2 = 26
                n3 = 9

                m = int(state.timestamp/100)

                TP = float(min(order_depthC.sell_orders.keys()) + max(order_depthC.buy_orders.keys()))/2
                TP_list.append(TP)

                if m>n2:
                    SMAlong = np.mean(TP_list[m-n2-1:m])
                else:
                    SMAlong = TP

                SMAlong_list.append(SMAlong)

                

                if m>n1:
                    SMAshort = np.mean(TP_list[m-n1-1:m])
                    
                else:
                    SMAshort = TP

                SMAshort_list.append(SMAshort)

                
                k2 = 2/(n2+1)
                k1 = 2/(n1+1)

                EMAlong = k2*SMAlong + (1-k2)*EMAlong_list[m]
                EMAlong_list.append(EMAlong)
       

                EMAshort = k1*SMAshort + (1-k1)*EMAshort_list[m]
                EMAshort_list.append(EMAshort)


                macd = EMAshort - EMAlong
                macd_list.append(macd)
                
                if m>n3:
                    macd_signal = np.mean(macd_list[m-n3-1:m])
                else:
                    macd_signal = macd_list[m]
                
                s1 = macd - macd_signal
                print(f"TPC {TP} signal {s1} EMAshort {EMAshort} EMAlong {EMAlong} macd_signal {macd_signal}")

                price_adjustment = np.std(SMAlong_list[m-n2-1:m]) / math.sqrt(26)
                acceptable_price = TP


                if macd - macd_signal > 0:
                    # if current_position < -500:
                    #     LOT_SIZE = int((600 - current_position)/20)
                    #     best_ask = min(order_depth.sell_orders.keys()) + 3*price_adjustment #int(min(min(order_depth.sell_orders.keys()), acceptable_price + 3 * price_adjustment))
                    #     print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    #     ordersC.append(Order(product, best_ask, LOT_SIZE))
                    #     print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    #     ordersC.append(Order(product, best_ask, LOT_SIZE))
                    #     print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    #     ordersC.append(Order(product, best_ask, LOT_SIZE))

                    # else:
                    LOT_SIZE = int((600 - current_position))
                    best_ask = int(min(min(order_depthC.sell_orders.keys()), acceptable_price + 3.4 * price_adjustment))
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_ask, LOT_SIZE))
                    
                elif macd - macd_signal < 0:
                    LOT_SIZE = int((600 + current_position))
                    best_bid =  max(TP - 0.2*(TP-max(order_depthC.buy_orders.keys())), max(order_depthC.buy_orders, key=order_depthC.buy_orders.get))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))
                    
             
                result[product] = ordersC

            elif product == 'PINA_COLADAS':

                ordersPi: list[Order] = []

                order_depthPi: OrderDepth = state.order_depths[product]

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]

                c1 = 12
                c2 = 26
                c3 = 9

                m = int(state.timestamp / 100)

                TP2 = float(min(order_depthPi.sell_orders.keys()) + max(order_depthPi.buy_orders.keys())) / 2
                TP_list2.append(TP2)

                if m > c2:
                    SMAlong2 = np.mean(TP_list2[m - c2 - 1:m])
                else:
                    SMAlong2 = TP2

                SMAlong_list2.append(SMAlong2)

                #print(SMAlong2)

                if m > c1:
                    SMAshort2 = np.mean(TP_list2[m - c1 - 1:m])

                else:
                    SMAshort2 = TP2
                SMAshort_list2.append(SMAshort2)

                #print(SMAshort2)

                k2 = 2 / (c2 + 1)
                k1 = 2 / (c1 + 1)

                EMAlong2 = k2 * SMAlong2 + (1 - k2) * EMAlong_list2[m - 1]
                EMAlong_list2.append(EMAlong2)
                #print(EMAlong2)

                EMAshort2 = k1 * SMAshort2 + (1 - k1) * EMAshort_list2[m - 1]
                EMAshort_list2.append(EMAshort2)
                #print(EMAshort2)

                macd2 = EMAshort2 - EMAlong2
                macd_list2.append(macd2)

                if m > c3:
                    macd_signal2 = np.mean(macd_list2[m - c3 - 1:m])
                else:
                    macd_signal2 = macd_list2[m - 1]

                s2 = macd2 - macd_signal2

           
                print(f"TPPi {TP2} signal {s2} EMAshort {EMAshort2} EMAlong {EMAlong2} macd_signal {macd_signal2}")

                price_adjustment2 = np.std(SMAlong_list2[m-c2-1:m]) / math.sqrt(26)
                acceptable_price2 = TP2

                if macd2 - macd_signal2 > 0:
                    LOT_SIZE = int((300 - current_position))
                    best_ask = int(min(min(order_depthPi.sell_orders.keys()), acceptable_price2 + 3.3 * price_adjustment2))
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_ask, LOT_SIZE))

                    
                elif macd2 - macd_signal2 < 0:
                    LOT_SIZE = int((300 + current_position))
                    best_bid = int(max(max(order_depthPi.buy_orders.keys()), acceptable_price2 - 3 * price_adjustment2))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_bid, -LOT_SIZE))

                result[product] = ordersPi

        return result