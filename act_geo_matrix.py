#!/usr/local/bin/python3
# -*- coding: utf-8

import numpy as np

class ActGeoMatrix:
    '''
    Action and Gegraphic feature matrix
    a row means an action such as "drink a little"
    a column means an geographic feature such as "Torikizoku Demachiyanagiten"
    a element means some score of the action and geographic feature
    '''

    def __init__(self, experiences, geos, scores):
        '''
        get actions, geographic features list and scores from MatrixMaker

        Args:
            experiences: Experiences()
            geos: Geos()
            scores: numpy.ndarray[float]
        '''

        # experiences of rows
        self.__experiences = experiences
        # geographic features of columns
        self.__geos = geos
        self.scores = scores
        self.action_similarities = []

    @property
    def experiences(self):
        return self.__experiences

    @property
    def geos(self):
        return self.__geos

    def show_geo_ranking(self, verb, modifiers, result_num):
        '''
        show geo ranking with its score
        Args:
            verb: str
            modifiers: list[str]
            result_num: int
                the number of geos shown
        '''

        experience_index = self.experiences.get_index(verb, modifiers)
        if experience_index is None:
            return print('no index \n')

        row = self.scores[experience_index]
        ranking = sorted([(v,i) for (i,v) in enumerate(row)])

        print('top ' + str(result_num) + ' geos for the experience "' + verb + ': [' + ','.join(modifiers) + ']' )
        for i in range(result_num+1):
            if i == 0:
                continue
            geo_index = ranking[-i][1]
            geo = self.geos.geos[geo_index]
            score = ranking[-i][0]

            if score == 0:
                break
            print(str(geo.geo_id) + ' ' + geo.name + ': ' + str(score))
        print('\n')

    def show_geo_ranking_by_multipule_actions(self, actions, result_num):
        '''
        show geo ranking with its score
        Args:
            actions: list<str>
                actions
            result_num: int
                the number of geos shown
        '''

        rows = []
        for action in actions:
            try:
                rows.append(self.scores[self.actions.index(action)])
            except:
                return print('no index')

        sum_row = []
        for i in range(len(rows[0])):
            sum = 0.0
            mul = 1.0
            for row in rows:
                sum += row[i]
                mul = mul * row[i]

            if mul == 0.0:
                sum = 0.0
            sum_row.append(sum)


        ranking = sorted([(v,i) for (i,v) in enumerate(sum_row)])
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
                read top n similar actions

        Returns:
            None

        action_similarities: list[dict{str: float}]
        '''
        self.action_similarities = []
        for action in self.actions:
            action_similarity_dict = {}
            f_s = open(result_dir + action + '.txt', 'r')
            i = 0
            for line in f_s:
                if i == num:
                    break
                line = line.replace('\n', '')
                similar_action, similarity = line.split(':')
                action_similarity_dict[similar_action] = similarity
                i += 1
            self.action_similarities.append(action_similarity_dict)


    def reflect_action_similarity_in_matrix(self, result_dir, num):
        '''
        remake geo-act-matrix reflecting similar actions

        Args:
            num: int
                the number of similar action used for remake the matrix
        Returns:
            None
        '''
        self.read_action_similarities(result_dir, num)
        # pass by value
        original_matrix = self.scores[:]
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
                self.scores[action_index] = [x + float(similarity) * y for (x, y) in zip(self.scores[action_index], similar_action_row)]
            action_index += 1

    def normalize_at_row(self):
        i = 0
        for row in self.scores:
            if np.amax(row) * 1 != 0:
                self.scores[i] = row / np.amax(row) * 1
            i += 1
