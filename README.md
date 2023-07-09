# Bollinger Bands Stock Analyzer
This simple Python script uses Bollinger Bands to determine whether a certain stock should be bought or not. It specifically considers if the stock's asking price is below the lower Bollinger Band.

Bollinger Bands consist of a middle band (which is a 20-day simple moving average) with two outer bands. The outer bands are typically two standard deviations away from the middle band. When the price of a stock drops below the lower Bollinger Band, it might be considered a good time to buy, as the stock may be oversold. However, it's important to note that this script uses a very simple strategy and doesn't consider other important factors like market news, company fundamentals or other technical indicators.

## How to Use
Before running the script, ensure that the following environment variables are set:
```
API_KEY: Your Alpaca API key
SECRET_KEY: Your Alpaca Secret Key
```

These are needed to connect to the Alpaca Stock Data API and fetch the relevant data.

To run the script, simply run python filename.py from your terminal (replace "filename.py" with the actual name of the script).

The script is currently set to analyze SPY (S&P 500 ETF Trust) but this can easily be changed by replacing "SPY" with the ticker symbol of the stock you want to analyze in the check_if_should_buy function call at the bottom of the script.

```
check_if_should_buy(["SPY"]) # change "SPY" to your chosen symbol
```

## Output
The script will print output to the terminal for each stock, showing the ticker, ask price, bid price, lower Bollinger Band, and the 20-day simple moving average (SMA 20). It will also print a recommendation on whether to buy or not based on the Bollinger Band strategy. Here's an example of the output:

```
-----------------------------
Ticker: SPY
ASK Price:  315.20
BID Price:  315.18
Lower Band: 310.20
SMA 20:  315.20
DON'T BUY
-----------------------------
```

## Dependencies
The script depends on several libraries including os, numpy, and pandas. It also uses the Alpaca Stock Data API and its associated Python client libraries: alpaca.data.live, alpaca.data.historical, alpaca.data.requests, and alpaca.data.timeframe.