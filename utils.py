from datetime import datetime

class Candle:
    def __init__(self, timestamp: datetime, open_price: float, high_price: float,
                 low_price: float, close_price: float, volume: float):
        self.timestamp = timestamp
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
