# Import Keys
from key import *

# Alpaca Imports
import alpaca_trade_api as tradeapi

# Alpha Vantage Imports
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

# Utility Imports
import matplotlib.pyplot as plot
import time
import pandas as pd
import json


BASE_URL = "https://paper-api.alpaca.markets"

TOLERANCE = 0.1

stocksSMA = {
    'SYK': 0,
    'ALGN': 0,
    'WLTW': 0,
    'PODD': 0,
}
stocksnewSMA = {
    'SYK': 0,
    'ALGN': 0,
    'WLTW': 0,
    'PODD': 0,
}
period = 50
interval = '1min'

ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY,
                       BASE_URL, api_version="v2")
account = alpaca.get_account()

print(account)


def getCurrentSMA(stock_name):
    data_ts, meta_data_ts = ts.get_intraday(
        symbol=stock_name, interval=interval, outputsize='full')
    ti = TechIndicators(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data_ti_sma, meta_data_ti_sma = ti.get_sma(symbol=stock_name, interval=interval,
                                               time_period=period, series_type='close')
    return data_ti_sma.tail(1)['SMA'][0]


for stock in stocksSMA:
    stocksSMA[stock] = getCurrentSMA(stock)

while(True):
    time.sleep(144)
    for stock in stocksSMA:
        stocksnewSMA[stock] = getCurrentSMA(stock)
        # print(stocksSMA[stock], stocksnewSMA[stock])
        if stocksnewSMA[stock] - stocksSMA[stock] > TOLERANCE:
            # print("Buying", stock)
            alpaca.submit_order(stock, 1, 'buy', 'market', 'day')
        elif stocksnewSMA[stock] - stocksSMA[stock] < -TOLERANCE:
            alpaca.submit_order(stock, 1, 'sell', 'market', 'day')
        stocksSMA[stock] = stocksnewSMA[stock]
