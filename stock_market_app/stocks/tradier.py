import sys
import json
import requests
import pprint as pp

endpoint = 'https://sandbox.tradier.com/v1/'

#Helper Functions
def join_args(*args):
    return " ".join([str(arg) for arg in args])


def get_api_key():
    key = None

    try:
        with open('tradier.key', 'r') as f:
            key = f.readline()
    except:
        raise IOError('tradier.key file not found')

    return key

default_key = get_api_key()
default_headers = {'Authorization': "Bearer " + default_key,
                   'Accept': 'application/json'}


# Functions for retrieving market information
def find_company(search_terms):
    '''
    :param search_terms: The name of the company you wish to find information on

    :return: JSON containing information about the company
    '''
    query = join_args(search_terms)
    url = endpoint + 'markets/search'

    payload = {'q' : query,
               'indexes': 'false'}

    try:
        r = requests.get(url, params=payload, headers=default_headers)

        return r.json()

    except:
        print('Error searching for company')


def get_historical_pricing(symbol, start_date, end_date, interval='daily'):
    '''
    :param symbol: The symbol of the stock you wish to get pricing for

    :param start_date: The beginning of the daterange you wish to search

    :param end_date: The end of the daterange you wish to search

    :param interval: If you want daily, weekly, or monthly data (optional, default= daily)

    :return: JSON containing historical pricing data
    '''
    url = endpoint + 'markets/history'
    payload = {'symbol': symbol,
               'start': start_date,
               'end': end_date,
               'interval': interval}

    try:
        r = requests.get(url, params=payload, headers=default_headers)

        return r.json()

    except json.decoder.JSONDecodeError as e:
        print(e)
        raise

    except TypeError as e:
        print(e)
        raise

    except Exception as e:
        print(e)
        raise


def get_current_quote(symbols):
    '''
    :param symbols: The symbols for the you wish to get a quote for (equity and option symbols accepted). For multiple symbols delimit with a comma

    :return: JSON containing quote information for one or many symbols
    '''
    url = endpoint + 'markets/quotes'

    try:
        r = requests.get(url, headers=default_headers)

        return r.json()

    except:
        print('Error fetching current quote data')
