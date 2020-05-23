import stock_wrapper

import yfinance
import robin_stocks
import pandas as pd
import os
import numpy as np

import json
import datetime

class data:
    __switcher = {
        'day': '1d',
        'week': '5d',
        'month': '1mo',
        '3month': '3mo',
        'year': '1y',
        'max': 'max'
    }

    @classmethod
    def get_history(cls, tickers, span='day', interval='1m', calculate_averages=[''], averages_to_calculate=[10, 20],  cache=False, extended=False):
        """Takes in a ticker object and returns a pandas dataframe containing price,
        :param tickers: Single Ticker object or list of Ticker objects
        :type tickers: str
        :param span: How much data to retrieve
        :type span: str, [day, week, month, 3month, year, max]
        :param interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :type interval: str
        :param calculate_averages: Whether or not to calculate moving averages
        :type calculate_averages: bool
        :param cache: whether or not to retrieve/store in cache
        :type cache: bool
        :return: pandas dataframe
        """

        if not isinstance(tickers, list):
            tickers = [tickers]

        ticker_symbols = ''
        for ticker in tickers:
            if isinstance(ticker, stock_wrapper.Stock):
                ticker_symbols += ticker.ticker + ' '
            else:
                ticker_symbols += ticker + ' '
        ticker_symbols = ticker_symbols[:-1]

        # downloaded history
        history = yfinance.download(tickers=ticker_symbols, period=cls.__switcher[span], group_by='ticker', prepost=extended, interval=interval).reset_index()

        ticker_symbols = ticker_symbols.split(" ")
        if calculate_averages:
            for symbol in ticker_symbols:
                history[symbol, "Average"] = (history[symbol]['High'] + history[symbol]['Low']) / 2

                def __build_average(period):
                    name = ('SMA_' + str(period))
                    history[(symbol, name)] = history[symbol]['Close'].rolling(period).mean()

                for average in averages_to_calculate:
                    if not isinstance(average, int):
                        raise Exception("Averages are numbers of days and must be of type int")

                    __build_average(average)

                # if history.columns.values[0] != 'Date':
                #     headers = history.columns.values
                #     headers[0] = 'Date'
                #     history.columns = headers

        return history

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

    @classmethod
    def clear_cache(cls):
        cls.cache.clear()

    class cache:
        @classmethod
        def read_file(cls, ticker_name, span, interval):
            path = cls.__get_path(ticker_name, span, interval)
            with open(path) as json_file:
                data = json.load(json_file)

            return data

        @classmethod
        def write_file(cls, ticker_name, span, interval, data):
            if not os.path.exists(os.path.abspath('__stock_cache__')):
                os.makedirs(os.path.abspath('__stock_cache__'))

            path = cls.__get_path(ticker_name, span, interval)
            with open(path, 'w+') as outfile:
                json.dump(data, outfile)

        @classmethod
        def exists(cls, ticker_name, span, interval):
            path = cls.__get_path(ticker_name, span, interval)
            return os.path.exists(path)

        @staticmethod
        def clear():
            if os.path.exists(os.path.abspath('__stock_cache__')):
                dirpath = os.path.abspath('__stock_cache__/')
                for path in os.listdir(dirpath):
                    os.remove(os.path.abspath('__stock_cache__/' + path))

        @classmethod
        def __get_path(cls, ticker_name, span, interval):
            return os.path.abspath('__stock_cache__/' + ticker_name + '_' + span + '_' + interval + '.py')