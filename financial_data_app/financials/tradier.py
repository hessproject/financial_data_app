import sys
import json
import requests
import pprint as pp



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


def get_company_info(query):
    '''
    :param query: Search query for company information

    :return: symbol, exchange, type, and description information for the given query
    '''
    url = 'https://sandbox.tradier.com/v1/markets/search'
    if type(query) is not str:
        raise TypeError('Not a valid search query')

    payload = {
        'q': query
    }

    try:
        print('entering try')
        r = requests.get(url, params=payload, headers=default_headers)
        print(r.json())
        return r.json()
    except Exception as e:
        raise e