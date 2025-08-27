import pandas as pd
from datetime import datetime
from orders import Order
from indicators.utils import Candle

    
class History:
    def __init__(self, candlesticks: list[Candle], ma10 : list[float], ma20: list[float]):
        self.candlesticks = candlesticks
        self.ma10 = ma10
        self.ma20 = ma20
        self.number_indexed = 0


    def update_ma(self):
        data_length = len(self.candlesticks)

        begin_traversal = max(data_length - 10, 0)
        total_sum = 0.0
        for i in range(begin_traversal, data_length):
            total_sum += self.candlesticks[i].close_price

        self.ma10.append(total_sum / (data_length - begin_traversal))

        begin_traversal = max(data_length - 20, 0)
        total_sum = 0.0
        for i in range(begin_traversal, data_length):
            total_sum += self.candlesticks[i].close_price

        self.ma20.append(total_sum / (data_length - begin_traversal))

    def check_signal(self):
        if len(self.candlesticks) <= 20:
            return []
        

        if self.ma10[-2] < self.ma20[-2] and self.ma10[-1] > self.ma20[-1]:
            order_setup = []
            order_setup.append(Order(side = "buy", order_type="market", quantity=1, 
                                     order_index=self.number_indexed, 
                                     blocking_index=[self.number_indexed])) 
            order_setup.append(Order(side = "sell", order_type="stop", quantity=1,
                                    stop_price = 0.8 * self.candlesticks[-1].close_price, 
                                    order_index=self.number_indexed + 2,
                                    blocking_index=[self.number_indexed + 1, self.number_indexed + 2]))
            order_setup.append(Order(side = "sell", order_type="limit", quantity=1, 
                                     price = 1.2 * self.candlesticks[-1].close_price,
                                     order_index=self.number_indexed + 1,
                                     blocking_index=[self.number_indexed + 1, self.number_indexed + 2]))

            
            
            self.number_indexed += 3
            return order_setup
        
        return []
            
    
        
    
history = History([], [], [])

def handle_candle(timestamp, open_price, high_price, low_price, close_price, volume):

    current_candle = Candle(timestamp, open_price, high_price, low_price, close_price, volume)
    history.candlesticks.append(current_candle)
    history.update_ma()
    return history.check_signal()




