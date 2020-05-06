from Classes.JSONReader import JSONReader
import stock_wrapper
from stock_wrapper import Stock
import multiprocessing


credentials = JSONReader.read_file("Credentials.json")
stock_wrapper.robin.login(credentials['email'], credentials['password'])

portfolio = stock_wrapper.robin.build_portfolio()
portfolio.append(Stock('LYFT'))
portfolio.append(Stock('UBER'))
stock_wrapper.visualize.graph_analysis(portfolio)
# stock_wrapper.visualize.graph_analysis([Stock('LYFT'), Stock('UBER')])

# stock_wrapper.visualize.graph_analysis(Stock('SPY'))
# stock_wrapper.visualize.graph_analysis(Stock('TSLA'))
# stock_wrapper.visualize.graph_analysis(Stock('NVDA'))

# stock_wrapper.visualize.display_stocks(['UAL', 'AAPL'])

# stock_wrapper.visualize.graph_stocks(portfolio, span='year')
# stock_wrapper.visualize.graph_analysis(Stock('BABA'))
# stock_wrapper.visualize.graph_analysis(Stock('ROST'))
# stock_wrapper.visualize.graph_analysis(Stock('TJX'))
# stock_wrapper.visualize.graph_analysis(Stock('LYFT'))
# stock_wrapper.visualize.graph_analysis(Stock('UBER'))
