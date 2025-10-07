from .utils import Candle

class ForceIndex:
    """
    A class implementing the Force Index Indicator.

    A single value of the Force Index is calculated as follows:
        (Close_price_t - Close_price_(t-1)) * Volume_t
    This takes into account both the direction of the price action
    and the volume (which represents the behaviour of the masses and their
    sentiment to the stock).

    Attributes
    ----------
    self.candlesticks : list of Candles
        Contains the historical data of a stock.
    self.fi_history : list of double
        Contains the values of the Force Index for each trading bar.
    """
    def __init__(self):
        """
        Initializes the class.
        """

        self.candlesticks = []
        self.fi_history = []

    def update(self, candle : Candle):
        """
        Updates the Force Index.

        Receives as an attribute the data for the most recent candestick
        and calculates the next value of the Force Index.

        Parameters
        ----------
        candle : Candle
            An object containing the data for the most recent trading bar.
        """
        
        if self.candlesticks:
            delta_price = candle.close_price - self.candlesticks[-1].close_price
            self.fi_history.append(delta_price * candle.volume) # Appends Force Index Value

        self.candlesticks.append(candle)



