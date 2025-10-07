from .utils import Candle
from .utils import newton_raphson

class ExponentialMovingAverage:
    """
    Represents an Exponential Moving Average Indicator.

    Attributes
    ----------
    values : list of floats
        Contains the values tracked by the EMA.
    periods : list of integers
        A list containing the periods to be tracked.
    ema_history : dict
        Contains pairs with tracked period and ema history (period -> list of ema-s)
    """
    def __init__(self, periods : list[int]):
        """
        Initializes the EMA.

        Parameters
        ----------
        periods : list of integers
            A list containing the periods of EMA to be tracked.
        """
        self.values = []
        self.periods = periods

        self.ema_history = {period : [] for period in self.periods}

    def update(self, value : float):
        """
        Updates the EMA-s for all tracked periods.

        Uses standard formula for the alpha:
            (alpha = 2 / (N + 1))
        where N is the period length.

        Parameters
        ----------
        candlestick : Candle
            The latest added candlestick.
            
        Returns
        -------
        None
        """
        
        self.values.append(value)
        for period in self.periods:
            window = min(period, len(self.values))
            alpha =  2.0 / (window + 1)
            new_ema = 0
            for i in range(-window, 0):               
                new_ema = new_ema * (1 - alpha) + alpha * self.values[i]
            
            new_ema = new_ema / (1 - (1 - alpha) ** (window))
            self.ema_history[period].append(new_ema)
        
