#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from geo import Geo, Geos
from act_geo_matrix import ActGeoMatrix
import numpy as np
import MySQLdb
from configparser import ConfigParser

class MatrixMaker:
    '''
    Making Action and Geographic feature matrix(ActGeoMatrix)
    MatrixMaker has several ways of making matrix.
    '''

    def __init__(self, actions_filename, geos_filename):
        '''
        get actions list and geographic features list to make a matrix
        '''

        self.env = ConfigParser()
        self.env.read('./.env')
        self.actions = self.read_actions(actions_filename)
        # self.geos = self.read_geos(geos_filename)
        self.geos = Geos([])
        self.reviews = {}
        self.get_geos_from_db()
        self.scores = np.zeros([len(self.actions), len(self.geos.geos)])

    def read_actions(self, actions_filename):
        '''
        read actions list from text file

        Args:
            actions_filename: str
        Returns:
            list[str]
        '''
        f_a = open(actions_filename, 'r')
        actions = [line.replace('\n', '') for line in f_a]
        f_a.close()
        return actions

    def read_geos(self, geos_filename):
        '''
        read geos list from text file

        Args:
            geos_filename: str
        Returns:
            list[str]
        '''
        f_g = open(geos_filename, 'r')
        geos = [line.replace('\n', '') for line in f_g]
        f_g.close()
        return geos

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

        db_connection = MySQLdb.connect(host=self.env.get('mysql', 'HOST'), user=self.env.get('mysql', 'USER'), passwd=self.env.get('mysql', 'PASSWD'), db=self.env.get('mysql', 'DATABASE'), charset=self.env.get('mysql', 'CHARSET'))
        cursor = db_connection.cursor()
        sql = 'select res.restaurant_id, res.name, res.url, res.pr_comment_title, res.pr_comment_body, rev.title, rev.body from restaurants as res left join reviews as rev on res.restaurant_id = rev.restaurant_id order by res.id;'
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            geo_id = row[0]
            name = row[1]
            geo_url = '' if row[2] is None else row[2]
            pr_title = '' if row[3] is None else row[3]
            pr_body = '' if row[4] is None else row[4]
            geo = Geo(geo_id, name, geo_url, pr_title, pr_body)
            self.geos.append(geo)
            rvw_title = '' if row[5] is None else row[5]
            rvw_body = '' if row[6] is None else row[6]
            review = rvw_title + rvw_body

            if geo_id in self.reviews:
                self.reviews[geo_id].append(review)
            else:
                self.reviews[geo_id] = [review]


    def get_scores_by_frequencies(self):
        '''
        get matrix scores by frequencies of reviews that include experiences fro geos
        '''

        for j, geo in enumerate(self.geos.geos):
            geo_id = geo.geo_id
            reviews = self.reviews[geo_id]
            for i, modifier in enumerate(self.actions):
                frequency = 0
                for review in reviews:
                    # ここ要相談
                    if modifier in review and '飲む' in review:
                    # if modifier+'飲む' in review:
                        frequency += 1
                self.scores[i,j] = frequency

    def make_matrix(self):
        '''
        make ActGeoMatrix

        Returns:
            ActGeoMatrix
        '''

        return ActGeoMatrix(self.actions, self.geos, self.scores)
