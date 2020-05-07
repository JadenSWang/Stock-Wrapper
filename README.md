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
- stock market data gathering
    - robin_stocks (robinhood)
    - yfinance (yahoo finance)
    
    
### Getting Started
Complete example is under Examples/example.py

Most of the data manipulation is based off the <stock_wrapper.Stock> object. 

### Using Stock_Wrapper with a RobinHood account
If you are a robinhood trader, you can login to your robinhood account and 
buy/sell stocks by simply creating a stock object like so.

##### We will be using the S&P 500 Index as an example
> stock = Stock('SPY')

##### Stock_Wrapper 
> stock.high
> stock.low

other properties include open, close, ceo, history, etc.
