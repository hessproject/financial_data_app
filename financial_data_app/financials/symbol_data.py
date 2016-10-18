from pandas_datareader import data as web
from pandas_datareader import wb
import plotly
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import traceback
import requests

def get_stock_data(symbols, start=datetime(2015,1,1), end=datetime(2016,1,1), adjust_price=False, interval='d'):
    '''
    :param symbols: (str or list) One or a list of stock symbols to look up
    :param start: (str or datetime) The start date for the returned stock data
    :param end: (str or datetime) The end date for the returned stock data
    :param adjust_price: (boolean) Adjust all historical prices
    :param interval: (str) 'd' - daily, 'w' - weekly, m -'monthly'

    :return: a pandas Panel of stock information, with "company" as the item, "dates" as the major axis, and stock info ('close' 'open' 'high' 'low' 'adj close') as the minor axis
    '''

    for symbol in symbols:
        print('symbols: ' + symbol)

    try:
        print('entering try')
        f = web.get_data_yahoo(symbols=symbols, start=start, end=end, adjust_price=adjust_price, interval=interval)
        return f.transpose(2,1,0)
    except Exception as e:
        raise e
        return


def get_company_info(query):
    '''
    :param query: a search query for a stock symbol or company
    :return: Company name, stock symbol, and exchange traded on for the query if found
    '''
    url = 'http://dev.markitondemand.com/Api/v2/Lookup/json'
    if type(query) is not str:
        raise TypeError("Not a valid search query")

    payload = {
        'input': query.strip()
    }

    try:
        r = requests.get(url, params=payload)
        return r.json()
    except Exception as e:
        raise e