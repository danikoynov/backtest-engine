from .indicators.utils import Candle
from .indicators.ema_indicator import ExponentialMovingAverage
from .indicators.rsi_indicator import RelativeStrengthIndex
from .indicators.utils import Order
from .indicators.portfolio import Portfolio

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
    EMA_PERIOD : int
        Tracked EMA period.
    ema_indicator : ExponentialMovingAverage
        A class which calculates the EMAs for tracked periods.
    RSI_PERIOD : int
        Tracked RSI period.
    rsi_indicator : RelativeStrengthIndex
        A class which calculates the RSIs for tracked periods.
    number_of_orders : int
        The number of orders sent by the strategy.
    """

    def __init__(self):
        self.candlesticks : list[Candle] = []
        self.EMA_PERIOD = 14
        self.ema_indicator = ExponentialMovingAverage([self.EMA_PERIOD])
        self.RSI_PERIOD = 7
        self.rsi_indicator = RelativeStrengthIndex([self.RSI_PERIOD]) 
        self.number_of_orders = 0

    def update(self, candlestick : Candle):
        """
        Updates indicators inside the strategy.

        Parameters
        ----------
        candlestick : Candle
            Latest recorded candlestick of the stock.
        
        Returns
        -------
        None 
        """
        self.candlesticks.append(candlestick)
        self.ema_indicator.update(candlestick)
        self.rsi_indicator.update(candlestick)

    def get_orders(self, portfolio : Portfolio):
        """
        A function which returns orders based on indicator signals.

        The function can only give orders if the number of candles
        passed is enough to cover all indicator tracked periods.

        Parameters
        ----------
        portfolio : Porfolio
            A portfolio tracking the performance and active assets.

        Returns
        -------
        None
        """

        if (self.EMA_PERIOD > len(self.candlesticks) or
            self.RSI_PERIOD > len(self.candlesticks)):
            return []
        current_price = self.candlesticks[-1].close_price
        order_setup = []
        
        max_value = portfolio.MAX_RISK * portfolio.cash

        if (self.ema_indicator.ema_history[self.EMA_PERIOD][-1] < current_price and
            self.rsi_indicator.rsi_history[self.RSI_PERIOD][-1] < 70):
            order_setup = Order.get_long_position(self.number_of_orders, quantity=max_value / self.candlesticks[-1].close_price,
                                                  stop_loss_price=0.9*current_price, exit_price=1.1*current_price)
            print("Enter long")
            
        elif (self.ema_indicator.ema_history[self.EMA_PERIOD][-1] > current_price and
              self.rsi_indicator.rsi_history[self.RSI_PERIOD][-1] > 30):
            order_setup = Order.get_short_position(self.number_of_orders, quantity=max_value / self.candlesticks[-1].close_price,
                                                   stop_loss_price=1.1*current_price, exit_price=0.9*current_price)
            print("Enter short")
            
        self.number_of_orders += len(order_setup)
        return order_setup