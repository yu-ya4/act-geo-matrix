#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
import requests
import lxml.html
from time import sleep
import sys
import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

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
        self.db_connection = MySQLdb.connect(host=os.environ.get('HOST'), user=os.environ.get('DB_USER'), passwd=os.environ.get('PASSWD'), db=os.environ.get('DATABASE'), charset=os.environ.get('CHARSET'))
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

    def get_reviews_from_restaurant(self, restaurant_url):
        '''
        get review htmls from restaurant

        Args:
            restaurant: str
        Returns:
            list[list[str], list[str]]
                review htmls
        '''

        review_htmls = []
        review_urls = []

        page = 1

        while 1:
            rvw_url = restaurant_url + 'dtlrvwlst/'
            parameters = {
                'rvw_part': 'all',
                'lc': 2, #1ページあたり１００件取得
                'PG': page
            }

            res = requests.get(rvw_url, params=parameters)
            html = res.text
            root = lxml.html.fromstring(html) # レストラン口コミ一覧

            try:
                # review_items = root.cssselect('.rstdtl-rvwlst')
                review_items = root.cssselect('.rvw-item')
                if not review_items:
                    break

                for review_item in review_items:
                    review_url = 'http://tabelog.com' + review_item.attrib['data-detail-url']
                    rvw_res = requests.get(review_url)
                    sleep(1)
                    review_html = rvw_res.text

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
                try:
                    body = review_contents.cssselect('.rvw-item__rvw-comment p')[0].text_content().replace('\n', '')[10:-8]
                except:
                    body = ''
                try:
                    rate = float(root.cssselect('.c-rating__val')[0].text_content())
                except:
                    rate = 0.0
                divided_url = review_url.split('/')
                restaurant_id = divided_url[6]
                review_id = divided_url[8]
                review = {
                    'review_id': review_id,
                    'restaurant_id': restaurant_id,
                    'title': title,
                    'body': body,
                    'rate': rate,
                    'url': review_url,
                    'html': review_html
                }
                reviews.append(review)

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                print(review_url)
                break

        return reviews

    def save_reviews(self, reviews):
        '''
        save restaurants in mysql

        Args:
            restaurants: list[dict{}]
        '''

        for review in reviews:
            try:
                self.cursor.execute(
                    'INSERT INTO reviews(\
                        review_id,\
                        restaurant_id,\
                        title,\
                        body,\
                        rate,\
                        url,\
                        html\
                    )\
                    VALUES(\
                        %(review_id)s,\
                        %(restaurant_id)s,\
                        %(title)s,\
                        %(body)s,\
                        %(rate)s,\
                        %(url)s,\
                        %(html)s\
                    )', review)

            except MySQLdb.Error as e:
                print(review['url'])
                print('MySQLdb.Error: ', e)
                print(e.args)
                with open('mysqllog.txt', 'a') as f:
                    f.write(review['url'] + '\n')
                    f.write('MySQLdb.Error: ' +  e.args[1] +  '\n')
        self.db_connection.commit()
        # self.db_connection.close()

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
        # self.db_connection.close()

    def get_restaurant_urls_from_db(self, num, offset):
        sql = 'select id, url from restaurants order by id limit ' + str(offset) + ', ' + str(num)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        urls = []
        for row in result:
            # print(row)
            urls.append(row[1])

        return urls

    def get_areas(self):
        areas = []
        tabelog_url = 'https://tabelog.com'
        map_url = 'https://tabelog.com/map/'
        res = requests.get(map_url)
        # print(res.url)
        html = res.text
        root = lxml.html.fromstring(html)

        try:
            # i = 0
            pals = root.cssselect('.list-japan li')
            for pal in pals:
                # if i == 2:
                #     break

                pal_url = tabelog_url + pal.cssselect('a')[0].attrib['href']
                print(pal_url)
                pal_name = pal.cssselect('a')[0].text_content()
                if pal_name == '中国':
                    break
                pal_code = pal_url.split('/')[3]
                pal_dict = {pal_name: [pal_code]}
                pal_page = requests.get(pal_url)
                sleep(5)
                pal_html = pal_page.text
                pal_root = lxml.html.fromstring(pal_html)
                lst_prfs = pal_root.cssselect('.list-area li')

                lst_prf_dict_list = []
                for lst_prf in lst_prfs:
                     lst_prf_url = tabelog_url + lst_prf.cssselect('a')[0].attrib['href']
                     lst_prf_name = lst_prf.cssselect('a')[0].text_content()
                     lst_prf_code = lst_prf_url.split('/')[4]
                     lst_prf_dict = {lst_prf_name: [lst_prf_code]}

                     lst_prf_page = requests.get(lst_prf_url)
                     sleep(2)
                     lst_prf_html = lst_prf_page.text
                     lst_prf_root = lxml.html.fromstring(lst_prf_html)
                     lst_areas = lst_prf_root.cssselect('.list-area li')

                     lst_area_dict_list = []
                     for lst_area in lst_areas:
                         lst_area_url = tabelog_url + lst_area.cssselect('a')[0].attrib['href']
                         lst_area_name = lst_area.cssselect('a')[0].text_content()
                         lst_area_code = lst_area_url.split('/')[5]
                         lst_area_dict = {lst_area_name: [lst_area_code]}

                         lst_area_page = requests.get(lst_area_url)
                         sleep(1)
                         lst_area_html = lst_area_page.text
                         lst_area_root = lxml.html.fromstring(lst_area_html)
                         stations = lst_area_root.cssselect('.list-area li')

                         station_dict_list = []
                         for station in stations:
                             station_url = tabelog_url + station.cssselect('a')[0].attrib['href']
                             station_name = station.cssselect('a')[0].text_content()
                             station_code = station_url.split('/')[6]
                             station_dict = {station_name: station_code}
                             station_dict_list.append(station_dict)
                         lst_area_dict[lst_area_name].append(station_dict_list)
                         lst_area_dict_list.append(lst_area_dict)
                     lst_prf_dict[lst_prf_name].append(lst_area_dict_list)
                     lst_prf_dict_list.append(lst_prf_dict)
                pal_dict[pal_name].append(lst_prf_dict_list)

                areas.append(pal_dict)
                # i += 1


        except Exception as e:
            import traceback
            traceback.print_exc()
            print(pal_url)
            print(e)

        return areas

    def save_areas(self, areas):
        '''
        Args:
            areas: list[
                        dict{
                            pal_name: [
                                pal_code,
                                list[
                                    dict{
                                        lst_prf_name: list[
                                            lst_prf_code,
                                            list[
                                                dict{
                                                    lst_area_name: list[
                                                        lst_area_code,
                                                        list[
                                                            dict{
                                                                station_name: station_code
                                                            }
                                                        ]
                                                    ]
                                                }
                                            ]
                                        ]
                                    }
                                ]
                            ]
                        }
                    ]
        '''
        pal_id = 1
        lst_prf_id = 1
        lst_area_id = 1

        for pal_dict in areas:
            for pal_name, pal_li in pal_dict.items():
                pal = {
                    'name': pal_name,
                    'code': pal_li[0]
                }
                try:
                    self.cursor.execute(
                        'INSERT INTO pals(\
                            name,\
                            code\
                        )\
                        VALUES(\
                            %(name)s,\
                            %(code)s\
                        )', pal)

                    # lst_prf
                    lst_prf_dict_list = pal_li[1]
                    for lst_prf_dict in lst_prf_dict_list:
                        for lst_prf_name, lst_prf_li in lst_prf_dict.items():
                            lst_prf = {
                                'name': lst_prf_name,
                                'code': lst_prf_li[0],
                                'pal_id': pal_id
                            }

                            try:
                                self.cursor.execute(
                                    'INSERT INTO lst_prfs(\
                                        name,\
                                        code,\
                                        pal_id\
                                    )\
                                    VALUES(\
                                        %(name)s,\
                                        %(code)s,\
                                        %(pal_id)s\
                                    )', lst_prf)

                                # lst_area
                                lst_area_dict_list = lst_prf_li[1]
                                for lst_area_dict in lst_area_dict_list:
                                    for lst_area_name, lst_area_li in lst_area_dict.items():
                                        lst_area = {
                                            'name': lst_area_name,
                                            'code': lst_area_li[0],
                                            'lst_prf_id': lst_prf_id
                                        }

                                        try:
                                            self.cursor.execute(
                                                'INSERT INTO lst_ares(\
                                                    name,\
                                                    code,\
                                                    lst_prf_id\
                                                )\
                                                VALUES(\
                                                    %(name)s,\
                                                    %(code)s,\
                                                    %(lst_prf_id)s\
                                                )', lst_area)


                                            # station
                                            if lst_area_li == []:
                                                continue
                                            # print(lst_area_li)
                                            station_dict_list = lst_area_li[1]
                                            print(station_dict_list)
                                            for station_dict in station_dict_list:
                                                for station_name, station_code in station_dict.items():
                                                    station = {
                                                        'name': station_name,
                                                        'code': station_code,
                                                        'lst_are_id': lst_area_id
                                                    }

                                                    try:
                                                        self.cursor.execute(
                                                            'INSERT INTO stations(\
                                                                name,\
                                                                code,\
                                                                lst_are_id\
                                                            )\
                                                            VALUES(\
                                                                %(name)s,\
                                                                %(code)s,\
                                                                %(lst_are_id)s\
                                                            )', station)

                                                    except MySQLdb.Error as e:
                                                        print(station['name'])
                                                        print('MySQLdb.Error: ', e)
                                        except MySQLdb.Error as e:
                                            print(lst_area['name'])
                                            print('MySQLdb.Error: ', e)
                                        lst_area_id += 1

                            except MySQLdb.Error as e:
                                print(lst_prf['name'])
                                print('MySQLdb.Error: ', e)
                            lst_prf_id += 1

                except MySQLdb.Error as e:
                    print(pal['name'])
                    print('MySQLdb.Error: ', e)
                pal_id += 1

        self.db_connection.commit()
