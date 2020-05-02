from StockTracker.Bases.Classes.base_stock import base_stock
from robin_stocks import robin_stocks


class base_share(base_stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    def sell(self):
        pass

    def limt_sell(self, price):
        pass

    def buy(self):
        pass

    def limit_buy(self, price):
        pass