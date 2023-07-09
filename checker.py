import os
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockLatestTradeRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date
from pandas.tseries.offsets import BDay
import numpy as np

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

wss_client = StockDataStream(API_KEY, SECRET_KEY)
client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

async def quote_data_handler(data):
    print(data)

def get_latest_quotes(symbols):
    request = StockLatestQuoteRequest(symbol_or_symbols=symbols)
    return client.get_stock_latest_quote(request)

def get_latest_trade(symbols):
    request = StockLatestTradeRequest(symbol_or_symbols=symbols)
    return client.get_stock_latest_trade(request)

def get_date_x_days_ago(x):
    return str(date.today() - BDay(x - 1))

def get_stock_bars_data(symbol):
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=get_date_x_days_ago(20))
    return client.get_stock_bars(request).df

def get_bollinger_bands(data):
    std_dev = np.std(data.close)
    sma_20 = data.close.mean()
    upper_band = sma_20 + (2 * std_dev)
    lower_band = sma_20 - (2 * std_dev)
    return upper_band, lower_band

def check_if_should_buy(symbols):
    data = get_stock_bars_data(symbols)
    quotes = get_latest_quotes(symbols)
    _, lower_band = get_bollinger_bands(data)
    sma_20 = round(data.close.mean(), 2)

    for ticker in quotes:
        print("-----------------------------")
        print('Ticker:', ticker)
        print('ASK Price: ', quotes[ticker].ask_price)
        print('BID Price: ', quotes[ticker].bid_price)
        print('Lower Band:', round(lower_band, 2))
        print('SMA 20: ', sma_20)
        if quotes[ticker].ask_price <= lower_band:
            print("BUY")
        else:
            print("DON'T BUY")
        print("-----------------------------")


check_if_should_buy(["SPY"])
# wss_client.subscribe_quotes(quote_data_handler, "SPY")
# wss_client.run()
