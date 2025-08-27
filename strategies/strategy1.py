from indicators.utils import Candle
from indicators.ema_indicator import ExponentialMovingAverage
from indicators.rsi_indicator import RelativeStrengthIndex

class Strategy:
    """
    This strategy will look to follow a trend. 
    Trend direction is determined based on whether
    the price action is above or below the EMA.
    Overbought and oversold zones will be avoided.

    Attributes
    ----------
    candlesticks : list of Candle
        A list containing the OHLC stock data.
    ema_indicator : ExponentialMovingAverage
        A class which calculates the EMAs for tracked periods.
    rsi_indicator : RelativeStrengthIndex
        A class which calculates the RSIs for tracked periods.    
    """

    def __init__(self):
        self.candlesticks : list[Candle] = []
        self.ema_indicator = ExponentialMovingAverage([14])
        self.rsi_indicator = RelativeStrengthIndex([7]) 

    def update(self, candlestick : Candle):
        