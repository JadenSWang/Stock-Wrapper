from Classes.JSONReader import JSONReader
from Classes.StockTracker import StockTracker
import tensorflow as tf

credentials = JSONReader.read_file("Credentials.json")
stocks = StockTracker(credentials['email'], credentials['password'])

# stocks.print()
stocks.graph(span='year')
stocks.live_graph()
# stocks.live_print(['SPY', 'CHGG', 'TSLA'], duration = 100)
# stocks.live_graph(['SPY', 'CHGG', 'TSLA'], duration = 100)
