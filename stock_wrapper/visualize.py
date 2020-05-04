import stock_wrapper

import robin_stocks
import pandas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
import seaborn as sns

import threading
import curses
import time


class visualize:
    @staticmethod
    def display_stocks(stocks_to_monitor, duration=100):
        """Turns the command shell executing into a ticker display
        :param stocks_to_monitor: any stocks you want to watch
        :type stocks_to_monitor: list [str]
        :param duration: duration in seconds, -1 for infinite
        :type duration: int
        """
        if len(stocks_to_monitor) < 1:
            return

        class Stocks_Data_Thread(threading.Thread):
            def __init__(self, stocks_to_monitor, duration=100):
                threading.Thread.__init__(self)
                self.stocks_to_monitor = stocks_to_monitor
                self.duration = duration

            def run(self):
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()

                try:
                    i = 0
                    while duration == -1 or i < duration * 20:
                        y = 0
                        for stock in self.stocks_to_monitor:
                            to_print = stock + "\t" + str(self.__get_stock_price(stock))
                            stdscr.addstr(y, 0, to_print)
                            y += 1

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

        Stocks_Data_Thread(stocks_to_monitor, duration).start()

    @staticmethod
    def display_holdings(extra_stocks_to_monitor=[], duration=100, show_quantity=False, show_equity=False):
        """Turns the command shell executing into a ticker display
        :param extra_stocks_to_monitor: any extra stocks you want towatch
        :type extra_stocks_to_monitor: list [str]
        :param duration: duration in seconds, -1 for infinite
        :type duration: int
        """
        class Stocks_Data_Thread(threading.Thread):
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
        if len(holdings) < 1:
            return

        Stocks_Data_Thread(holdings.keys(), show_quantity, show_equity, extra_stocks_to_monitor, duration).start()

    @staticmethod
    def graph(ticker_symbol, span='day'):
        """Takes in a single Ticker Symbol and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: single Ticker Symbol
        :type stock: str
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        def __graph(data):
            sns.set(style="darkgrid")
            ax = sns.lineplot('begins_at', 'average_price', data=data)

            #final config
            if span == "day":
                ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

        data = stock_wrapper.data.get_historical_prices(ticker_symbol, span=span)
        __graph(data)
        plt.show()