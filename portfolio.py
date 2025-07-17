class Portfolio:
    """
    Represents a trading portfolio with cash and assets information

    Attributes:
        initial_cash (float) : Initial cash in the portfolio
        cash (float): Available cash in the portfolio
        positions (dict): Holdings per symbol
        holdings_value (float): the value of all holdings
        toatl_value (float): the current total value of the portfolio
    """
    def __init__(self, initial_cash = 100000):
        self.inital_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}
        self.holdings_value = 0
        self.total_value = initial_cash
        self.history = []

    def update_market_prices(self, price_data):
        
        self.holdings_value = 0
        for symbol, quantity in self.positions.items():
            self.holdings_value += price_data[symbol]
        
        self.total_value = self.cash + self.holdings_value
        self.history.append(self.total_value)

    def buy(self, symbol, price, quantity): 
        cost = price * quantity
        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        else:
            raise ValueError("Not enough cash to execute buy order")

    def sell(self, symbol, price, quantity):

        print("current quantity/sell: " + str(self.positions.get(symbol, 0)))
        if self.positions.get(symbol, 0) >= quantity:
            self.positions[symbol] -= quantity
            self.cash += price * quantity
            if self.positions[symbol] == 0:
                del self.positions[symbol]
        else:
            raise ValueError("Not enough holdings to execute sell order")
        
    def get_portfolio_value(self):
        return self.total_value
    
    def get_cash(self):
        return self.cash
    
    def get_positions(self):
        return dict(self.positions) # this is creating a copy!
    
    def get_history(self):
        return self.history