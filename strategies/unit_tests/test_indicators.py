import pytest
from strategies.indicators.force_index import ForceIndex
from strategies.indicators.utils import Candle


def test_force_index():
    fi = ForceIndex()
    dummy_datetime = (2025, 10, 7, 2025, 11, 30, 0)
    candlesticks = [
        Candle(dummy_datetime, open_price=100.0, high_price=101.0, 
               low_price=99.0, close_price= 100.5, volume=1000),
        Candle(dummy_datetime, open_price=100.4, high_price=102.0, 
               low_price=99.5, close_price= 100.6, volume=750),
        Candle(dummy_datetime, open_price=100.8, high_price=102.5, 
               low_price=98.0, close_price= 101.2, volume=1100),
        Candle(dummy_datetime, open_price=101.1, high_price=101.5, 
               low_price=98.0, close_price= 98.5, volume=1200),
    ]

    for candle in candlesticks:
       fi.update(candle)

    answer = [75, 660, -3240]
    
    diff = [answer[i] - fi.fi_history[i] for i in range(0, len(answer))]
    max_diff = max(diff)
    assert(max_diff < 10**-6)
