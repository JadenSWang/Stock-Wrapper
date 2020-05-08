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
    def get_history(cls, ticker_symbol, calculate_averages=True, cache=True):
        """Takes in a ticker object and returns a pandas dataframe containing price,
        :param stock: single Ticker Symbol
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """
        if cache and cls.cache.exists(ticker_symbol):
            return pd.read_json(cls.cache.read_file(ticker_symbol))
        else:
            history = yfinance.Ticker(ticker_symbol).history(period='max').reset_index()
            history['Average'] = (history['High'] + history['Low']) / 2

            def __build_average(df, period):
                name = (str(period) + '_SMA')

                if len(history) > period:
                    history.loc[0:period, name] = 0

                    index = period + 1
                    while index < len(history):
                        history.iloc[index, history.columns.get_loc(name)] = history.iloc[index - period:index]['Close'].sum() / period
                        index += 1

            if calculate_averages:
                __build_average(history, 50)
                __build_average(history, 100)
                __build_average(history, 200)

            cls.cache.write_file(ticker_symbol, history.to_json())

        return history

    @classmethod
    def get_historical_prices(cls, ticker_symbol, span='day'):
        """Takes a single Ticker Symbol to build a list of tuples representing a time_frame and its respective price
        :param stock: single Ticker Symbol
        :type: str
        :param span: width of the history of the selected stock
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        history = robin_stocks.get_historicals(ticker_symbol, span=span)
        for time_frame in history:
            time_frame['begins_at'] = cls.__get_time(time_frame['begins_at'])

        historicals_df = pd.DataFrame(history).astype({'open_price': 'float32', 'close_price': 'float32'})
        historicals_df['Average'] = historicals_df.apply(lambda row: (row.open_price + row.close_price) / 2, axis=1)
        historicals_df = historicals_df.rename(columns={'begins_at':'Date', 'open_price':'Open', 'close_price':'Close', 'high_price':'High', 'low_price':'Low', 'symbol':'Symbol', 'volume':'Volume', 'session':'Session', 'interpolated':'Interpolated'})
        return historicals_df

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

    @classmethod
    def clear_cache(cls):
        cls.cache.clear()

    class cache:
        @staticmethod
        def read_file(ticker_name):
            path = os.path.abspath('__stock_cache__/' + ticker_name + '.py')
            with open(path) as json_file:
                data = json.load(json_file)

            return data

        @staticmethod
        def write_file(ticker_name, data):
            if not os.path.exists(os.path.abspath('__stock_cache__')):
                os.makedirs(os.path.abspath('__stock_cache__'))

            path = os.path.abspath('__stock_cache__/' + ticker_name + '.py')
            with open(path, 'w+') as outfile:
                json.dump(data, outfile)

        @staticmethod
        def exists(ticker_name):
            path = os.path.abspath('__stock_cache__/' + ticker_name + '.py')
            return os.path.exists(path)

        @staticmethod
        def clear():
            dirpath = os.path.abspath('__stock_cache__/')
            for path in os.listdir(dirpath):
                os.remove(os.path.abspath('__stock_cache__/' + path))
