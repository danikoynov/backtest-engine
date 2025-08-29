import yfinance as yf
import os
import datetime
import pandas as pd
from visualizer import Visualizer
def fetch_data(ticker):
    """
    Fetches the historic data.

    Parameters
    ----------
    ticker : str
        Indicates the ticker symbol of the traded asset.

    Returns
    -------
    data : Dataframe
        A multicolumn dataframe containing the historical data of the asset.
    """
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(weeks=52)

    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')
    return data

def save_data(df, filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, filename)

    df.to_csv(file_path)
    print("Data is saved at " + file_path)

from strategies.strategy1 import Strategy
from strategies.indicators.utils import Order
from strategies.indicators.portfolio import Portfolio
from strategies.indicators.utils import Candle

def execute_orders(ticker, previous_candle, current_candle, 
                   orders_stack: list[Order], portfolio: Portfolio, executed_orders: set[int]):
    """
    Simulates exectution of the orders.

    The execution of an order depends on which other orders have been executed.
    If multiple orders are executed at the same time and they are cyclic dependent
    it is not clear which one to execute. Thus, all orders are assigned a priority.
    The orders come in a decreasing priority in the list.

    Once an order is executed, its index is added to the list of executed orders.
    This is a simple model, which assumes that the market orders are executed at the
    start of the period and that stop/limit orders are executed at their respective price.

    Parameters
    ----------
    ticker : str
        The ticker symbol of the traded asset.
    previous_candle : pandas.Series
        The information for the previous candle.
    current_candle : pandas.Series
        The information for the current candle.
    orders_stack : list of Order
        A list with all orders which have not been yet executed.
    portfolio : Portfolio
        An object containing the information for the portfolio.
    executed_orders : set of integers
        A set containing the indexes of all executed orders.
    
    Returns
    -------
    remaining_orders : list of Order
        A list with all remaining orders, which are not executed.
    executed_orders : set of integers
        An updated set with the integers of executed orders.
    """
  
    for order in orders_stack:
        depedency_executed = False
        for index in order.blocking_index:
            if index in executed_orders:
                depedency_executed = True
                break
        
        if depedency_executed:
            executed_orders.add(order.order_index)
            continue

        executed = False
        execution_price = 0.0
        if order.order_type == "market":
            execution_price = current_candle['Open']
            executed = True

        if order.order_type == "limit":
            if order.side == "buy" and current_candle['Low'] < order.price:
                execution_price = order.price
                executed = True
            if order.side == "sell" and current_candle['High'] > order.price:
                execution_price = order.price
                executed = True
        
        if order.order_type == "stop":
            if (previous_candle['Low'] < order.stop_price and 
                current_candle['High'] > order.stop_price):
                executed = True
                execution_price = order.stop_price
            if (previous_candle['High'] > order.stop_price and 
                current_candle['Low'] < order.stop_price):
                executed = True
                execution_price = order.stop_price

        if executed == True: 
            if order.side == "buy":
                portfolio.buy(ticker, execution_price, order.quantity)
            if order.side == "sell":
                portfolio.sell(ticker, execution_price, order.quantity)
            executed_orders.add(order.order_index)

    remaining_orders = [order for order in orders_stack 
                        if order.order_index not in executed_orders]

    return remaining_orders, executed_orders
        


def simulate(full_data, ticker):
    """
    Simulates trading process.

    Each day previously placed orders are checked for execution.
    After that based on indicators we place the new orders.
    They will be executed from the next day.
    
    Parameters
    ----------
    full_data : pandas.DataFrame
        Multilevel dataframe containing the OPHC candles for multiple stocks.
    ticker : str
        A string containing the ticker symbol for a specific stock.
    
    Returns
    -------
    portfolio : Portfolio
        A class containing the performance history of the portfolio. 
    """

    data = full_data.xs(ticker, level=1, axis=1)
    orders_stack = []
    executed_orders = set()
    portfolio = Portfolio()
    strategy = Strategy()

    for i in range(0, len(data)):

        print("Processing day " + str(i))
        if i != 0:
            orders_stack, executed_orders = execute_orders(
                ticker=ticker,
                previous_candle=data.iloc[i - 1],
                current_candle=data.iloc[i],
                orders_stack=orders_stack, 
                portfolio=portfolio,
                executed_orders=executed_orders
            )


        current_candle = Candle(
            timestamp=data.index[i],
            open_price=data.iloc[i]['Open'],
            high_price=data.iloc[i]['High'],
            low_price=data.iloc[i]['Low'],
            close_price=data.iloc[i]['Close'],
            volume=data.iloc[i]['Volume']
        )

        strategy.update(current_candle)
        orders_stack.extend(strategy.get_orders(portfolio))

        portfolio.update_market_prices({ticker : data.iloc[i]['Close']}, data.index[i])
        print("Portfolio value: " + str(portfolio.get_portfolio_value()))

    #vs = Visualizer(data, ticker)
    #vs.plot()
    
    return portfolio
        
def analyze(portfolio : Portfolio):
    portfolio.get_stats()

if __name__ == "__main__":
    ticker = "AAPL"
    df = fetch_data(ticker)
    portfolio = simulate(df, ticker)
    analyze(portfolio)
