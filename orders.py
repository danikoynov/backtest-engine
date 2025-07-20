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
    