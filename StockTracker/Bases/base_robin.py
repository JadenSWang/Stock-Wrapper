import robin_stocks

import curses
import threading
import time
import datetime


class base_robin:
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
    def limit_buy_stock(cls):
        pass

    @classmethod
    def limit_sell_stock(cls):
        pass