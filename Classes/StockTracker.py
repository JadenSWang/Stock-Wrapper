import robin_stocks as r

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

import threading
import curses
import time


class StockTracker:
    def __init__(self, username, password):
        r.login(username, password)

    def print(self):
        stocks = r.build_holdings().items()
        for key, value in stocks:
            print(value["name"], "(" + key + ")")
            print("\t", "Quantity         ", value["quantity"])
            print("\t", "Current Price    ", value["price"])
            print("\t", "Average Buy Price", value["price"])
            print("\t", "Equity           ", value["equity"])
            print()

    def graph(self):
        stock = 'UAL'

        data = {"time": [0], "price": [100]}
        sns.lineplot('time', 'price', data=data, linestyle='-', marker='o')
        plt.show()

    def live_print(self, stocks_to_monitor=[], duration=100):
        class Stocks_Data_Thread (threading.Thread):
            def __init__(self, stocks, stocks_to_monitor=[], duration=100):
                threading.Thread.__init__(self)
                self.stocks = stocks
                self.stocks_to_monitor = stocks_to_monitor
                self.duration = duration

            def run(self):
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()

                try:
                    for i in range(duration * 20):
                        y = 0
                        for stock in self.stocks:
                            stdscr.addstr(y, 0, stock + "\t" + str(self.__get_stock_price(stock)))
                            y += 1

                        if len(self.stocks_to_monitor) > 0:
                            y += 1

                            for stock in self.stocks_to_monitor:
                                if stock not in self.stocks:
                                    stdscr.addstr(y, 0, stock + "\t" + str(self.__get_stock_price(stock)))
                                    y += 1
                            stdscr.refresh()
                            time.sleep(0.05)

                finally:
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()

            @staticmethod
            def __get_stock_price(stock, rounding=1000):
                return float(int(float(r.stocks.get_latest_price(stock)[0]) * rounding) / rounding)

        holdings = r.account.build_holdings()
        Stocks_Data_Thread(holdings.keys(), stocks_to_monitor, duration).start()

    def live_graph(self, stocks_to_monitor = [], duration = 100):
        def graph(fig, stock, animations=[]):
            ax1 = fig.add_subplot(1,1,1)

            def animate(i):
                x_axis = []
                y_axis = []

                historical = r.stocks.get_historicals(stock)
                for time in historical:
                    date = time['begins_at']
                    price = time['open_price']

                    x_axis.append(date)
                    y_axis.append(price)

                ax1.clear()
                ax1.plot(x_axis, y_axis)

            animations.append(animation.FuncAnimation(fig, animate, interval=10000))
            plt.show()


        animations = []
        holdings = r.account.build_holdings()
        graph(plt.figure(), 'UAL', animations)
        graph(plt.figure(), 'TSLA', animations)
        # for stock in holdings.keys():
        #     graph(stock)
            # threading.Thread(target=graph, args=(stock,)).start()

        # for stock in stocks_to_monitor:
        #     if stock not in holdings.keys():
        #         threading.Thread(target=graph, args=(stock,)).start()

    def __live_graph(self, stocks_to_monitor = [], duration = 100):
        class Load_Stock_To_File(threading.Thread):
            def __init__(self, stock):
                threading.Thread.__init__(self)
                self.stock = stock

            def run(self):
                while True:
                    data_source = open('StockData/' + self.stock + '.txt', 'w+')
                    data_source.write()
                    print(r.stocks.get_historicals(self.stock, span='day'))
                return

        #loading data
        stock_loading_threads = []
        holdings = r.account.build_holdings()
        for stock in holdings.keys():
            stock_thread = Load_Stock_To_File(stock)
            stock_thread.start()
            stock_loading_threads.append(stock_thread)

        for stock in stocks_to_monitor:
            if stock not in holdings.keys():
                stock_thread = Load_Stock_To_File(stock)
                stock_thread.start()
                stock_loading_threads.append(stock_thread)

        #graphing
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        def animate(i):
            data_source = open('stockdata.txt', 'r').read()
            data_array = data_source.split('\n')

            x_axis = []
            y_axis = []

            for line in data_array:
                if len(line) > 1:
                    x, y = line.split(',')
                    x_axis.append(int(x))
                    y_axis.append(int(y))

            ax1.clear()
            ax1.plot(x_axis, y_axis)

        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()
