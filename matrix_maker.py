#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from geo import Geo, Geos
from experience import Experience, Experiences
from act_geo_matrix import ActGeoMatrix
import numpy as np
import MySQLdb
import os
import traceback
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class MatrixMaker:
    '''
    Making Action and Geographic feature matrix(ActGeoMatrix)
    MatrixMaker has several ways of making matrix.
    '''

    def __init__(self):
        '''
        get actions list and geographic features list to make a matrix
        '''

        # self.actions = self.read_actions(actions_filename)
        # self.geos = self.read_geos(geos_filename)
        self.experiences = Experiences()
        self.geos = Geos()
        self.reviews = {}
        self.get_experiences_from_db('test0')
        self.get_geos_from_db()
        # self.scores = np.zeros([len(self.actions), len(self.geos.geos)])
        self.scores = np.zeros([len(self.experiences.experiences), len(self.geos.geos)])

    def get_db_connection(self, db='ieyasu'):
        '''
        Get database connection

        Args:
            db: str
                local
                ieyasu
                ieyasu-berry
        '''
        try:
            if db == 'local':
                return MySQLdb.connect(host=os.environ.get('LOCAL_DB_HOST'), user=os.environ.get('LOCAL_DB_USER'), passwd=os.environ.get('LOCAL_DB_PASSWD'), db=os.environ.get('LOCAL_DB_DATABASE'), charset=os.environ.get('CHARSET'))
            elif db == 'ieyasu':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_DB_PORT')))
            elif db == 'ieyasu-berry':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_BERRY_DB_PORT')))
            elif db == 'ieyasu-local':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'))
            else:
                print('Error: please select correct database')
                exit()
        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)
            exit()

    # def read_actions(self, actions_filename):
    #     '''
    #     read actions list from text file
    #
    #     Args:
    #         actions_filename: str
    #     Returns:
    #         list[str]
    #     '''
    #     f_a = open(actions_filename, 'r')
    #     actions = [line.replace('\n', '') for line in f_a]
    #     f_a.close()
    #     return actions

    # def read_geos(self, geos_filename):
    #     '''
    #     read geos list from text file
    #
    #     Args:
    #         geos_filename: str
    #     Returns:
    #         list[str]
    #     '''
    #     f_g = open(geos_filename, 'r')
    #     geos = [line.replace('\n', '') for line in f_g]
    #     f_g.close()
    #     return geos

    def get_scores_by_review_counts_for_each_geo(self, reviews_dir):
        '''
        for each action, get review counts for each geographic feature(store name)

        Args:
            reviews_dir: str
        Returns:
            None
        '''
        counts_list = []
        for action in self.actions:
            # reviews got by each action query
            reviews = TabelogReviews(reviews_dir + action + '/')
            counts_list.append(reviews.get_review_counts_for_each_geo(self.geos))

        self.scores = np.array(counts_list)

    def get_scores_by_review_counts_for_each_geo_by_modifiers(self, reviews_dir):
        '''
        for each modify that means an action,
        get review counts for each geographic feature(store name)

        Args:
            reviews_dir: str
        Returns:
            None
        '''
        counts_list = []
        reviews = TabelogReviews(reviews_dir)
        for action in self.actions:
            counts_list.append(reviews.get_review_counts_for_each_geo_contain_word(self.geos, action))

        self.scores = np.array(counts_list)

    def get_geos_from_db(self):
        '''
        get geos(restaurants) from db

        Returns:
            None
        '''

        try:
            db_connection = self.get_db_connection()
            cursor = db_connection.cursor()
            sql = 'select res.restaurant_id, res.name, res.url, res.pr_comment_title, res.pr_comment_body, rev.title, rev.body from restaurants as res left join reviews as rev on res.restaurant_id = rev.restaurant_id where res.LstPrf = "A2601" order by res.id;'
            cursor.execute(sql)
            result = cursor.fetchall()

            geo_ids = []
            for row in result:
                geo_id = row[0]
                name = row[1]
                geo_url = '' if row[2] is None else row[2]
                pr_title = '' if row[3] is None else row[3]
                pr_body = '' if row[4] is None else row[4]
                geo = Geo(geo_id, name, geo_url, pr_title, pr_body)
                if geo_id not in geo_ids:
                    geo_ids.append(geo_id)
                    self.geos.append(geo)
                rvw_title = '' if row[5] is None else row[5]
                rvw_body = '' if row[6] is None else row[6]
                review = rvw_title + rvw_body

                if geo_id in self.reviews:
                    self.reviews[geo_id].append(review)
                else:
                    self.reviews[geo_id] = [review]

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        finally:
            cursor.close()
            db_connection.close()

    def get_experiences_from_db(self, label):
        self.experiences.read_experiences_from_database(label)

    def get_scores_by_frequencies(self):
        '''
        get matrix scores by frequencies of reviews that include experiences from geos
        '''
        #
        # for j, geo in enumerate(self.geos.geos):
        #     geo_id = geo.geo_id
        #     reviews = self.reviews[geo_id]
        #     for i, modifier in enumerate(self.actions):
        #         frequency = 0
        #         for review in reviews:
        #             # ここ要相談
        #             if modifier in review and '飲む' in review:
        #             # if modifier+'飲む' in review:
        #                 frequency += 1
        #         self.scores[i,j] = frequency

        for j, geo in enumerate(self.geos.geos):
            geo_id = geo.geo_id
            reviews = self.reviews[geo_id]
            for i, experience in enumerate(self.experiences.experiences):
                frequency = 0
                for review in reviews:
                    # ここ要相談
                    if experience.modifiers[0] in review and experience.verb in review:
                    # if modifier+'飲む' in review:
                        frequency += 1
                self.scores[i,j] = frequency


    def test(self):
        '''
        for test
        '''
        self.actions = [
                'ちょっと',
                '一人で',
                '女性と',
                'しっぽり'
        ]
        self.geos = Geos([
                Geo(1, 'くれしま', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(2, 'くれない', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(3, '鳥貴族', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(4, '鳥次郎', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(5, '大島', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(6, '順菜', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(7, '魔境', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．'),
                Geo(8, '眠い', 'http://test.com', '宴会に最適！', 'エンジェルがいるよ．')
        ])

        self.reviews = {
        1: ['なんて日だ！', 'ちょっと飲むにはいい店です．', 'ちょっと飲むの楽しい'],
        2: ['なんて日だ！'],
        3: [],
        4: ['ちょっとだけと思ったのに気づいたら飲む飲む', '一人で参戦！飲む', '楽しい'],
        5: ['女性としっぽりと飲むでました', '女性とちょっとだけ飲む'],
        6: [],
        7: ['しっぽり！'],
        8: ['ちょっと', '一人でゆっくりと飲む']
        }

        self.scores = np.zeros([len(self.actions), len(self.geos.geos)])


    def make_matrix(self):
        '''
        make ActGeoMatrix

        Returns:
            ActGeoMatrix
        '''

        # return ActGeoMatrix(self.actions, self.geos, self.scores)
        return ActGeoMatrix(self.experiences, self.geos, self.scores)
