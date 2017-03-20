#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from act_geo_matrix import ActGeoMatrix
import numpy as np

class MatrixMaker:
    '''
    Making Action and Geographic feature matrix(ActGeoMatrix)
    MatrixMaker has several ways of making matrix.
    '''

    def __init__(self, actions_filename, geos_filename):
        '''
        get actions list and geographic features list to make a matrix
        '''

        self.actions = self.read_actions(actions_filename)
        self.geos = self.read_geos(geos_filename)
        self.scores = np.zeros([len(self.actions), len(self.geos)])

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

    def make_matrix(self):
        '''
        make ActGeoMatrix

        Returns:
            ActGeoMatrix
        '''

        return ActGeoMatrix(self.actions, self.geos, self.scores)
