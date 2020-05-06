import stock_wrapper

import robin_stocks


class Shares(stock_wrapper.Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    def sell(self, quantity):
        robin_stocks.orders.order_sell_market(self.ticker, quantity)

    def limt_sell(self, quantity, price):
        robin_stocks.orders.order_sell_limit(self.ticker, quantity, price)

    def buy(self, quantity):
        robin_stocks.orders.order_buy_market(self.ticker, quantity)

    def limit_buy(self, quantity, price):
        robin_stocks.orders.order_buy_limit(self.ticker, quantity, price)

    @property
    def equity(self):
        stocks_data = robin_stocks.account.get_current_positions()
        stock_data = self.__get_stock_from_positions_list(self.ticker, stocks_data)

        return float(stock_data['quantity']) * self.price

    @staticmethod
    def __get_stock_from_positions_list(ticker, list):
        for stock in list:
            if robin_stocks.get_symbol_by_url(stock['instrument']) == ticker:
                return stock
