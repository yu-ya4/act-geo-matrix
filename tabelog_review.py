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
