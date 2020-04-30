import robin_stocks

import mplcursors
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
import seaborn as sns

import datetime

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

            ax = sns.lineplot('time', 'price', data={"time": times, "price": prices})

            #final config
            ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
            mplcursors.cursor(hover=True)

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
