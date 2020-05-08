import stock_wrapper
from stock_wrapper import Stock

# getting the most updated prices requires a FREE robinhood account
stock_wrapper.robin.login('email', 'password')

apple = Stock('AAPL')
microsoft = Stock('MSFT')

apple.price # get the current price
microsoft.price

# data analysis does NOT require a robinhood account
stock_wrapper.visualize.graph_trendline_analysis([apple, microsoft])
stock_wrapper.visualize.graph_candlestick_analysis([apple, microsoft])

stock_wrapper.visualize.graph_candlestick_analysis([Stock('TSLA')])

