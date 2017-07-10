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
        review_htmls = tls.search('彼女', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '4596')
        reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])

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
        self.rvw_url = 'https://tabelog.com/0/0/rvw/COND-0-0-1-0/D-edited_at/'
        self.rst_url = 'https://tabelog.com/rstLst/'

    def search_for_reviews(self, query, pal, LstPrf, LstAre, Cat, LstCat, station_id):
        '''
        search tabelog for reviews by some condition
        get htmls got by each url of reviews

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
            list[str], list[str]
                list of htmls of reviews, list of urls
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
        # result = TabelogReviews('')
        review_htmls = []
        review_urls = []

        while 1:
            url = self.rvw_url + str(page) + '/'
            res = requests.get(url, params=parameters)
            print(res.url)
            # a page of the search results
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
                    review = requests.get(review_url)
                    # sleep(5)
                    review_html = review.text
                    review_htmls.append(review_html)
                    review_urls.append(review_url)
                page += 1
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(review_url)
                print(e)
                break

        return review_htmls, review_urls

    def parse_reviews(self, review_htmls, review_urls):
        '''
        parse htmls of tabelog reviews

        Args:
            review_html: list[str]
            review_urls: list[str]
        Returns:
            list[dict{}]
        '''

        reviews = []
        for (review_html, review_url) in zip(review_htmls, review_urls):
            review = {}
            root = lxml.html.fromstring(review_html)
            try:
                review_contents = root.cssselect('.rvw-item__review-contents')[0]
                try:
                    title = review_contents.cssselect('.rvw-item__title strong')[0].text_content()
                except:
                    title = ''
                body = review_contents.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')[10:-8]
                rate = float(root.cssselect('.c-rating__val')[0].text_content())
                divided_url = review_url.split('/')
                store_id = divided_url[6]
                review_id = divided_url[8]
                review = {'review_id': review_id, 'rate': rate, 'store_id': store_id, 'title': title, 'body': body, 'html': review_html, 'url': review_url}
                reviews.append(review)

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                print(review_url)
                break

        return reviews

    def search_for_restaurants(self, query, pal, LstPrf, LstAre, Cat, LstCat, station_id):
        '''
        search tabelog for restaurants by some condition
        get htmls got by each url of restaurants

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
            list[str], list[str]
                list of htmls of restaurants, list of urls
        '''

        parameters = {
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
        restaurant_htmls = []
        restaurant_urls = []

        while 1:
            url = self.rst_url + str(page) + '/'
            res = requests.get(url, params=parameters)
            print(res.url)
            # a page of the search results
            html = res.text
            root = lxml.html.fromstring(html)

            try:
                restaurants = root.cssselect('.list-rst')
                # when all restaurants are got, break loop
                if not restaurants:
                    break
                for restaurant in restaurants:
                    restaurant_url = restaurant.cssselect('.list-rst__rst-name-target')[0].attrib['href']
                    print(restaurant_url)
                    # get review detail
                    restaurant = requests.get(restaurant_url)
                    # sleep(5)
                    restaurant_html = restaurant.text
                    restaurant_htmls.append(restaurant_html)
                    restaurant_urls.append(restaurant_url)
                page += 1
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(restaurant_url)
                print(e)
                break

        return restaurant_htmls, restaurant_urls
