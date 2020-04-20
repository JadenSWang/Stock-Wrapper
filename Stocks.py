import robin_stocks as r

class Stocks:
    def __init__(self, username, password):
        r.login(username, password)

    def get_stocks(self):
        return r.build_holdings().items()

    def print(self):
        stocks = self.get_stocks()
        for key, value in stocks:
            print(value["name"])
            print("\t", "Current Price", value["price"])
            print("\t", "Average Buy Price", value["price"])
            print("\t", "Equity", value["equity"])
            print()
