import yfinance as yf
import os
import datetime
import pandas as pd

def fetch_data():
    ticker = "TSLA"
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(weeks=208)

    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')
    return data

def save_data(df, filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, filename)

    df.to_csv(file_path)
    print("Data is saved at " + file_path)

def handle_data():
    df = fetch_data()
    save_data(df, "APPL_data")

from strategies.ma_crossover import handle_candle
from orders import Order
from portfolio import Portfolio

def execute_orders(ticker, last_close_price, current_price, 
                   orders_stack: list[Order], portfolio: Portfolio):
    executed_indexes = set()

    
    for order in orders_stack:
        executed = False
        if order.order_type == "market":
            executed = True

        if order.order_type == "limit":
            if order.side == "buy" and current_price < order.price:
                executed = True
            if order.side == "sell" and current_price > order.price:
                executed = True
        
        if order.order_type == "stop":
            if last_close_price < order.stop_price and current_price > order.stop_price:
                executed = True
            if last_close_price > order.stop_price and current_price < order.stop_price:
                executed = True

        if executed == True and order.execution_index not in executed_indexes: # quick fix as stop orders come after limit
            #print(str(order.order_type) + " " + str(order.execution_index))
            if order.side == "buy":
                portfolio.buy(ticker, current_price, order.quantity)
            if order.side == "sell":
                portfolio.sell(ticker, current_price, order.quantity)
            executed_indexes.add(order.execution_index)

    remaining_orders = [order for order in orders_stack 
                        if order.execution_index not in executed_indexes]

    return remaining_orders
    #print("Remaining " + str(len(remaining_orders)))

            
            


def simulate(data):
    ticker = "TSLA"

    
    orders_stack = []
    portfolio = Portfolio()
    previous_close = 0.0

    for index, row in data.iterrows():
        
        print("Before " + str(len(orders_stack)))
        if previous_close != 0.0:
            orders_stack = execute_orders(
                ticker=ticker,
                last_close_price=previous_close, 
                current_price=row['Open'][ticker], 
                orders_stack=orders_stack,
                portfolio=portfolio
            )
        print("After " + str(len(orders_stack)))

        orders = handle_candle(
            index,
            row['Open'][ticker], 
            row['High'][ticker], 
            row['Low'][ticker],
            row['Close'][ticker], 
            row['Volume'][ticker]
        )

        previous_close = row['Close'][ticker]

        orders_stack.extend(orders)
        
        portfolio.update_market_prices({ticker: row['Close'][ticker]})
        print("Portfolio value " + str(portfolio.get_portfolio_value()))
        print("Portfolio cash " + str(portfolio.get_cash()))
        
if __name__ == "__main__":
    df = fetch_data()
    simulate(df)


"""
figure out exact prices to use for order execution
add slipage and commision
add statistics line PnL


"""