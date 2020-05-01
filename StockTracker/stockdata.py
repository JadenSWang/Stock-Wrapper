import robin_stocks

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
import seaborn as sns

import datetime
import threading
import curses
import time

import yfinance as yf


class stock_tracker:
    @staticmethod
    def login(username, password):
        """This is your login information, you have to log in before you can perform any sort of operation.
        This device will be validated for 86400 seconds

        :param username: The username for your robinhood account, usually your email. Not required if credentials are already cached and valid.
        :type username: str
        :param password: The password for your robinhood account. Not required if credentials are already cached and valid.
        :type username: str
        """
        #init
        robin_stocks.login(username, password)

        #graph init
        mpl.rcParams['toolbar'] = 'None'
        sns.despine()
        sns.set_style("darkgrid", {"axis.facecolor": ".9"})

    @staticmethod
    def print_holdings():
        """Fetches a list of owned stocks and displays them in the following format

        Name (Ticker Symbol)
            Quantity\n
            Current Price\n
            Average Buy Price\n
            Equity
        """

        holdings = robin_stocks.build_holdings().items()

        for key, value in holdings:
            print(value["name"], "(" + key + ")")
            print("\t", "Quantity         ", value["quantity"])
            print("\t", "Current Price    ", value["price"])
            print("\t", "Average Buy Price", value["price"])
            print("\t", "Equity           ", value["equity"])
            print()

    @staticmethod
    def display_holdings(stocks_to_monitor=[], duration=100, show_quantity=False, show_equity=False):
        """Turns the command shell executing into a ticker display
        :param stocks_to_monitor: any extra stocks you want to
        :param duration: duration in seconds, -1 for infinite
        :type duration: int
        """
        class Stocks_Data_Thread (threading.Thread):
            def __init__(self, stocks, show_quantity, show_equity, stocks_to_monitor=[], duration=100):
                threading.Thread.__init__(self)
                self.stocks = stocks
                self.stocks_to_monitor = stocks_to_monitor
                self.duration = duration

                self.show_quantity = show_quantity
                self.show_equity = show_equity

            def run(self):
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()

                try:
                    holdings = robin_stocks.build_holdings()

                    i = 0
                    while duration == -1 or i < duration * 20:
                        y = 0
                        for stock in self.stocks:
                            to_print = stock + "\t" + str(self.__get_stock_price(stock))

                            if self.show_quantity:
                                to_print += "\t" + str(int(float(holdings[stock]['quantity'])))

                            if self.show_equity:
                                to_print += "\t" + str(float(holdings[stock]['equity']))
                            stdscr.addstr(y, 0, to_print)
                            y += 1

                        if 0 < len(self.stocks_to_monitor):
                            y += 1
                            for stock in self.stocks_to_monitor:
                                if stock not in self.stocks:
                                    stdscr.addstr(y, 0, stock + "\t" + str(self.__get_stock_price(stock)))

                        stdscr.refresh()
                        time.sleep(0.05)
                        i += 1

                finally:
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()

            @staticmethod
            def __get_stock_price(stock, rounding=1000):
                return float(int(float(robin_stocks.stocks.get_latest_price(stock)[0]) * rounding) / rounding)

        holdings = robin_stocks.account.build_holdings()
        Stocks_Data_Thread(holdings.keys(), show_quantity, show_equity, stocks_to_monitor, duration).start()

    @staticmethod
    def get_historical_prices(ticker_symbol, span='day'):
        """Takes a single Ticker Symbol to build a list of tuples representing a time_frame and its respective price
        :param stock: single Ticker Symbol
        :type: str
        :param span: width of the history of the selected stock
        :type: str
        :param time_zone: one of the global time zones,
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        historicals = []
        history = robin_stocks.get_historicals(ticker_symbol, span=span)
        for time_frame in history:
            time = stock_tracker.__get_time(time_frame['begins_at'])
            price = time_frame['open_price']
            historicals.append((time, float(price)))

        return historicals

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

    @staticmethod
    def graph(ticker_symbol, span='day'):
        """Takes in a single Ticker Symbol and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: single Ticker Symbol
        :type stock: str
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        def __graph(data):
            times, prices = zip(*data)

            ax = sns.regplot('time', 'price', data={"time": times, "price": prices})
            # ax = sns.lineplot('time', 'price', data={"time": times, "price": prices})

            #final config
            if span == "day":
                ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

        data = stock_tracker.get_historical_prices(ticker_symbol, span=span)
        __graph(data)
        plt.show()

    @staticmethod
    def live_graph(ticker_symbol, span='day'):
        """Takes in a single Ticker Symbol and optional span. Displays a matplot graph with the history of that stock and updates it live. Ideal for displays, default span to one day
        :param stock: single Ticker Symbol
        :type stock: str
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """
        return

    class data:
        @staticmethod
        def get_data(ticker_symbol):
            return yf.Ticker(ticker_symbol).info