from StockTracker.Bases.base_stock_tracker import base_stock_tracker
from StockTracker.Bases.base_robin import base_robin
from StockTracker.Bases.base_data import base_data
from StockTracker.Bases.base_visualize import base_visualize
from StockTracker.Bases.base_stocks import base_stock


class stock_tracker(base_stock_tracker):
    def __init__(self):
        pass

    class robin(base_robin):
        def __init__(self):
            pass

    class data(base_data):
        def __init__(self):
            pass

    class visualize(base_visualize):
        def __init__(self):
            pass

class Stock(base_stock):
    def __init__(self, ticker_symbol):
        super().__init__(ticker_symbol)
