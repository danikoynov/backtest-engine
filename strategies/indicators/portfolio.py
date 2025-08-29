from rich import print
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd
import statistics
import math

class Portfolio:
    """
    Represents a trading portfolio with cash and asset holdings.

    Attributes
    ----------
    initial_cash : float
        Initial cash in the portfolio.
    cash : float
        Available cash in the portfolio.
    positions : dict
        Current holdings per symbol (symbol -> quantity).
    holdings_value : float
        The current market value of all held positions.
    total_value : float
        The current total value of the portfolio (cash + holdings).
    dates : datetime
        The dates of trading history.
    MAX_RISK : constant float
        The maximal percentage of cash to be used in a trade.
    """
    
    def __init__(self, initial_cash = 100000):
        """Initializes the portfolio with empty positions and initial cash."""
        self.inital_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}
        self.holdings_value = 0
        self.total_value = initial_cash
        self.history = []
        self.dates = []
        self.MAX_RISK = 0.02

    def update_market_prices(self, price_data, timestamp : datetime):
        """
        Updates the holdings_value based on the new market prices.
        Adds current total value into the history of the portfolio.

        Parameters
        ---------
        price_data : dict
            A dictionary mapping each ticker symbol to its latest price.

        Returns 
        -------
        None
        """
        self.holdings_value = 0
        for symbol, quantity in self.positions.items():
            self.holdings_value += price_data[symbol] * quantity
        
        self.total_value = self.cash + self.holdings_value
        self.history.append(self.total_value)
        self.dates.append(timestamp)

    def buy(self, symbol, price, quantity):
        """
        Executes a buy order.

        Parameters
        ----------
        symbol : string
            The symbol of the asset being bought.
        price : float
            The current price of the asset. 
        quantity : float
            The amount of shares being bought.
            
        Raises
        ------
        ValueError 
            If there is not enough cash to execute the order.

        Returns
        -------
        None
        """ 
        cost = price * quantity
        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        else:
            raise ValueError("Not enough cash to execute buy order")

    def sell(self, symbol, price, quantity):
        """
        Executes a sell order.

        Parameters
        ----------
        symbol : string
            The symbol of the asset being sold.
        price : float
            The current price of the asset.
        quantity : float
            The amount of shares being sold.

        Raises
        ------
        ValueError 
            If there are not enough shares to execute the order.

        Returns
        -------
        None
            
        """
        #if self.positions.get(symbol, 0) >= quantity:
        self.positions[symbol] = self.positions.get(symbol, 0) - quantity
        self.cash += price * quantity
        if self.positions[symbol] == 0:
            del self.positions[symbol]
        #else
        #    raise ValueError("Not enough holdings to execute sell order")
        
    def get_portfolio_value(self):
        """
        Returns the current total value of the portfolio.

        Returns
        -------
        float
            The total portfolio value (cash + holdings).
        """
        
        return self.total_value
    
    def get_cash(self):
        """
        Returns the current cash in the portfolio.

        Returns
        ------
        float
            The current cash in the portfolio.
        """
        return self.cash
    
    def get_positions(self):
        """
        Returns current open positions in the portfolio.

        Returns
        -------
        dict
            A copy of the current asset positions, where keys are symbols and values are quantities. 
        """
        return dict(self.positions)
    
    def get_history(self):
        """
        Return the portfolio total value over time.

        Returns
        history : list
            A list containing all recorded portfolio total values.
        """
        return self.history
    
    def print_total_return(self):
        """
        Prints the the total portfolio value.

        Returns
        -------
        """
        total_return = self.total_value - self.inital_cash

        if total_return > 0:
            print(f"Total return: [green]{round(total_return, 2)}€[/green]")
        else:
            print(f"Total return: [red]{round(total_return, 2)}€[/red]")
        
        return self.total_value - self.inital_cash
    
    def print_initial_cash(self):
        print(f"Initial cash: [white]{round(self.inital_cash, 2)}€[/white]")

    def print_cagr(self):
        """
        Print the compound annual grow rate (CAGR).

        Returns
        -------
        None
        """
        number_of_days = (self.dates[-1] - self.dates[0]).days + 1
        number_of_years = number_of_days / 365.25
        cagr = ((self.total_value / self.inital_cash) ** (1.0 / number_of_years) - 1) * 100

        if cagr > 0:
            print(f"CAGR: [green]{round(cagr, 2)}%[/green]")
        else:
            print(f"CAGR: [red]{round(cagr, 2)}%[/red]")

    def plot_equity_curve(self):
        """
        Prints the equity curve.

        On the x-axis are the times at which the porfolio total values is recorded.
        On the y-axis is the ratio of total value and initial cash at each moment.

        Rerturns
        --------
        """
        history_normalized = [value / self.inital_cash for value in self.history]
        equity_series = pd.Series(data=history_normalized, index=self.dates)

        plt.figure(figsize=(10, 5), dpi=120)
        plt.plot(equity_series, marker="o", linewidth=1, markersize = 2, color="lightgreen")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as YYYY-MM-DD

        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Ratio of Value / Initial Cash")

        plt.show()

    def print_std(self):
        """
        Prints the annualized standard deviation of the portfolio.

        Returns
        -------
        None
        """

        returns = []
        for i in range(1, len(self.history)):
            returns.append(self.history[i] / self.history[i - 1] - 1.0)

        std_daily = statistics.stdev(returns)

        std_yearly_percentage = (std_daily * math.sqrt(252)) * 100

        print(f"Standard Deviation Yearly: [white]{round(std_yearly_percentage, 2)}%c[/white]")

    def get_stats(self):
        """
        Gives statistics about the portfolio.
        """
        self.print_initial_cash()
        self.print_total_return()
        self.print_cagr()
        self.print_std()
        self.plot_equity_curve()


        




        