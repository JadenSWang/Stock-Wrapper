from Classes.JSONReader import JSONReader
import stock_wrapper
from stock_wrapper import Stock
import multiprocessing


credentials = JSONReader.read_file("Credentials.json")
stock_wrapper.robin.login(credentials['email'], credentials['password'])

portfolio = stock_wrapper.robin.build_portfolio()
portfolio.append(Stock('LYFT'))
portfolio.append(Stock('UBER'))
portfolio.append(Stock('AMD'))
portfolio.append(Stock('PYPL'))
portfolio.append(Stock('CSCO'))
# stock_wrapper.visualize.graph_trendline_analysis(portfolio)
# stock_wrapper.visualize.graph_candlestick_analysis(portfolio)

stock_wrapper.visualize.graph_candlestick_analysis([Stock('SUN')])
