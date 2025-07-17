class Order:
    def __init__(self, side, order_type, quantity, 
                 price = None, stop_price = None, execution_index = None):
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.stop_price = stop_price
        self.execution_index = execution_index
    