from Classes.JSONReader import JSONReader
import stock_wrapper
from stock_wrapper import Stock
import multiprocessing

credentials = JSONReader.read_file("Credentials.json")
stock_wrapper.robin.login(credentials['email'], credentials['password'])

# stock_wrapper.visualize.display_stocks(['UAL', 'AAPL'])

portfolio = stock_wrapper.robin.build_portfolio()
print(portfolio)
portfolio = [Stock('UAL'), Stock('TSLA'), Stock('DAL'), Stock('TJX'), Stock('BABA')]
print(portfolio)
# stock_wrapper.visualize.graph_stocks(portfolio, span='week')
stock_wrapper.visualize.graph(Stock('CHGG'), span='year')