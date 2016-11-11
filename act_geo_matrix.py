#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
from time import sleep

class ActGeoMatrix:
    def __init__(self, actions_filename, review_dir):
        self.actions = []
        self.geos = []
        self.reviews = []
        self.matrix = []

        self.read_actions(actions_filename)
        self.read_reviews(review_dir)
        self.make_matrix()

    def read_actions(self, actions_filename):
        '''
        read actions list from txt file

        Args:
            actions_filename: str
        '''
        self.actions = []
        f_a = open(actions_filename, 'r')
        for line in f_a:
            action = line.replace('\n', '')
            self.actions.append(action)

    def read_reviews(self, review_dir):
        '''
        read reviews dict from txt file
            dict{action: list[TabelogReview]}

        Args:
            review_dir: str
        '''
        self.reviews = {}
        self.geos = []

        for action in self.actions:
            urls = []
            store_names = []
            titles = []
            bodies = []
            self.reviews[action] = []
            f_urls = open(review_dir + '/urls/' + action + '.txt', 'r')
            for line in f_urls:
                url = line.replace('\n', '')
                urls.append(url)

            f_store_names = open(review_dir + '/store_names/' + action + '.txt', 'r')
            for line in f_store_names:
                store_name = line.replace('\n', '')
                store_names.append(store_name)
                # make geos list
                if store_name in self.geos:
                    continue
                else:
                    self.geos.append(store_name)

            f_titles = open(review_dir + '/titles/' + action + '.txt', 'r')
            for line in f_titles:
                title = line.replace('\n', '')
                titles.append(title)

            f_bodies = open(review_dir + '/bodies/' + action + '.txt', 'r')
            for line in f_bodies:
                body = line.replace('\n', '')
                bodies.append(body)

            for i in range(len(urls)):
                self.reviews[action].append(TabelogReview(urls[i], store_names[i], titles[i], bodies[i]))

    def make_matrix(self):
        '''
        make matrix by reviews
        '''
        self.matrix = []
        for action in self.actions:
            row = len(self.geos)*[0]
            for review in self.reviews[action]:
                store_name = review.get_store_name()
                index = self.geos.index(store_name)
                row[index] += 1

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
        action_index = self.actions.index(action)
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

    def show_geo_ranking_sim(self, action, result_num, result_dir, use_num):
        sim_dic = self.read_similar_scores(result_dir, action, use_num)

        action_index = self.actions.index(action)
        row = self.matrix[action_index]
        for a, s in sim_dic.items():
            a_index = self.actions.index(a)
            a_row = self.matrix[a_index]
            a_row = list(map(lambda x: x*float(s), a_row))
            row = [x + y for (x, y) in zip(row, a_row)]

        ranking = sorted([(v,i) for (i,v) in enumerate(row)])
        for i in range(result_num+1):
            if i == 0:
                continue
            geo_index = ranking[-i][1]
            score = ranking[-i][0]

            if score == 0:
                break
            print(self.geos[geo_index] + ': ' + str(score))

    def read_similar_scores(self, result_dir, action, use_num):
        sim_dic = {}
        f_s = open('../similar_actions/result/tabelog/drink/' + result_dir + '/' + action + '.txt', 'r')
        i = 0
        for line in f_s:
            if i == use_num:
                break
            line = line.replace('\n', '')
            action, similarity = line.split(':')
            sim_dic[action] = similarity
            print(action + ':' + similarity)
            i += 1
        print('\n')
        return sim_dic

    def reflect_similarity_in_matrix(self, result_dir):
        '''
        remake geo act matrix reflecting similarity of actions
        Args:
            result_dir: str
        '''
        similarities = []
        for action in self.actions:
            similarity_dict = {}
            f_s = open('../similar_actions/result/tabelog/drink/' + result_dir + '/' + action + '.txt', 'r')
            for line in f_s:
                line = line.replace('\n', '')
                action, similarity = line.split(':')
                similarity_dict[action] = similarity
            similarities.append(similarity_dict)
        print(similarities[0])
