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

class Order:
    """
    Represents an order

    Attributes
    ---------
    side : string
        The side of the order (either buy or sell).
    order_type : string
        The type of the order (market, limit or stop).
    quantity : float
        The amount of shares requested in the order.
    price : float
        The price at which a limit order is executed
    stop_price: float
        The price at which a stop order is executed
    order_index: int
        The unique index of the order
    blocking_index: int
        A list with indexes of orders, whose execution, cancels or removes the current order
    
    """
    def __init__(self, side: str, order_type: str, quantity: float, 
                 price: float = None, stop_price: float = None, order_index: int = None, blocking_index: list[int] = None):
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.stop_price = stop_price
        self.order_index = order_index
        self.blocking_index = blocking_index

    @staticmethod
    def get_long_position(index: int, quantity: float, 
                          stop_loss_price: float, exit_price: float):
        order_setup = []
        
        order_setup.append(Order(side="buy", order_type="market", quantity=quantity,
                                order_index=index, blocking_index=[index]))
        order_setup.append(Order(side="sell", order_type="stop", quantity=quantity,
                                stop_price=stop_loss_price, order_index=index + 1,
                                blocking_index=[index + 1, index + 2]))
        order_setup.append(Order(side="sell", order_type="limit", quantity=quantity,
                                price = exit_price, order_index=index + 2,
                                blocking_index=[index + 1, index + 2]))
        
        return order_setup

    @staticmethod
    def get_short_position(index: int, quantity: float,
                           stop_loss_price: float, exit_price: float):
        order_setup = []

        order_setup.append(Order(side="sell", order_type="market", quantity=quantity,
                                 order_index=index, blocking_index=[index]))
        order_setup.append(Order(side="buy", order_type="stop", quantity=quantity,
                                stop_price=stop_loss_price, order_index=index + 1, 
                                blocking_index=[index + 1, index + 2]))
        order_setup.append(Order(side="buy", order_type="limit", quantity=quantity,
                                price=exit_price, order_index=index + 1,
                                blocking_index=[index + 1, index + 2]))

        return order_setup    

