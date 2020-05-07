import stock_wrapper

import robin_stocks
import pandas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import matplotlib.dates as md
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import threading
import multiprocessing as mp
import curses
import time
import datetime
import numpy as np


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
    def graph(stock, span='day'):
        """Takes in a single Ticker Symbol and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: single Stock object
        :type stock: <stock_wrapper.Stock>
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        def __graph(stock):
            data = stock.get_historical_prices()

            sns.set(style="darkgrid")
            ax = sns.lineplot('begins_at', 'average_price', data=data)

            #final config
            if span == "day":
                ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

            ax.set_title(stock.ticker + ": " + span)
            plt.xlabel("Date")
            plt.ylabel("Price ($)")

        __graph(stock)
        plt.show()

    @staticmethod
    def graph_candlestick_analysis(stocks):
        """Takes in a list of Ticker Symbols and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: list of Stock objects
        :type stock: list [<stock_wrapper.Stock>]
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        def __graph(stock, data):
            sns.set(style="darkgrid")

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Market Price'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['50_SMA'], name='50 Day Moving Average', marker_color='rgba(13, 140, 214, .8)'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['100_SMA'], name='100 Day Moving Average', marker_color='rgba(230, 223, 23, .8)'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['200_SMA'], name='200 Day Moving Average', marker_color='rgba(255, 165, 0, .8)'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume', marker_color='rgba(130, 178, 255, .8)'), secondary_y=True)

            fig.show()

        data = []
        for stock in stocks:
            data.append(stock_wrapper.data.get_history(stock.ticker, calculate_averages=True))

        for i in range(len(data)):
            __graph(stocks[i], data[i])

    @staticmethod
    def graph_trendline_analysis(stocks):
        """Takes in a list of Ticker Symbols and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: list of Stock objects
        :type stock: list [<stock_wrapper.Stock>]
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        def __graph(stock, data):
            sns.set(style="darkgrid")

            plt.figure()
            ax = sns.lineplot(x="Date", y="High", color='#82b2ff', data=data)
            sns.lineplot(x="Date", y="Low", color='#82b2ff', data=data)
            sns.lineplot(x="Date", y="50_SMA", color='#0d5ad6', data=data)
            sns.lineplot(x="Date", y="100_SMA", color='#e6df17', data=data)
            sns.lineplot(x="Date", y="200_SMA", color='#ffa500', data=data)

            average_patch = mpatches.Patch(color='#82b2ff', label='Average Price')
            sma_50_patch = mpatches.Patch(color='#0d5ad6', label='50 Day Moving Average')
            sma_100_patch = mpatches.Patch(color='#e6df17', label='100 Day Moving Average')
            sma_200_patch = mpatches.Patch(color='#ffa500', label='200 Day Moving Average')
            plt.legend(handles=[average_patch, sma_50_patch, sma_100_patch, sma_200_patch])

            ax.set_title(stock.ticker)
            plt.gcf().canvas.set_window_title(stock.ticker)
            plt.xlabel("Date")
            plt.ylabel("Price ($)")

        data = []
        for stock in stocks:
            data.append(stock_wrapper.data.get_history(stock.ticker, calculate_averages=True))

        for i in range(len(data)):
            __graph(stocks[i], data[i])

        plt.show()

    @staticmethod
    def graph_stocks(stock_objects, span='day'):
        """Takes in a list of and optional span. Displays a matplot graph with the history of that stock, default span to one day
        :param stock: list of Stock objects
        :type stock: list <stock_wrapper.Stock>
        :param span: how far back the graph should span for
        :type span: str, ['day', 'week', 'month', '3month', 'year']
        """

        f, axes = plt.subplots(int(np.ceil(len(stock_objects) / 3)), 3, figsize=(8, 6))

        def __graph(data, row, col, axes):
            chart = sns.lineplot('begins_at', 'average_price', data=data, ax=axes[row, col])
            chart.set_xlabel("Date")
            plt.setp(chart.get_xticklabels(), rotation=45)
            # chart.set_xticklabels(chart.get_xticklabels(), rotation=5, horizontalalignment='right')
            chart.set_ylabel("Price ($)")

            #final config
            if span == "day":
                chart.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

        i = 0
        for row in range(int(np.ceil(len(stock_objects) / 3))):
            for col in range(3):
                if i < len(stock_objects):
                    axes[row][col].set_title(stock_objects[i].ticker)
                    __graph(stock_objects[i].get_historical_prices(span=span), row, col, axes)
                i += 1

        # chart config
        sns.despine(left=True)
        sns.set(style="dark")

        plt.show()