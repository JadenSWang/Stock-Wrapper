import yfinance
import stock_wrapper


class Stock():
    def __init__(self, ticker):
        self.ticker = ticker
        self.reload_info()

    def __str__(self):
        return self.ticker

    def reload_info(self):
        self.company_info = yfinance.Ticker(self.ticker).info

    def get_historical_prices(self, span='day'):
        return stock_wrapper.data.get_historical_prices(self.ticker, span=span)

    @property
    def history(self):
        return stock_wrapper.data.get_history(self.ticker)

    @property
    def price(self):
        data_this_minute = self.__get_current_price_data()
        return float((data_this_minute['Close'] + data_this_minute['Open']) / 2)

    @property
    def open(self):
        """
        :return: latest open price
        """
        return float(self.__get_current_price_data()['Open'])

    @property
    def close(self):
        """
        :return: latest closing price
        """
        return float(self.__get_current_price_data()['Close'])

    @property
    def high(self):
        """
        :return: highest price today
        """
        return float(self.__get_current_price_data()['High'])

    @property
    def low(self):
        """
        :return: lowest price today
        """
        return float(self.__get_current_price_data()['Low'])

    def __get_current_price_data(self):
        return yfinance.Ticker(self.ticker).history(period='day', interval='1m').iloc[[-1]]

    @property
    def low_52_weeks(self):
        """
        :return: highest price this year
        """
        return self.company_info['fiftyTwoWeekLow']

    @property
    def high_52_weeks(self):
        """
        :return: highest price this year
        """
        return self.company_info['fiftyTwoWeekHigh']

    @property
    def market_cap(self):
        return self.company_info['marketCap']

    @property
    def volume(self):
        """
        :return: average market volume
        """
        return self.company_info['averageVolume']

    @property
    def sector(self):
        return self.company_info['sector']

    @property
    def industry(self):
        return self.company_info['industry']

    @property
    def shares_outstanding(self):
        return self.company_info['sharesOutstanding']

    @property
    def num_employees(self):
        return self.company_info['fullTimeEmployees']

    @property
    def hq_city(self):
        return self.company_info['city']

    @property
    def hq_state(self):
        return self.company_info['state']

    @property
    def hq_country(self):
        return self.company_info['country']

    #contact information
    @property
    def website(self):
        return self.company_info['website']

    @property
    def website(self):
        return self.company_info['website']

    @property
    def address(self):
        return self.company_info['address1']

    @property
    def phone(self):
        return self.company_info['phone']

    @property
    def logo(self):
        return self.company_info['logo_url']

    @property
    def description(self):
        return self.company_info['longBusinessSummary']

