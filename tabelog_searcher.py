#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
import requests
import lxml.html
from time import sleep
import sys

class TabelogSearcher:
    '''
    search tabelog for stores or reviews

    ex:
        tls = TabelogSearcher()
        reviews = tls.search('彼女', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '4596')

        検索クエリ：'彼女'
        エリア1：'kyoto' -> 京都府
        エリア2：'A2601' -> 京都市
        エリア3：'A260201' -> 河原町・木屋町・先斗町
        ジャンル1：'BC' -> バー・お酒
        ジャンル2：'BC04' -> ワインバー
        ジャンル3(最寄り駅)：'4596' -> 四条駅（京都市営）

        カテゴリ参考: https://tabelog.com/cat_lst/

    '''

    def __init__(self):
        # change the request url along with the change of specifications of 食べログ
        # 2017/06/07 by yu-ya4
        # self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'
        self.r_url = 'https://tabelog.com/0/0/rvw/COND-0-0-1-0/D-edited_at/'

    def search_for_reviews(self, query, pal, LstPrf, LstAre, Cat, LstCat, station_id):
        '''
        search tabelog for reviews by some condition

        Args:
            query: str
                query for searching tabelog review
            pal: str
                area1
            LstPrf: str
                area2
            LstAre: str
                area3
            Cat: str:
                genre1
            LstCat: str
                genre2
            station_id: str
                station

        Returns:
            list[str]: list of htmls of reviews
        '''

        parameters = {
            'rvw_part': 'all',
            'sw': query,
            'pal': pal,
            'LstPrf': LstPrf,
            'LstAre': LstAre,
            'Cat': Cat,
            'LstCat': LstCat,
            'station_id': station_id,
            'lc': 2 #1ページあたり１００件取得
        }

        page = 1
        # an instance of TabelogReviews
        result = TabelogReviews('')

        while 1:
            url = self.r_url + str(page) + '/'
            res = requests.get(url, params=parameters)
            print(res.url)
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
                    # sleep(5)
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

    def parse_reviews(self, review_htmls):
        '''
        parse htmls of tabelog reviews

        Args:
            review_html: list[str]
        Returns:
            list[dict{}]
        '''

        reviews = []

        for review_html in review_htmls:
            review = {}
            root = lxml.html.fromstring(review_html)
            try:
                item = root.cssselect('.rvw-item')
                body = item.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')[10:-8]
                store_name = item.cssselect('.rvw-item__rst-name')[0].text_content()
                try:
                    title = item.cssselect('.rvw-item__title-target')[0].text_content()
                except:
                    title = ''
                review = {'title': title, 'store_name': store_name, 'body': body}
                reviews.append(review)

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                break
                
        return reviews
