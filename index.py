from Classes.JSONReader import JSONReader
from StockTracker.stocks import Stock
from StockTracker.stocks import Share
from StockTracker.stocks import stock_tracker

credentials = JSONReader.read_file("Credentials.json")
stock_tracker.robin.login(credentials['email'], credentials['password'])

# robin
print(stock_tracker.robin.build_portfolio())

#visualize
united_share = Share('UAL')
apple = Stock('AAPL')

print(united_share.price)

#data
