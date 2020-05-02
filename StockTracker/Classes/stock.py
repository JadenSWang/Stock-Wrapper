import yfinance


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

    @property
    def price(self):
        return yfinance.Ticker(self.ticker).info['ask']

    @property
    def open(self):
        return yfinance.Ticker(self.ticker).info['open']

    @property
    def previous_close(self):
        return yfinance.Ticker(self.ticker).info['previousClose']

    @property
    def test(self):
        return yfinance.Ticker(self.ticker).info


