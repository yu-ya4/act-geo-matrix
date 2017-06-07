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
        # change the request url along with the change of specifications of 食べログ
        # 2017/06/07 by yu-ya4
        # self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'
        self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-1-0/D-edited_at/'

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
                    # review_url = 'https://tabelog.com' + review.cssselect('.rvw-item__title-target')[0].attrib['href']
                    review_url = 'https://tabelog.com' + review.cssselect('.rvw-item__frame')[0].attrib['data-detail-url']
                    print(review_url)
                    # get review detail
                    detail_res = requests.get(review_url)
                    sleep(5)
                    detail_html = detail_res.text
                    detail_root = lxml.html.fromstring(detail_html)
                    # detail_review = detail_root.cssselect('.rvw-item__review-contents')[0]
                    # body = detail_review.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')

                    detail_reviews = detail_root.cssselect('.rvw-item__review-contents')
                    body = ''
                    for detail_review in detail_reviews:
                        try:
                            # remove default spaces of the starts of sentences
                            body += detail_review.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')[10:-8]
                        except:
                            continue

                    store_name = review.cssselect('.rvw-item__rst-name')[0].text_content()
                    try:
                        title = review.cssselect('.rvw-item__title-target')[0].text_content()
                    except:
                        title = ''
                    result.append(TabelogReview(review_url, store_name, title, body))
                page += 1
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(review_url)
                print(e)
                break

        return result
