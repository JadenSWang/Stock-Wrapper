from Classes.JSONReader import JSONReader
from StockTracker.stocks import stock_tracker

credentials = JSONReader.read_file("Credentials.json")
stock_tracker.robin.login(credentials['email'], credentials['password'])
print(stock_tracker.robin.build_portfolio())
