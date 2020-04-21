import robin_stocks as r
import numpy as np
import tkinter as tk

import time
import csv
import threading
import sys
import curses
from datetime import datetime

# graphing
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import style

class Stocks:
    def __init__(self, username, password):
        r.login(username, password)

    def get_stocks(self):
        return r.build_holdings().items()

    def print(self):
        stocks = self.get_stocks()
        for key, value in stocks:
            print(value["name"], "(" + key + ")")
            print("\t", "Quantity         ", value["quantity"])
            print("\t", "Current Price    ", value["price"])
            print("\t", "Average Buy Price", value["price"])
            print("\t", "Equity           ", value["equity"])
            print()

    def get_history_today(self, stock):
        return r.stocks.get_historicals(stock, span='day')



    def realtime_data(self, stocks):
        class Stocks_Data_Thread (threading.Thread):
            def __init__(self, stocks):
                threading.Thread.__init__(self)
                self.stocks = stocks

            def run(self):
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()

                try:
                    for i in range(100):
                        y = 0
                        for stock in self.stocks:
                            truncated = float(int(float(r.stocks.get_latest_price(stock)[0]) * 1000) / 1000)
                            stdscr.addstr(y, 0, stock + "\t" + str(truncated))
                            y += 1
                        stdscr.refresh()
                        time.sleep(0.2)
                finally:
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()

        stocks_thread = Stocks_Data_Thread(stocks)
        stocks_thread.start()

    def graph(self, data, span='day'):
        data = self.get_history_today(data)
        dates = []
        prices = []

        for day in data:
            date = datetime.strptime(day["begins_at"], '%Y-%m-%dT%H:%M:%SZ')
            dates.append(date)

            price = day["close_price"]
            prices.append(price)

        style.use('fivethirtyeight')
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        def animate(i):
            graph_data = open('stock.txt', 'r').read()
            lines = graph_data.split('\n')

            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    x, y = line.split(',')
                    xs.append(float(x))
                    ys.append(float(y))
            ax1.clear()
            ax1.plot(xs, ys)

        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

    def get_data(self, stocks, span='day'):
        data = []
        raw_data = r.stocks.get_historicals(stocks, span)
        for time_frame in raw_data:
            begins_at, open_price, close_price, high_price, low_price, volume, session, interpolated, _ = time_frame.values()
            begins_at = datetime.strptime(begins_at, "%Y-%m-%dT%H:%M:%SZ")
            data.append([begins_at, open_price, close_price, high_price, low_price, volume, session, interpolated])

        return data
