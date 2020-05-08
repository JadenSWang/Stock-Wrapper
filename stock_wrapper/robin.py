import stock_wrapper
import robin_stocks


class robin:
    @classmethod
    def login(cls, username, password):
        """This is your login information, you have to log in before you can perform any sort of operation.
        This device will be validated for 86400 seconds

        :param username: The username for your robinhood account, usually your email. Not required if credentials are already cached and valid.
        :type username: str
        :param password: The password for your robinhood account. Not required if credentials are already cached and valid.
        :type username: str
        """
        # init
        robin_stocks.login(username, password)

    @classmethod
    def build_portfolio(cls):
        """
        :return:
        """
        shares = []
        for ticker in robin_stocks.build_holdings().keys():
            shares.append(stock_wrapper.Shares(ticker))

        return shares

    @classmethod
    def build_watchlist(cls):
        """
        :return:
        """
        shares = []
        for ticker in robin_stocks.account.get_watchlist_by_name():
            shares.append(stock_wrapper.Shares(robin_stocks.get_instrument_by_url(ticker['instrument'])['symbol']))

        return shares

    @classmethod
    def print_portfolio(cls):
        """Fetches a list of owned stocks and displays them in the following format

        Name (Ticker Symbol)
            Quantity\n
            Current Price\n
            Average Buy Price\n
            Equity
        """
        holdings = cls.build_portfolio().items()

        for key, value in holdings:
            print(value["name"], "(" + key + ")")
            print("\t", "Quantity         ", value["quantity"])
            print("\t", "Current Price    ", value["price"])
            print("\t", "Average Buy Price", value["price"])
            print("\t", "Equity           ", value["equity"])
            print()