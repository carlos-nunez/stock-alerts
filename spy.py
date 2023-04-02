import os
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockLatestTradeRequest
from alpaca.data.requests import StockBarsRequest
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
    data = client.get_stock_latest_quote(request)
    return data


def get_latest_trade(symbols):
    request = StockLatestTradeRequest(symbol_or_symbols=symbols)
    data = client.get_stock_latest_trade(request)
    return data

def get_date_20_days_ago():
    today = date.today()
    twenty_days_ago = str(today - BDay(19))
    return twenty_days_ago

def get_20_day_mov_avg(symbol):
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=get_date_20_days_ago())
    data = client.get_stock_bars(request).df
    print(data)
    return data

def get_20_day_std_dev(symbol):
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=get_date_20_days_ago())
    data = client.get_stock_bars(request).df
    std_dev = data.close.std()
    return std_dev

def get_20_day_bollinger_bands(symbol):
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=get_date_20_days_ago())
    data = client.get_stock_bars(request).df
    
    std_dev = np.std(data.close)
    sma_20 = data.close.mean()
    upper_band = sma_20 + (2 * std_dev)
    lower_band = sma_20 - (2 * std_dev)
    return upper_band, lower_band


# quotes = get_latest_quotes(["SPY"])
# trades = get_latest_trade(["SPY"])
# spy_trade = trades['SPY']
# spy_quote = quotes['SPY'].ask_price
# bars = get_20_day_mov_avg(["SPY"])
# _, lower_band = get_20_day_bollinger_bands(["SPY"])
# sma_20 = round(bars.close.mean(), 2)



def check_if_should_buy(symbols):
    request = StockBarsRequest(symbol_or_symbols=symbols, timeframe=TimeFrame.Day, start=get_date_20_days_ago())
    quotes = get_latest_quotes(symbols)
    data = client.get_stock_bars(request).df
    std_dev = np.std(data.close)
    sma_20 = round(data.close.mean(), 2)
    lower_band = round(sma_20 - (2 * std_dev), 2)

    for ticker in quotes:
        print("-----------------------------")
        print('Ticker:', ticker)
        print('ASK Price: ', quotes[ticker].ask_price)
        print('BID Price: ', quotes[ticker].bid_price)
        print('Lower Band:', lower_band)
        print('SMA 20: ', sma_20)
        if quotes[ticker].ask_price <= lower_band:
            print("BUY")
        else:
            print("DON'T BUY")
        print("-----------------------------")


check_if_should_buy(["SPY"])
# wss_client.subscribe_quotes(quote_data_handler, "SPY")
# wss_client.run()