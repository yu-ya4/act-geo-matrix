#!/usr/local/bin/python3
# -*- coding: utf-8

import requests
import lxml.html
from time import sleep
import sys
import api_keys
from tabelog_review import TabelogReview, TabelogReviews

class YahooLocoReviewSearcher:
    '''
    search Yahoo!ロコ for reviews
    shops in Kyoto

    ex:
        ylrs = YahooLocoReviewSearcher()
        reviews = ylrs.get_reviews('hogeohaoiareighjoih')
    '''

    def __init__(self, app_id = api_keys.YAHOO_APP_KEY):
        self.review_url = 'http://api.olp.yahooapis.jp/v1/review/'
        self.local_url = 'https://map.yahooapis.jp/search/local/V1/localSearch'
        self.app_id = app_id

    def get_stores(self, query):
        '''
        Get stores by Yahoo! local search API

        Args:
        Returns:
            list[list[str]]
        '''
        r = []

        local_url = self.local_url
        start = 1
        results = 10

        while 1:
            if start >= 100:
                break

            parameters = {
                'appid': self.app_id,
                'ac': '26100',
                'gc': '01',
                # 'query': query,
                'start': start,
                'results': results,
                'output': 'json'
            }
            res = requests.get(local_url, params=parameters)
            json = res.json()
            # 検索結果が空なら終了
            if json['ResultInfo']['Count'] == 0:
                break
            if 'Feature' in json:
                stores = json['Feature']
                for store in stores:
                    store_name = ''
                    url = ''
                    if 'Name' in store:
                        store_name = store['Name']
                    if 'Property' in store:
                        pro = store['Property']
                        if 'Detail' in pro:
                            if 'ReviewCount' in pro:
                                print(pro['ReviewCount'])
                            if 'ReviewUrl' in pro['Detail']:
                                url = pro['Detail']['ReviewUrl']
                        if 'Uid' in pro:
                            uid = pro['Uid']
                    r.append([uid, store_name, url])
            start += results

        return r

    def get_reviews(self, store_id, store_name, url):
        '''
        Args:
            store_id: str
                store id got by local search API(http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/localsearch.html)
        Returns:
            TabelogReviews
        '''
        r = TabelogReviews('')

        review_url = self.review_url + store_id
        start = 1
        results = 5

        while 1:
            # if start >=20:
            #     break

            parameters = {
                'appid': self.app_id,
                'results': results,
                'start': start,
                'output': 'json'
            }

            res = requests.get(review_url, params=parameters)
            json = res.json()
            if json['ResultInfo']['Count'] == 0:
                break
            if 'Feature' in json:
                reviews = json['Feature']
                for review in reviews:
                    if 'Property' in review:
                        comment = review['Property']['Comment']
                        title = comment['Subject'].replace('\n', '')
                        body = comment['Body'].replace('\n', '')
                        r.append(TabelogReview(url, store_name, title, body))
            start += results

        return r


if __name__ == '__main__':
    ylrs = YahooLocoReviewSearcher()
    stores = ylrs.get_stores('')
    result = TabelogReviews('')
    for store in stores:
        reviews = ylrs.get_reviews(store[0], store[1], store[2])
        result.extend(reviews)
    result.write_review('./reviews/yolp/kyoto/')
