from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

TP_list = []
SMAshort_list = [0]
SMAlong_list = [0]
EMAshort_list = [0]
EMAlong_list = [0]
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
        position = state.position
        
        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            print(position.keys())
            print(position.values())
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':
                
                ordersB: list[Order] = []
            
                order_depthB: OrderDepth = state.order_depths[product]

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]
                

                b1 = 12
                b2 = 26
                b3 = 9

                m = int(state.timestamp/100)

                TP1 = float(min(order_depthB.sell_orders.keys()) + max(order_depthB.buy_orders.keys()))/2
                TP_list1.append(TP1)

                if m>b2:
                    SMAlong1 = np.mean(TP_list1[m-b2-1:m])
                    
                else:
                    SMAlong1 = TP_list1[m-1]
                SMAlong_list1.append(SMAlong1)

                print(SMAlong1)

                if m>b1:
                    SMAshort1 = np.mean(TP_list1[m-b1-1:m])
                    
                else:
                    SMAshort1 = TP_list1[m-1]
                SMAshort_list1.append(SMAshort1)

                print(SMAshort1)
                
                k2 = 2/(b2+1)
                k1 = 2/(b1+1)

                EMAlong1 = k2*SMAlong1 + (1-k2)*EMAlong_list1[m-1]
                EMAlong_list1.append(EMAlong1)
                print(EMAlong1)

                EMAshort1 = k1*SMAshort1 + (1-k1)*EMAshort_list1[m-1]
                EMAshort_list1.append(EMAshort1)
                print(EMAshort1)

                macd1 = EMAshort1 - EMAlong1
                macd_list1.append(macd1)
                
                if m>b3:
                    macd_signal1 = np.mean(macd_list1[m-b3-1:m])
                else:
                    macd_signal1 = macd_list1[m-1]
                
                print(macd1-macd_signal1)

                if macd1 - macd_signal1 > 0:
                    LOT_SIZE = int((20 - current_position))
                    best_ask = 0.2*(min(order_depthB.sell_orders.keys())-TP1)+TP1
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersB.append(Order(product, best_ask, LOT_SIZE))

                    
                elif macd1 - macd_signal1 < 0:
                    LOT_SIZE = int((20 + current_position))
                    best_bid = TP1 - 0.2*(TP1-max(order_depthB.buy_orders.keys()))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersB.append(Order(product, best_bid, -LOT_SIZE))
                    
                    
             
                result[product] = ordersB

            # elif product == 'PEARLS':
                
            #     ordersP: list[Order] = []
                
            #     order_depth: OrderDepth = state.order_depths[product]

            #     best_ask = min(order_depth.sell_orders.keys())
            #     best_ask_volume = -2

            #     if (len(position) == 0) or (product not in position.keys()):
            #         current_position = 0
            #         position[product] = 0
            #     else:
            #         current_position = position[product]
                

            #     print(f"{product} and {current_position} BUY at price {best_ask} with volume {best_ask_volume}")
            #     ordersP.append(Order(product, best_ask, -best_ask_volume))

            #     result[product] = ordersP

            elif product == 'COCONUTS':

                ordersC: list[Order] = []

                order_depthC: OrderDepth = state.order_depths[product]

                if (len(position) == 0) or (product not in position.keys()):
                    current_position = 0
                else:
                    current_position = position[product]

                print(current_position)

                n1 = 12
                n2 = 26
                n3 = 9

                m = int(state.timestamp/100)

                TP = float(min(order_depthC.sell_orders.keys()) + max(order_depthC.buy_orders.keys()))/2
                TP_list.append(TP)

                if m>n2:
                    SMAlong = np.mean(TP_list[m-n2-1:m])
                    
                else:
                    SMAlong = TP_list[m-1]
                SMAlong_list.append(SMAlong)

                print(SMAlong)

                if m>n1:
                    SMAshort = np.mean(TP_list[m-n1-1:m])
                    
                else:
                    SMAshort = TP_list[m-1]
                SMAshort_list.append(SMAshort)

                print(SMAshort)
                
                k2 = 2/(n2+1)
                k1 = 2/(n1+1)

                EMAlong = k2*SMAlong + (1-k2)*EMAlong_list[m-1]
                EMAlong_list.append(EMAlong)
                print(EMAlong)

                EMAshort = k1*SMAshort + (1-k1)*EMAshort_list[m-1]
                EMAshort_list.append(EMAshort)
                print(EMAshort)

                macd = EMAshort - EMAlong
                macd_list.append(macd)
                
                if m>n3:
                    macd_signal = np.mean(macd_list[m-n3-1:m])
                else:
                    macd_signal = macd_list[m-1]
                
                print(macd-macd_signal)

                if macd - macd_signal > 0:
                    if current_position < -500:
                        LOT_SIZE = int((600 - current_position)/12)
                        best_ask = min(list(order_depthC.sell_orders.keys()))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))

                    else:
                        LOT_SIZE = int((600 - current_position)/7)
                        best_ask = 0.3*(min(order_depthC.sell_orders.keys())-TP)+TP
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                        print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                        ordersC.append(Order(product, best_ask, LOT_SIZE))
                    
                elif macd - macd_signal < 0:
                    LOT_SIZE = int((600 + current_position)/5)
                    best_bid = max(TP - 0.2*(TP-max(order_depthC.buy_orders.keys())), max(order_depthC.buy_orders, key=order_depthC.buy_orders.get))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersC.append(Order(product, best_bid, -LOT_SIZE))
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

                m = int(state.timestamp/100)

                TP2 = float(min(order_depthPi.sell_orders.keys()) + max(order_depthPi.buy_orders.keys()))/2
                TP_list2.append(TP2)

                if m>c2:
                    SMAlong2 = np.mean(TP_list2[m-c2-1:m])
                    
                else:
                    SMAlong2 = TP_list2[m-1]
                SMAlong_list2.append(SMAlong2)

                print(SMAlong2)

                if m>c1:
                    SMAshort2 = np.mean(TP_list2[m-c1-1:m])
                    
                else:
                    SMAshort2 = TP_list2[m-1]
                SMAshort_list2.append(SMAshort2)

                print(SMAshort2)
                
                k2 = 2/(c2+1)
                k1 = 2/(c1+1)

                EMAlong2 = k2*SMAlong2 + (1-k2)*EMAlong_list2[m-1]
                EMAlong_list2.append(EMAlong2)
                print(EMAlong2)

                EMAshort2 = k1*SMAshort2 + (1-k1)*EMAshort_list2[m-1]
                EMAshort_list2.append(EMAshort2)
                print(EMAshort2)

                macd2 = EMAshort2 - EMAlong2
                macd_list2.append(macd2)
                
                if m>c3:
                    macd_signal2 = np.mean(macd_list2[m-c3-1:m])
                else:
                    macd_signal2 = macd_list2[m-1]
                
                print(macd2-macd_signal2)

                if macd2 - macd_signal2 > 0:
                    LOT_SIZE = int((300 - current_position)/6)
                    best_ask = 0.2*(min(order_depthPi.sell_orders.keys())-TP2)+TP2
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_ask, LOT_SIZE))
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_ask, LOT_SIZE))
                    print(f"{product} and {current_position} BUY at price {best_ask} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_ask, LOT_SIZE))

                    
                elif macd2 - macd_signal2 < 0:
                    LOT_SIZE = int((300 + current_position)/6)
                    best_bid = TP2 - 0.2*(TP2-max(order_depthPi.buy_orders.keys()))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_bid, -LOT_SIZE))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_bid, -LOT_SIZE))
                    print(f"{product} and {current_position} SELL at price {best_bid} with volume {LOT_SIZE}")
                    ordersPi.append(Order(product, best_bid, -LOT_SIZE))
                    
                    
             
                result[product] = ordersPi

        return result