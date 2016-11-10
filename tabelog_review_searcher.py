#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
import requests

class TabelogReviewSearcher:

    def __init__(self):
        self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'
        # self.parameters = '/?rvw_part=all&sw=%E9%A3%B2%E3%82%80'
        self.parameters = '/?rvw_part=all&sw=ちょっと飲む'


    def search(self, query):
        '''
        Args:
            query: str
                query for searching tabelog review
        Returns:
            list[TabelogReview]
        '''

        parameters = {
            'rvw_part': 'all',
            'sw': query
        }
        page = 1
        url = self.url + str(page) + '/'
        res = requests.get(url, params=parameters)

        review_list = []
        review_list.append(TabelogReview(1, 'hoge', 'hogehoge', 'hogehogehoge'))
        review_list.append(TabelogReview(2, 'hoga', 'hogahoga', 'hogahogahoga'))

        return review_list
