#!/usr/local/bin/python3
# -*- coding: utf-8

import requests
import lxml.html
from time import sleep
import sys
import api_keys

class YahooLocoReviewSearcher:
    '''
    search Yahoo!ロコ for reviews
    shops in Kyoto

    ex:
        ylrs = YahooLocoReviewSearcher()
        reviews = ylrs.get_reviews('hogeohaoiareighjoih')
    '''

    def __init__(self, app_id = api_keys.YAHOO_APP_KEY):
        self.url = 'https://map.yahooapis.jp/olp/V1/review/'
        self.app_id = app_id

    def get_reviews(self, store_id):
        '''
        Args:
            store_id: str
                store id got by local search API(http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/localsearch.html)
        Returns:

        '''
        url = self.url + store_id
        parameters = {
            'appid': self.app_id,
            'result': 10,
            'start': 0,
            'output': 'json'
        }

        res = requests.get(url, params=parameters)


if __name__ == '__main__':
    ylrs = YahooLocoReviewSearcher()
    reviews = ylrs.get_reviews('92e25cd1c952bf27fbe783663530ce603f9ab90b')
