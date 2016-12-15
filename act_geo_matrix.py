#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
from time import sleep

class ActGeoMatrix:
    '''
    Action and Gegraphic feature matrix
    a row means an action such as "drink a little"
    a column means an geographic feature such as "Torikizoku Demachiyanagiten"
    a element means some score of the action and geographic feature
    '''

    def __init__(self, actions_filename, review_dir):
        '''
        read actions and reviews from text files
        and make Action and Geographic matrix

        Args:
            actions_filename: str
                file path of the text file of actions list for matrix
            review_dir: str
                path of the directory countaining text files of reviews
        '''

        # actions of rows
        self.actions = []
        # geographic features of columns
        self.geos = []
        self.reviews = []
        self.matrix = []
        self.action_similarities = []

        self.read_actions(actions_filename)
        self.read_reviews(review_dir)
        self.make_flequency_matrix()

    def read_actions(self, actions_filename):
        '''
        read actions list from text file

        Args:
            actions_filename: str
        '''
        f_a = open(actions_filename, 'r')
        self.actions = [line.replace('\n', '') for line in f_a]
        f_a.close()

    def read_reviews(self, review_dir):
        '''
        read reviews dictionary from text file
            dict{str: list[TabelogReview]}
                ex. self.reviews['ちょっと飲む'][0].get_store_name = '鳥貴族 出町柳駅前店'

        Args:
            review_dir: str
        '''
        self.reviews = {}
        self.geos = []

        for action in self.actions:

            f_urls = open(review_dir + '/urls/' + action + '.txt', 'r')
            urls = [line.replace('\n', '') for line in f_urls]
            f_urls.close()

            store_names = []
            f_store_names = open(review_dir + '/store_names/' + action + '.txt', 'r')
            for line in f_store_names:
                store_name = line.replace('\n', '')
                store_names.append(store_name)
                # make geos list
                if store_name in self.geos:
                    continue
                else:
                    self.geos.append(store_name)
            f_store_names.close()

            f_titles = open(review_dir + '/titles/' + action + '.txt', 'r')
            titles = [line.replace('\n', '') for line in f_titles]
            f_titles.close()

            f_bodies = open(review_dir + '/bodies/' + action + '.txt', 'r')
            bodies = [line.replace('\n', '') for line in f_bodies]
            f_bodies.close()

            self.reviews[action] = [TabelogReview(urls[i], store_names[i], titles[i], bodies[i]) for i in range(len(urls))]

    def make_flequency_matrix(self):
        '''
        make matrix by reviews
        search for reviews by action query
        each element means the flequency of the reviews about the geo by the action query
        order by self.actions and self.geos

        self.matrix: list[list[int]]
        '''
        self.matrix = []
        n = len(self.geos)
        for action in self.actions:
            row = n * [0]
            for review in self.reviews[action]:
                store_name = review.get_store_name()
                geo_index = self.geos.index(store_name)
                row[geo_index] += 1

            self.matrix.append(row)

    def show_geo_ranking(self, action, result_num):
        '''
        show geo ranking with its score
        Args:
            action: str
                action
            result_num: int
                the number of geos shown
        '''
        try:
            action_index = self.actions.index(action)
        except:
            return print('no index')
        row = self.matrix[action_index]
        ranking = sorted([(v,i) for (i,v) in enumerate(row)])
        for i in range(result_num+1):
            if i == 0:
                continue
            geo_index = ranking[-i][1]
            score = ranking[-i][0]

            if score == 0:
                break
            print(self.geos[geo_index] + ': ' + str(score))

    def read_action_similarities(self, result_dir, num):
        '''
        read action similarities from txt file
        Args:
            result_dir: str
            num: int

        action_similarities: list[dict{str: float}]
        '''
        self.action_similarities = []
        for action in self.actions:
            action_similarity_dict = {}
            f_s = open('../similar_actions/result/tabelog/drink/' + result_dir + '/' + action + '.txt', 'r')
            for line in f_s:
                if len(action_similarity_dict) == num:
                    break
                line = line.replace('\n', '')
                action, similarity = line.split(':')
                action_similarity_dict[action] = similarity
            self.action_similarities.append(action_similarity_dict)


    def reflect_action_similarity_in_matrix(self, result_dir, num):
        '''
        remake geo-act-matrix reflecting similar actions

        Args:
            num: int
                the number of similar action used for remake the matrix
        '''
        self.read_action_similarities(result_dir, num)
        # pass by value
        original_matrix = self.matrix[:]
        action_index = 0
        # a row for an action
        for row in original_matrix:
            if action_index == len(self.actions):
                break
            # an action similarities dict for the action
            action_similarity_dict = self.action_similarities[action_index]
            # TOPn件のみの類似度・頻度を反映するという仕様に後で変更する
            # 今はとりあえず全部反映
            # an similar action and its similarity of the action
            for similar_action, similarity in action_similarity_dict.items():
                similar_action_index = self.actions.index(similar_action)
                similar_action_row = original_matrix[similar_action_index]
                # reflect the similar actions row in the action row
                # add each element of the similar action multiplied by the similarity to the element of the action
                self.matrix[action_index] = [x + float(similarity) * y for (x, y) in zip(self.matrix[action_index], similar_action_row)]
            action_index += 1
