from Classes.JSONReader import JSONReader
from Classes.StockTracker import StockTracker
import tensorflow as tf

credentials = JSONReader.read_file("Credentials.json")
stocks = StockTracker(credentials['email'], credentials['password'])

stocks.live_graph(['SPY', 'CHGG', 'TSLA'], duration = 100)