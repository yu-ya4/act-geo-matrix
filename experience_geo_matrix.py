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
            scores: numpy.ndarray[numpy.float64]
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
            numpy.ndarray[numpy.float64]
        '''
        experience_index = self.experiences.get_index(verb, modifier)
        if experience_index is None:
            return print('no index \n')

        return self.scores[experience_index]

    def show_geo_ranking_by_vector(self, experience_vec, result_num):
        '''
        Args:
            experience_vec: numpy.ndarray[numpy.float64]

        Returns:
            None
        '''
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
        Args:
            verb: str
            modifier: str
            result_num: int

        Returns:
            None
        '''
        vec = self.get_experience_vector(verb, modifier)
        self.show_geo_ranking_by_vector(vec, result_num)

    def show_geo_ranking_by_multipule_experiences(self, verb1, modifier1, verb2, modifier2, result_num):
        '''
        Calculate vectors for multiple experiences and show geos

        v_e1e2 = α(v_e1 + v_e2)/2 + (1-α)(v_e1 AND v_e2)
        α: sim(e_1, e_2)

        Args:
            verb1, verb2: str
            modifier1, modifier2: str
            result_num: int
                the number of geos shown
        '''
        ex_vec1 = self.get_experience_vector(verb1, modifier1)
        ex_vec2 = self.get_experience_vector(verb2, modifier2)

        ex1_index = self.experiences.get_index(verb1, modifier1)
        sim_dict = self.experience_similarities[ex1_index]
        print(sim_dict)
        try:
            sim = float(sim_dict[modifier2])
        except:
            sim = 0.0

        print(sim)
        alfa = sim

        and_vec = np.logical_and(ex_vec1, ex_vec2)
        sum_vec = ex_vec1 + ex_vec2
        mul_vec = alfa * sum_vec/2 + (1-alfa) * sum_vec/2 * and_vec

        self.show_geo_ranking_by_vector(mul_vec, result_num)

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
