#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
import requests
import lxml.html
from time import sleep
import sys
import MySQLdb
from configparser import ConfigParser

class TabelogSearcher:
    '''
    search tabelog for stores or reviews

    ex:
        tls = TabelogSearcher()
        review_htmls = tls.search('彼女', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '', '4596')
        reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])

        検索クエリ：'彼女'
        エリア1：'kyoto' -> 京都府
        エリア2：'A2601' -> 京都市
        エリア3：'A260201' -> 河原町・木屋町・先斗町
        ジャンル1：'BC' -> バー・お酒
        ジャンル2：'BC04' -> ワインバー
        ジャンル3: 'BC9991' -> 日本酒バー・焼酎バー
        最寄り駅：'4596' -> 四条駅（京都市営）

        カテゴリ参考: https://tabelog.com/cat_lst/

    '''

    def __init__(self):
        # change the request url along with the change of specifications of 食べログ
        # 2017/06/07 by yu-ya4
        # self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'
        self.rvw_url = 'https://tabelog.com/0/0/rvw/COND-0-0-1-0/D-edited_at/'
        self.rst_url = 'https://tabelog.com/rstLst/'
        env = ConfigParser()
        env.read('./.env')
        self.db_connection = MySQLdb.connect(host=env.get('mysql', 'HOST'), user=env.get('mysql', 'USER'), passwd=env.get('mysql', 'PASSWD'), db=env.get('mysql', 'DATABASE'), charset=env.get('mysql', 'CHARSET'))
        self.cursor = self.db_connection.cursor()

    def search_for_reviews(self, query, pal, LstPrf, LstAre, Cat, LstCat, LstCatD, station_id):
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
            LstCatD: str
                genre3
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
            'LstCatD': LstCatD,
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
            # print(res.url)
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
                    # print(review_url)
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
                restaurant_id = divided_url[6]
                review_id = divided_url[8]
                review = {
                    'review_id': review_id,
                    'rate': rate,
                    'restaurant_id': restaurant_id,
                    'title': title,
                    'body': body,
                    'html': 1,
                    'url': review_url
                }
                reviews.append(review)

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                print(review_url)
                break

        return reviews

    def search_for_restaurants(self, query, pal, LstPrf, LstAre, Cat, LstCat, LstCatD, station_id):
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
            LstCatD: str
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
            'LstCatD': LstCatD,
            'station_id': station_id,
            'lc': 2 #1ページあたり１００件取得
        }

        page = 1
        restaurant_htmls = []
        restaurant_urls = []

        while 1:
            url = self.rst_url + str(page) + '/'
            res = requests.get(url, params=parameters)
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
                    # print(restaurant_url)
                    # get review detail
                    restaurant = requests.get(restaurant_url)
                    sleep(1)
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


    def parse_restaurants(self, restaurant_htmls, restaurant_urls):
        '''
        parse htmls of tabelog restaurants

        Args:
            restaurant_htmls: list[str]
            restaurant_urls: list[str]
        Returns:
            list[dict{}]
        '''

        restaurants = []
        for (restaurant_html, restaurant_url) in zip(restaurant_htmls, restaurant_urls):
            restaurant = {}
            root = lxml.html.fromstring(restaurant_html)
            try:
                try:
                    pr_comment = root.cssselect('.pr-comment-wrap')[0]
                    pr_comment_title = pr_comment.cssselect('.pr-comment-title')[0].text_content().replace('\n', '')
                    pr_comment_body = pr_comment.cssselect('.pr-comment__body span')[0].text_content().replace('\n', '')[10:-8]
                except:
                    pr_comment_title = ''
                    pr_comment_body = ''
                try:
                    rate = float(root.cssselect('.tb-rating__val span')[0].text_content())
                except:
                    rate = 0.0

                try:
                    detail = {}
                    details = root.cssselect('#contents-rstdata')[0]
                    trs = details.cssselect('tr')
                    for tr in trs:
                        key = tr.cssselect('th')[0].text_content().replace('\n', '').strip()
                        val = tr.cssselect('td')[0].text_content().replace('\n', '').strip()
                        detail[key] = val
                    # print(detail)
                except:
                    continue

                name = detail['店名'] if '店名' in detail else ''
                genre = detail['ジャンル'] if 'ジャンル' in detail else ''
                address = detail['住所'].split()[0] if '住所' in detail else ''
                open_time = detail['営業時間'] if '営業時間' in detail else ''
                regular_holiday = detail['定休日'] if '定休日' in detail else ''
                budget= detail['予算'] if '予算' in detail else ''
                budget_from_reviews= detail['予算（口コミ集計）'] if '予算（口コミ集計）' in detail else ''
                seats= detail['席数'] if '席数' in detail else ''
                private_room = detail['個室'] if '個室' in detail else ''
                private_use = detail['貸切'] if '貸切' in detail else ''
                smoking = detail['禁煙・喫煙'] if '禁煙・喫煙' in detail else ''
                space_or_facilities = detail['空間・設備'] if '空間・設備' in detail else ''
                occasion = detail['利用シーン'] if '利用シーン' in detail else ''
                drink = detail['ドリンク'] if 'ドリンク' in detail else ''
                location = detail['ロケーション'] if 'ロケーション' in detail else ''
                service = detail['サービス'] if 'サービス' in detail else ''
                homepage = detail['ホームページ'] if 'ホームページ' in detail else ''
                remarks = detail['備考'] if '備考' in detail else ''

                divided_url = restaurant_url.split('/')
                pal = divided_url[3]
                LstPrf = divided_url[4]
                LstAre = divided_url[5]
                restaurant_id = divided_url[6]

                restaurant = {
                    'restaurant_id': restaurant_id,
                    'name': name,
                    'genre': genre,
                    'address': address,
                    'pal': pal,
                    'LstPrf': LstPrf,
                    'LstAre': LstAre,
                    'open_time': open_time,
                    'regular_holiday': regular_holiday,
                    'budget': budget,
                    'budget_from_reviews': budget_from_reviews,
                    'seats': seats,
                    'private_room': private_room,
                    'private_use': private_use,
                    'smoking': smoking,
                    'space_or_facilities': space_or_facilities,
                    'occasion': occasion,
                    'drink': drink,
                    'location': location,
                    'service': service,
                    'homepage': homepage,
                    'remarks': remarks,
                    'rate': rate,
                    'pr_comment_title': pr_comment_title,
                    'pr_comment_body': pr_comment_body,
                    'url': restaurant_url,
                    'html': restaurant_html,
                 }
                restaurants.append(restaurant)

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                print(restaurant_url)

        return restaurants

    def save_restaurants(self, restaurants):
        '''
        save restaurants in mysql

        Args:
            restaurants: list[dict{}]
        '''

        for restaurant in restaurants:
            try:
                self.cursor.execute(
                    'INSERT INTO restaurants(\
                        restaurant_id,\
                        name,\
                        genre,\
                        address,\
                        pal,\
                        LstPrf,\
                        LstAre,\
                        open_time,\
                        regular_holiday,\
                        budget,\
                        budget_from_reviews,\
                        seats,\
                        private_room,\
                        private_use,\
                        smoking,\
                        space_or_facilities,\
                        occasion,\
                        location,\
                        service,\
                        homepage,\
                        remarks,\
                        rate,\
                        pr_comment_title,\
                        pr_comment_body,\
                        url,\
                        html\
                    )\
                    VALUES(\
                        %(restaurant_id)s,\
                        %(name)s,\
                        %(genre)s,\
                        %(address)s,\
                        %(pal)s,\
                        %(LstPrf)s,\
                        %(LstAre)s,\
                        %(open_time)s,\
                        %(regular_holiday)s,\
                        %(budget)s,\
                        %(budget_from_reviews)s,\
                        %(seats)s,\
                        %(private_room)s,\
                        %(private_use)s,\
                        %(smoking)s,\
                        %(space_or_facilities)s,\
                        %(occasion)s,\
                        %(location)s,\
                        %(service)s,\
                        %(homepage)s,\
                        %(remarks)s,\
                        %(rate)s,\
                        %(pr_comment_title)s,\
                        %(pr_comment_body)s,\
                        %(url)s,\
                        %(html)s\
                    )', restaurant)

            except MySQLdb.Error as e:
                print(restaurant['url'])
                print('MySQLdb.Error: ', e)
        self.db_connection.commit()
        self.db_connection.close()
