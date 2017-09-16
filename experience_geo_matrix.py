#!/usr/local/bin/python3
# -*- coding: utf-8

import numpy as np

class ExperienceGeoMatrix:
    '''
    Experience and Gegraphic feature matrix
    a row means a experience such as "drink a little"
    a column means an geographic feature such as "Torikizoku Demachiyanagiten"
    a element means some score of the experience and geographic feature
    '''

    def __init__(self, experiences, geos, scores):
        '''
        get experiences, geographic features list and scores from MatrixMaker

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
        self.experience_similarities = []

    @property
    def experiences(self):
        return self.__experiences

    @property
    def geos(self):
        return self.__geos

    def get_experience_vector(self, verb, modifier):
        '''
        Args:
            verb: str
            modifier: str

        Returns:
            list[float]
        '''
        experience_index = self.experiences.get_index(verb, modifier)
        if experience_index is None:
            return print('no index \n')

        return self.scores[experience_index]

    def show_geo_ranking_by_vector(self, experience_vec, result_num):
        ranking = sorted([(v,i) for (i,v) in enumerate(experience_vec)])

        for i in range(result_num+1):
            if i == 0:
                continue
            geo_index = ranking[-i][1]
            geo = self.geos.geos[geo_index]
            score = ranking[-i][0]

            if score == 0:
                break
            print(geo.url + ' ' + geo.name + ': ' + str(score))
        print('\n')

    def show_geo_ranking_by_experience(self, verb, modifier, result_num):
        '''
        show geo ranking with its score
        Args:
            verb: str
            modifier: str
            result_num: int
                the number of geos shown
        '''

        experience_vec = self.get_experience_vector(verb, modifier)
        print('top ' + str(result_num) + ' geos for the experience "' + verb + ': ' + modifier )
        self.show_geo_ranking_by_vector(experience_vec, result_num)

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

    def read_experience_similarities(self, result_dir, num):
        '''
        read experience similarities from txt file
        Args:
            result_dir: str
            num: int
                read top n similar experiences

        Returns:
            None

        experience_similarities: list[dict{str: float}]
        '''
        self.experience_similarities = []
        for experience in self.experiences.experiences:
            experience_similarity_dict = {}
            f_s = open(result_dir + experience.modifier + '.txt', 'r')
            i = 0
            for line in f_s:
                if i == num:
                    break
                line = line.replace('\n', '')
                similar_experience, similarity = line.split(':')
                experience_similarity_dict[similar_experience] = similarity
                i += 1
            self.experience_similarities.append(experience_similarity_dict)


    def reflect_experience_similarity_in_matrix(self, result_dir, num):
        '''
        remake experience-geo-matrix reflecting similar experiences

        Args:
            num: int
                the number of similar experience used for remake the matrix
        Returns:
            None
        '''
        self.read_experience_similarities(result_dir, num)
        # pass by value
        original_matrix = self.scores[:]
        experience_index = 0
        # a row for a experience
        for row in original_matrix:
            if experience_index == len(self.experiences.experiences):
                break
            # an experience similarities dict for the experience
            experience_similarity_dict = self.experience_similarities[experience_index]
            # TOPn件のみの類似度・頻度を反映するという仕様に後で変更する
            # 今はとりあえず全部反映
            # an similar experience and its similarity of the experience
            for similar_experience, similarity in experience_similarity_dict.items():
                similar_experience_index = self.experiences.get_index('飲む', similar_experience)
                similar_experience_row = original_matrix[similar_experience_index]
                # reflect the similar experience row in the experience row
                # add each element of the similar experience multiplied by the similarity to the element of the experience
                self.scores[experience_index] = [x + float(similarity) * y for (x, y) in zip(self.scores[experience_index], similar_experience_row)]
            experience_index += 1

    def normalize_at_row(self):
        i = 0
        for row in self.scores:
            if np.amax(row) * 1 != 0:
                self.scores[i] = row / np.amax(row) * 1
            i += 1
