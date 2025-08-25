from datetime import datetime

class Candle:
    """
    Represents a single candlestick in a trading chart

    Attributes
    ---------
    timestamp : datetime
        The time at which the candlestick is recorded.
    open_price : float
        The opening price of the asset at the beginning of the period.
    high_price : float
        The highest price of the asset during the period.
    low_price : float
        The lowest price of the asset duing the period.
    close_price : float
        The closing price of the asset at the end of the period.
    volume : float
        The trading volume during the period.
    """
    def __init__(self, timestamp: datetime, open_price: float, high_price: float,
                 low_price: float, close_price: float, volume: float):
        """
        Initializes a Candle object with OHLCV data for a specific time period.

        Parameters
        ----------
        timestamp : datetime
            The time at which the candlestick is recorded.
        open_price : float
            The asset's opening price during the time period.
        high_price : float
            The highest price reached during the time period.
        low_price : float
            The lowest price reached during the time period.
        close_price : float
            The asset's closing price during the time period.
        volume : float
            The trading volume during the time period.
        """
        self.timestamp = timestamp  
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume

