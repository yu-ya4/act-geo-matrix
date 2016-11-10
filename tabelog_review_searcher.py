#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
import requests
import lxml.html
from time import sleep


class TabelogReviewSearcher:

    def __init__(self):
        self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'

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
        review_list = []

        while 1:
            url = self.url + str(page) + '/'
            res = requests.get(url, params=parameters)
            html = res.text
            root = lxml.html.fromstring(html)

            try:
                reviews = root.cssselect('.review-wrap')
                # when all reviews are got, break loop
                if not reviews:
                    break
                # parse necessary information of review
                for review in reviews:
                    review_url = 'https://tabelog.com' + review.cssselect('.title a')[0].attrib['href']
                    title = review.cssselect('.title a')[0].text_content()
                    store_name = review.cssselect('.mname-wrap a')[0].text_content()
                    body = review.cssselect('.comment p')[0].text_content().replace('\n', '')
                    # print(review_url)
                    # print(title)
                    # print(store_name)
                    # print(body)
                    # remove default spaces of the starts of sentences
                    review_list.append(TabelogReview(review_url, store_name, title, body[13:]))
                page += 1
            except:
                break

        return review_list
