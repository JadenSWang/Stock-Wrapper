from Classes.JSONReader import JSONReader
from API.stocks import stock_tracker
from API.stockdata import stock_data

credentials = JSONReader.read_file("Credentials.json")

stock_tracker.login(credentials['email'], credentials['password'])
stock_tracker.display_holdings(duration=-1)