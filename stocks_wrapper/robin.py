import robin_stocks


class robin:
    logged_in = False

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
        cls.logged_in = True

    @classmethod
    def check_login(cls):
        if not cls.logged_in:
            raise ValueError("Did you forget to login?")

    @classmethod
    def build_portfolio(cls):
        cls.check_login()
        return robin_stocks.build_holdings()

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
