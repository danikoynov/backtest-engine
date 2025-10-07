from .utils import Candle

class ExponentialMovingAverage:
    """
    Represents an Exponential Moving Average Indicator.

    Attributes
    ----------
    periods : list of integers
        A list containing the periods to be tracked.
    ema_history : dict
        Contains pairs with tracked period and ema history (period -> list of ema-s)
    """
    def __init__(self, periods : list[int]):
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
        for period in self.periods:
            alpha =  2.0 / (period + 1)
            last_ema = self.ema_history[period][-1] if self.ema_history[period] else 0.0
            new_ema = last_ema * (1 - alpha) + value * alpha
            self.ema_history[period].append(new_ema)
