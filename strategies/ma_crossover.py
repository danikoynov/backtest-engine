import pandas as pd
from datetime import datetime
from orders import Order
from utils import Candle

    
class History:
    def __init__(self, candlesticks: list[Candle], ma10 : list[float], ma20: list[float]):
        self.candlesticks = candlesticks
        self.ma10 = ma10
        self.ma20 = ma20
        self.number_executed = 0


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
        

        if self.ma10[-2] < self.ma20[-1] and self.ma10[-1] > self.ma20[-1]:
            order_setup = []
            order_setup.append(Order(side = "buy", order_type="market", quantity=1, 
                                     execution_index=self.number_executed)) 
            order_setup.append(Order(side = "sell", order_type="limit", quantity=1, 
                                     price = 1.04 * self.candlesticks[-1].close_price,
                                     execution_index=self.number_executed + 1)) # later will integrate support and resistance
            order_setup.append(Order(side = "sell", order_type="stop", quantity=1,
                                      stop_price = 0.98 * self.candlesticks[-1].close_price, 
                                      execution_index=self.number_executed + 1))
            
            self.number_executed += 2
            return order_setup
        
        return []
            
    
        
    
history = History([], [], [])

def handle_candle(timestamp, open_price, high_price, low_price, close_price, volume):
    print("Close price " + str(type(close_price)))
    current_candle = Candle(timestamp, open_price, high_price, low_price, close_price, volume)
    history.candlesticks.append(current_candle)
    history.update_ma()
    return history.check_signal()




