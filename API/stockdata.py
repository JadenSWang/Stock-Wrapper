import quandl
import datetime

class stock_data:
    @staticmethod
    def login(api_key):
        quandl.ApiConfig.api_key = api_key

    @staticmethod
    def get_features(ticker_symbol, features=[], start_date='today', end_date='today'):
        """Generates a list of dictionaries containing features specified in the optional features parameter, no parameter will result in only the price

        :param ticker_symbol: Official ticker symbol of the specified company
        :type ticker_symbol: str
        :param features: list of strings containing the strings
        :type features: Optional[list
        :param start_date: Begin date to search
        :type start_date: Optional[str] 'yyyy-mm--dd'
        :param end_date: End date to search
        :type end_date: Optional[str] 'yyyy-mm--dd'
        :return: list of dictionaries containing features of the specified symbol
        """

        if start_date == 'today':
            start_date = datetime.datetime.today().date()

        if end_date == 'today':
            end_date = datetime.datetime.today().date()
            
