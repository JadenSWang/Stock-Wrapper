## StockTracker
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

### Introduction
This Stock market library utilizes both static and class system architecture to 
provide a streamlined stock market analysis experience.

No API key is needed, all data is 100% free and accessible from yahoo finance and robin_hood's 
free API. 

### Installation
Setup is simple, simply type 
> pip install stock_wrapper

If you wish to use the source code simply download this repository, its free forever, I promise

### What packages are used?

- direct portfolio manipulation
    - robin_stocks (robinhood: requires account)
        - market buy/sell
        - limit buy/sell
- stock market data gathering
    - robin_stocks (robinhood)
    - yfinance (yahoo finance)
    
### Getting Started
Complete example is under Examples/example.py

Most of the data manipulation is based off the <stock_wrapper.Stock> object. 

##### We will be using the S&P 500 Index as an example
> from stock_wrapper import Stock 
>
> snp = Stock('SPY')

##### Stock_Wrapper 
> high_price = snp.high
>
> low_price = snp.low

Other properties include open, close, ceo, history, etc.

##### Visualization
> from stock_wrapper import visualize
> from stock_wrapper import Stock

Place your stock object inside brackets, as of now, visualization methods take in a list of Stock objects

> snp = Stock('SPY')
>
> visualize.graph_trendline_analysis([snp])
>
> visualize.graph_candlestick_analysis([snp])

The graphing might take a couple seconds since it's loading years and years of data and calculating various moving averages

If you want to graph multiple stocks, its best to group them like so
> microsoft = Stock('MSFT')
>
> visualize.graph_trendline_analysis([snp, microsoft])