import stock_wrapper
from stock_wrapper import Stock

apple = Stock('AAPL')
microsoft = Stock('MSFT')

apple.price # get the current price
microsoft.price

apple.history # get the entire history of the stock including Moving Averages
microsoft.history

stock_wrapper.visualize.graph_trendline_analysis([apple, microsoft])
stock_wrapper.visualize.graph_candlestick_analysis([apple, microsoft])

portfolio = stock_wrapper.robin.build_portfolio()
portfolio.append(Stock('LYFT'))
portfolio.append(Stock('UBER'))
portfolio.append(Stock('AMD'))
portfolio.append(Stock('PYPL'))
portfolio.append(Stock('CSCO'))
# stock_wrapper.visualize.graph_trendline_analysis(portfolio)
# stock_wrapper.visualize.graph_candlestick_analysis(portfolio)

stock_wrapper.visualize.graph_candlestick_analysis([Stock('SUN')])
