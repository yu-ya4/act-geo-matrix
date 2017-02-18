#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
import requests
import lxml.html
from time import sleep
import sys

class TabelogReviewSearcher:
    '''
    search tabelog for reviews
    shops in Kyoto

    ex:
        trs = TabelogReviewSearcher()
        reviews = trs.search('ちょっと飲む')
    '''

    def __init__(self):
        self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'

    def search(self, query):
        '''
        Args:
            query: str
                query for searching tabelog review
        Returns:
            TabelogReviews
        '''

        parameters = {
            'rvw_part': 'all',
            'sw': query,
            'lc': 2 #1ページあたり１００件取得
        }
        page = 1
        # an instance of TabelogReviews
        result = TabelogReviews('')

        while 1:
            url = self.url + str(page) + '/'
            res = requests.get(url, params=parameters)
            html = res.text
            root = lxml.html.fromstring(html)

            try:
                reviews = root.cssselect('.rvw-item')
                # when all reviews are got, break loop
                if not reviews:
                    break
                # parse necessary information of review
                for review in reviews:
                    review_url = 'https://tabelog.com' + review.cssselect('.rvw-item__title-target')[0].attrib['href']
                    # get review detail
                    sleep(3)
                    detail_res = requests.get(review_url)
                    sleep(7) 
                    detail_html = detail_res.text
                    detail_root = lxml.html.fromstring(detail_html)
                    detail_review = detail_root.cssselect('.rvw-item__review-contents')[0]
                    body = detail_review.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')
                    store_name = review.cssselect('.rvw-item__rst-name')[0].text_content()
                    title = review.cssselect('.rvw-item__title-target')[0].text_content()
                    # body = review.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')
                    # remove default spaces of the starts of sentences
                    # result.append(TabelogReview(review_url, store_name, title, body[13:]))
                    result.append(TabelogReview(review_url, store_name, title, body[8:]))
                page += 1
            except:
                break

        return result
