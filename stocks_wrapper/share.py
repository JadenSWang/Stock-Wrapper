from . import stock, robin

import robin_stocks


class Share(stock):
    def __init__(self, ticker):
        robin.check_login()
        super().__init__(ticker)

        data = robin_stocks.build_holdings()
        if ticker not in data.keys():
            raise Exception("You don't own this stock")

    def sell(self):
        pass

    def limt_sell(self, price):
        pass

    def buy(self):
        pass

    def limit_buy(self, price):
        pass