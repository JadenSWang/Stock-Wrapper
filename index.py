from Classes.JSONReader import JSONReader
from API.stocks import stock_tracker

credentials = JSONReader.read_file("Credentials.json")
stocks = stock_tracker(credentials['email'], credentials['password'])

stocks.graph('UAL')