import yfinance
import stock_wrapper


class Stock():
    """
    All data is cached within the object
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.update()

    def __str__(self):
        return self.ticker

    def update(self):
        self.company_info = yfinance.Ticker(self.ticker).info

    def get_historical_prices(self, span='day'):
        return stock_wrapper.data.get_historical_prices(self.ticker, span=span)

    @property
    def history(self):
        return stock_wrapper.data.get_history(self.ticker)

    @property
    def price(self):
        """
        Average Latest Price
        """
        data_this_minute = self.__get_current_price_data()
        return float((data_this_minute['Close'] + data_this_minute['Open']) / 2)

    @property
    def open(self):
        """
        Latest Open Price
        """
        return float(self.__get_current_price_data()['Open'])

    @property
    def close(self):
        """
        Latest Closing Price
        """
        return float(self.__get_current_price_data()['Close'])

    @property
    def high(self):
        """
        Highest Price Today
        """
        return float(self.__get_current_price_data()['High'])

    @property
    def low(self):
        """
        Lowest Price Today
        """
        return float(self.__get_current_price_data()['Low'])

    def __get_current_price_data(self):
        return yfinance.Ticker(self.ticker).history(period='day', interval='1m').iloc[[-1]]

    @property
    def low_52_weeks(self):
        """
        Lowest Price Within 52 Weeks
        """
        return self.company_info['fiftyTwoWeekLow']

    @property
    def high_52_weeks(self):
        """
        Highest Price Within 52 Weeks
        """
        return self.company_info['fiftyTwoWeekHigh']

    @property
    def market_cap(self):
        """
        Current Market Cap (Company Value)
        """
        return self.company_info['marketCap']

    @property
    def volume(self):
        """
        Average Market Volume
        """
        return self.company_info['averageVolume']

    @property
    def sector(self):
        """
        Comppany Sector
        """
        return self.company_info['sector']

    @property
    def industry(self):
        """
        Company Industry
        """
        return self.company_info['industry']

    @property
    def shares_outstanding(self):
        """
        Total Number of shares
        """
        return self.company_info['sharesOutstanding']

    @property   
    def num_employees(self):
        """
        Reported Number of Full Time Employees
        """
        return self.company_info['fullTimeEmployees']

    @property
    def hq_city(self):
        """
        City which the Company is Headquartered in
        """
        return self.company_info['city']

    @property
    def hq_state(self):
        """
        State which the Company is Headquartered in
        """
        return self.company_info['state']

    @property
    def hq_country(self):
        """
        Country which the Company is Headquartered in
        """
        return self.company_info['country']

    @property
    def hq_zip(self):
        """
        Zip code which the Company is Headquartered in
        """
        return self.company_info['zip']

    #contact information
    @property
    def website(self):
        """
        Offical Company Website
        """
        return self.company_info['website']

    @property
    def hq_address(self):
        """
        Full Address Which the Company is Headquartered in. Number Street City State Zip-Code Country
        """
        return self.company_info['address1']  + " " + self.hq_city  + " " + self.hq_state + " " + self.hq_zip+ " " + self.hq_country 

    @property
    def phone(self):
        """
        Company Primary Phone Number
        """
        return self.company_info['phone']

    @property
    def logo(self):
        """
        URL to Company Logo
        """
        return self.company_info['logo_url']

    @property
    def description(self):
        """
        Long Company Description
        """
        return self.company_info['longBusinessSummary']

    