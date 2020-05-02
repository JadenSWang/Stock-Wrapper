from Classes.JSONReader import JSONReader
from StockTracker.stocks import stock_tracker

from StockTracker.Classes.stock import Stock

credentials = JSONReader.read_file("Credentials.json")
stock_tracker.robin.login(credentials['email'], credentials['password'])

# robin
# print(stock_tracker.robin.build_portfolio())
# stock_tracker.robin.print_portfolio()

#visualize
stock = Stock('UAL')
stock_data = stock.test
print(stock_data)
stock_data = stock.price
print(stock_data)
stock_data = stock.open
print(stock_data)
stock_data = stock.previous_close
print(stock_data)

#data
