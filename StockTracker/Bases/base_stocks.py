import yfinance
import robin_stocks


class base_stock:
    def __init__(self, ticker):
        self.ticker = ticker

        self.fundamentals = robin_stocks.get_fundamentals(self.ticker)[0]

    @classmethod
    def reload_cache(cls):
        cls.fundamentals = robin_stocks.get_fundamentals(cls.ticker)[0]

    @property
    def price(self):
        return float(robin_stocks.stocks.get_latest_price(self.ticker)[0])

    @property
    def open(self):
        """
        :return: latest open price
        """
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['open'])

    @property
    def close(self):
        """
        :return: latest closing price
        """
        return float(robin_stocks.stocks.get_historicals(self.ticker, span='day')[0]['close_price'])

    @property
    def low(self):
        """
        :return: lowest price today
        """
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['low'])

    @property
    def low_52_weeks(self):
        """
        :return: highest price this year
        """
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['low_52_weeks'])

    @property
    def high(self):
        """
        :return: highest price today
        """
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['high'])

    @property
    def high_52_weeks(self):
        """
        :return: highest price this year
        """
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['high_52_weeks'])

    @property
    def market_cap(self):
        return float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['market_cap'])

    @property
    def volume(self):
        """
        :return: average market volume
        """
        return int(float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['volume']))

    @property
    def volume_2_weeks(self):
        """
        :return: average market volume from past two weeks
        """
        return int(float(robin_stocks.stocks.get_fundamentals(self.ticker)[0]['average_volume_2_weeks']))

    @property
    def ceo(self):
        return robin_stocks.stocks.get_fundamentals(self.ticker)[0]['ceo']

    @property
    def sector(self):
        return self.fundamentals['sector']

    @property
    def industry(self):
        return robin_stocks.stocks.get_fundamentals(self.ticker)[0]['industry']

    @property
    def shares_outstanding(self):
        return robin_stocks.stocks.get_fundamentals(self.ticker)[0]['shares_outstanding']

    @property
    def num_employees(self):
        return robin_stocks.stocks.get_fundamentals(self.ticker)[0]['num_employees']

    @property
    def hq_city(self):
        return self.fundamentals['headquarters_city']

    @property
    def hq_state(self):
        return self.fundamentals['headquarters_state']

    @property
    def description(self):
        return self.fundamentals['description']

    @property
    def year_founded(self):
        return self.fundamentals['year_founded']
