from utils import Candle

class ExponentialMovingAverageIndicator:
    """
    Represents an Exponential Moving Average Indicator.

    Attributes
    ----------
    candlesticks : list of Candle
        A list containing the history of candlesticks.
    periods : list of integers
        A list containing the periods to be tracked.
    ema_history : dict
        Contains pairs with tracked period and ema history (period -> list of ema-s)
    """
    def __init__(self, candlesticks : list[Candle], periods : list[int]):

        self.candlesticks = candlesticks
        self.periods = periods
        self.ema_history = {period : [] for period in self.periods}

    def update(self, candlestick : Candle):
        """
        Updates the ema-s for all tracked periods.

        Uses standard formula for the alpha:
            (alpha = 2 / (N + 1))
        where N is the period length.
        
        Parameters
        ----------
        candlestick : Candle
            The latest added candlestick.
            
        """
        candlestick.append(candlestick)
        for period in self.periods:
            alpha =  2.0 / (period + 1)
            last_ema = self.ema_history[period] if self.ema_history[period] else 0.0
            new_ema = last_ema * (1 - alpha) + candlestick.close_price * alpha
            self.ema_history[period].append(new_ema)
