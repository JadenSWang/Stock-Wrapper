import robin_stocks

import mplcursors
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
import seaborn as sns

import datetime


class stock_tracker:
    def __init__(self, username, password):
        """This is your login information, you have to log in before you can perform any sort of operation.
        This device will be validated for 86400 seconds

        :param username: The username for your robinhood account, usually your email. Not required if credentials are already cached and valid.
        :type username: str
        :param password: The password for your robinhood account. Not required if credentials are already cached and valid.
        :type username: str
        """

        robin_stocks.login(username, password)

        #graph init
        mpl.rcParams['toolbar'] = 'None'
        sns.despine()
        sns.set_style("darkgrid", {"axis.facecolor": ".9"})

    def print_holdings(self):
        """Fetches a list of owned stocks and displays them in the following format

        Name (ID)
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

    def get_historical_prices(self, stock, span='day'):
        """Takes a single stock id to build a list of tuples representing a time_frame and its respective price

        :param stock: single Stock ID
        :type: str
        :param span: width of the history of the selected stock
        :type: str
        :param time_zone: one of the global time zones,
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        historicals = []
        history = robin_stocks.get_historicals(stock, span=span)
        for time_frame in history:
            time = self.__get_time(time_frame['begins_at'])
            price = time_frame['open_price']
            historicals.append((time, float(price)))

        return historicals

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

    def graph(self, stock, span='day'):
        """Takes in a single stock id and displays a matplot graph
        :param stock:
        :param span:
        :return:
        """


        def __graph(data):
            times, prices = zip(*data)

            ax = sns.lineplot('time', 'price', data={"time": times, "price": prices})

            #final config
            ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
            mplcursors.cursor(hover=True)

        data = self.get_historical_prices(stock, span=span)
        __graph(data)
        plt.show()

    def live_graph(self, stock):
        return