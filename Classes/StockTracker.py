import robin_stocks as r

import threading
import curses
import time

class StockTracker:
    def __init__(self, username, password):
        r.login(username, password)

    def print(self):
        holdings = r.account.build_holdings()
        print(holdings)

    def live_print(self, stocks_to_monitor=[], duration=100):
        class Stocks_Data_Thread (threading.Thread):
            def __init__(self, stocks, stocks_to_monitor=[], duration=100):
                threading.Thread.__init__(self)
                self.stocks = stocks
                self.stocks_to_monitor = stocks_to_monitor
                self.duration = duration

            @staticmethod
            def get_price(stock):
                return float(int(float(r.stocks.get_latest_price(stock)[0]) * 1000) / 1000)

            def run(self):
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()

                try:
                    for i in range(duration * 20):
                        y = 0
                        for stock in self.stocks:
                            stdscr.addstr(y, 0, stock + "\t" + str(Stocks_Data_Thread.get_price(stock)))
                            y += 1

                        if len(self.stocks_to_monitor) > 0:
                            stdscr.addstr(y, 0, "=======================================")
                            y += 1

                            for stock in self.stocks_to_monitor:
                                if stock not in self.stocks:
                                    stdscr.addstr(y, 0, stock + "\t" + str(Stocks_Data_Thread.get_price(stock)))
                                    y += 1
                            stdscr.refresh()
                            time.sleep(0.05)

                finally:
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()

        holdings = r.account.build_holdings()
        Stocks_Data_Thread(holdings.keys(), stocks_to_monitor, duration).start()

    def live_graph(self, stocks_to_monitor=[]):
        return