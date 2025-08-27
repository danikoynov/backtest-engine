from strategies.indicators.utils import Candle
import pandas as pd
import mplfinance as mpf
from strategies import ExponentialMovingAverage
import numpy as np
import matplotlib.pyplot as plt

class Visualizer:
    """
    A class used to visualize market data and indicators.

    Attributes
    ----------
    data : pandas.DataFrame
        A dataframe containing the OPHL data for a given stock.
    ticker : str
        The stock whose data will be visualized.
    ema_periods : list of integers
        The periods of EMA that will be tracked.
    """
    def __init__(self, data : pd.DataFrame, ticker : str):
        self.data = data
        self.ticker = ticker
        self.ema_periods = [10, 20]

    def get_exponential_moving_average(self):
        """
        A function which calculates the EMA for the tracked periods.

        We make use of the ExponentialMovingAverage class and feed it the
        market data.

        Parameters
        ----------
        None

        Returns
        ema_history : dictonary
            Contains pairs (period -> list of floats) representing the EMA for different periods.
        """
        ema_indicator = ExponentialMovingAverage(self.ema_periods) # default periods
        for i in range(0, len(self.data)):
            ema_indicator.update(candlestick=Candle(
                timestamp=self.data.index[i],
                open_price=self.data.iloc[i]["Open"],
                high_price=self.data.iloc[i]["High"],
                low_price=self.data.iloc[i]["Low"],
                close_price=self.data.iloc[i]["Close"],
                volume=self.data.iloc[i]["Volume"]))
        

        return ema_indicator.ema_history
  
    def get_exponential_lines(self):
        """
        A function that gives additional plots for the EMAs.

        Parameters
        ----------
        None

        Returns
        colors : list
            Contains the used colors for the EMA lines.
        ap : list of plots
            Contains the plot layers for each EMA line.
        """
        ap = []
        ema_history = self.get_exponential_moving_average() 
        n_emas = len(ema_history)
        cmap = plt.cm.get_cmap('tab20')
        colors = []
        for i, period in enumerate(self.ema_periods):
            ema = pd.Series(ema_history[period])
            color = cmap(i / n_emas)
            colors.append(color)
            ap.append(mpf.make_addplot(ema, color=color, width=1.0, linestyle='-', secondary_y=False))

        return colors, ap

    def plot(self):
        """
        A function that plots the market data with indicators.

        The function makes use of the mplfinance library.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.data = self.data[["Open", "High", "Low", "Close", "Volume"]]
        self.data.index.name = None

        ema_colors, ap = self.get_exponential_lines()      

        fig, axlist = mpf.plot(
            self.data, 
            type="candle", 
            style="yahoo", 
            volume=False, 
            title=self.ticker,
            addplot=ap,
            returnfig=True
        )

        ax = axlist[0]
        for i, period in enumerate(self.ema_periods):
            ax.plot([], [], color=ema_colors[i], label=f"EMA {period}")
        
        ax.legend(loc="upper left")

        plt.show()


