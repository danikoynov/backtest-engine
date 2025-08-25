from utils import Candle

class RelativeStrengthIndex:
    """
    Represents a Relative Strength Index Indicator.

    RSI represents the relative strength of the upward and
    downward trend in a given period.

    It has three main use cases:
        1. Whenever the RSI is above a certain threshold, the
        stock is overbought and gives a sell signal. Conversely,
        when it is the RSI is below a certain threshold, it is 
        oversold and gives a buy signal.
        2. Bullish or bearish divergences.
        3. Charting patterns.
    Attributes
    ----------
    periods : list of integers
        A list containing the periods to be tracked.
    rsi_history : dictionary
        Contains pairs (period -> rsi history). 
    """
    def __init__(self, periods : list[int]):
        self.candlesticks: list[Candle] = list()
        self.periods = periods
        self.rsi_history = {period : [] for period in periods}


    def update(self, candlestick : Candle):
        """
        Updates the RSI index for all tracked periods.

        Parameters
        ----------
        candlestick : Candle
            The latest added candlestick.
        
        Returns
        -------
        None
        """
        
        self.candlesticks.append(candlestick)
        for period in self.periods:
            if len(self.candlesticks) > period:
                gains = 0.0
                losses = 0.0
                for i in range(-period, 0):
                    delta = self.candlesticks[i].close_price - self.candlesticks[i - 1].close_price
                    if delta > 0:
                        gains += delta
                    else:
                        losses -= delta

                rsi = 0
                if losses == 0 and gains == 0:
                    rsi = 50.0
                elif losses == 0:
                    rsi = 100.0
                else:
                    rsi = 100 - 100 / (1 + gains / losses)

                self.rsi_history[period].append(rsi)                

