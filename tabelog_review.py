#!/usr/local/bin/python3
# -*- coding: utf-8

import os
import MySQLdb
import traceback
from configparser import ConfigParser

class TabelogReview:
    '''
    This class reprents a review of tabelog.
    The instance has a review_id(unique), a restaurant_id, an url, a title and a body of the review.

    '''

    def __init__(self, review_id, store_id, url, title, body):
        '''
        Args:
            review_id: str
            store_id: int
            url: str
            title: str
            body: str

        Ex:
            tr = TabelogReview('B233597230', 26011529, 'http://tabelog.com/kyoto/A2601/A260605/26011529/dtlrvwlst/B233597230/?use_type=0&rvw_part=all&lc=2&smp=1',
             'お刺身が美味しい！かす汁が熱々！軽く食べるには嬉しい居酒屋さんランチ', 'hogehoge')
        '''
        self.__review_id = review_id
        self.__store_id = store_id
        self.__url = url
        self.__title = title
        self.__body = body

    @property
    def review_id(self):
        return self.__review_id

    @property
    def store_id(self):
        return self.__store_id

    @property
    def url(self):
        return self.__url

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body

class TabelogReviews:
    '''
    This class represents a list of Review.

    There are two ways of reading tabelog reviews.
    One is reading from text files,
    and the other is reading from database.
    '''

    def __init__(self):
        # self.__reviews = self.__read_reviews(reviews_path)
        self.__reviews = []

    @property
    def reviews(self):
        return self.__reviews

    def read_reviews_from_database(self):
        '''
        Read TabelogReviews from database.

        Returns:
            None
        '''
        self.__init__()
        env = ConfigParser()
        env.read('./.env')
        try:
            db_connection = MySQLdb.connect(host=env.get('mysql', 'HOST'), user=env.get('mysql', 'USER'), passwd=env.get('mysql', 'PASSWD'), db=env.get('mysql', 'DATABASE'), charset=env.get('mysql', 'CHARSET'))
            cursor = db_connection.cursor()
            sql = 'SELECT id, review_id, restaurant_id, url, title, body FROM reviews;'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                tabelog_review = TabelogReview(row[1], int(row[2]), row[3], row[4], row[5])
                self.__reviews.append(tabelog_review)

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        cursor.close()
        db_connection.close()

    def __read_reviews_from_text(self, reviews_path):
        '''
        Read TabelogReviews from reviews directory.

        Args:
            reviews_dir: str
                a path to the review directory
        Returns:
            list[TabelogReview]
        '''
        try:

            f_urls = open(reviews_path + 'urls.txt', 'r')
            urls = [line.replace('\n', '') for line in f_urls]
            f_urls.close()

            f_store_names = open(reviews_path + 'store_names.txt', 'r')
            store_names = [line.replace('\n', '') for line in f_store_names]
            f_store_names.close()

            f_titles = open(reviews_path + 'titles.txt', 'r')
            titles = [line.replace('\n', '') for line in f_titles]
            f_titles.close()

            f_bodies = open(reviews_path + 'bodies.txt', 'r')
            bodies = [line.replace('\n', '') for line in f_bodies]
            f_bodies.close()

            reviews = [TabelogReview(urls[i], store_names[i], titles[i], bodies[i]) for i in range(len(urls))]
        except Exception as e:
            # print(e)
            # print(reviews_path)
            reviews = []

        return reviews

    def write_review(self, review_dir):
        '''
        Write TabelogReviews in text files in specified directory

        Args:
            review_dir: str
        Returns:
            None
        '''
        if not os.path.exists(review_dir):
            os.makedirs(review_dir)

        f_urls = open(review_dir + 'urls.txt', 'w')
        f_store_names = open(review_dir + 'store_names.txt', 'w')
        f_titles = open(review_dir + 'titles.txt', 'w')
        f_bodies = open(review_dir + 'bodies.txt', 'w')

        for review in self.reviews:
            f_urls.write(review.url + '\n')
            f_store_names.write(review.store_name + '\n')
            f_titles.write(review.title + '\n')
            f_bodies.write(review.body + '\n')
        f_urls.close()
        f_store_names.close()
        f_titles.close()
        f_bodies.close()


    def append(self, another_review):
        '''
        append a TabelogReview to the TabelogReviews

        Args:
            antheor_review: TabelogReview
        Returns:
            None
        '''
        self.__reviews.append(another_review)

    def extend(self, other_reviews):
        '''
        extend the TabelogReviews by another TabelogReviews

        Args:
            other_reviews: TabelogReviews
        Returns:
            None
        '''
        self.__reviews.extend(other_reviews.reviews)

    def get_review_counts_for_each_geo(self, geos):
        '''
        count reviews for each geographic feature(store name)

        Args:
            geos: list[str]
                a list of geographic feature names
        Returns:
            list[float]
                a list of counts of review for each geographic feature
        '''
        counts = len(geos) * [0]
        for review in self.reviews:
            try:
                geo_index = geos.index(review.store_name)
                counts[geo_index] += 1.0
            except ValueError as ve:
                print(ve)
                exit()

        return counts

    def get_review_counts_for_each_geo_contain_word(self, geos, word):
        '''
        count reviews that contain a specific word in title or body
        for each geographic feature(store name)

        Args:
            geos: list[str]
                a list of geographic feature names
            word: str
                a specific word to focus on
        Returns:
            list[float]
                a list of counts of review for each geographic feature
        '''
        counts = len(geos) * [0]
        for review in self.reviews:
            if word in (review.title + review.body):
                try:
                    geo_index = geos.index(review.store_name)
                    counts[geo_index] += 1.0
                except ValueError as ve:
                    print(ve)
                    exit()
        return counts

    def get_geo_names(self):
        '''
        get geographic features names from reviews store names
        duplicates are removed

        Returns:
            list[str]
        '''
        # geos = {review.store_name for review in self.reviews}
        geos = []
        for review in self.reviews:
            if review.store_name not in geos:
                geos.append(review.store_name)
        return geos
