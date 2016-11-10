#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
import requests
import lxml.html
from time import sleep


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
        print(res.url)
        html = res.text
        root = lxml.html.fromstring(html)

        review_list = []
        try:
            reviews = root.cssselect('.review-wrap')
            for review in reviews:
                review_url = 'https://tabelog.com' + review.cssselect('.title a')[0].attrib['href']
                title = review.cssselect('.title a')[0].text_content()
                store_name = review.cssselect('.mname-wrap a')[0].text_content()
                body = review.cssselect('.comment p')[0].text_content()
                # print(review_url)
                # print(title)
                # print(store_name)
                # print(body)
                review_list.append(TabelogReview(review_url, title, store_name, body))
        except:
            print("fin")


        return review_list
