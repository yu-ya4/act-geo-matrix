#!/usr/local/bin/python3
# -*- coding: utf-8

import numpy as np
from scipy import linalg

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
        Get the experience vector, the row of the matrix by an experience(a verb and a modifier)

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

    def convert_experience_vector_to_result_list(self, experience_vec, result_num=10):
        '''
        Args:
            vec: numpy.ndarray[numpy.float64]
        Returns:
            list[int]
        '''
        result_list = []
        ranking = sorted([(v,i) for (i,v) in enumerate(experience_vec)])

        for i in range(result_num+1):
            if i == 0:
                continue
            geo_index = ranking[-i][1]
            geo = self.geos.geos[geo_index]
            score = ranking[-i][0]

            if score == 0:
                break
            result_list.append(geo.geo_id)

        return result_list

    def show_geo_ranking_by_vector(self, experience_vec, result_num):
        '''
        Show top n geos of an experience vector
        geo url, geo name, socre

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
            # print(geo.url + ' ' + geo.name + ': ' + str(score))
            print(geo.url)
        print('\n')

    def show_geo_ranking_by_experience(self, verb, modifier, result_num):
        '''
        Show top n geos of a row of the matrix by an experience(a verb, a modifier)

        Args:
            verb: str
            modifier: str
            result_num: int

        Returns:
            None
        '''
        vec = self.get_experience_vector(verb, modifier)
        self.show_geo_ranking_by_vector(vec, result_num)


    def calc_multiple_experiences_vector(self, ex_vec1, ex_vec2, sim):
        '''
        Calculate multiple experiences vector

        Args:
            ex_vec1, ex_vec2: numpy.ndarray[numpy.float64]
        Returns:
            numpy.ndarray[numpy.float64]
        '''

        and_vec = np.logical_and(ex_vec1, ex_vec2)
        sum_vec = ex_vec1 + ex_vec2
        mul_vec = sim * sum_vec/2 + (1-sim) * sum_vec/2 * and_vec

        return mul_vec


    def get_multiple_experiences_vector(self, verb1, modifier1, verb2, modifier2):
        '''
        Get the experience vector by calculating scores for multiple experiences

        v_e1e2 = α(v_e1 + v_e2)/2 + (1-α)(v_e1 AND v_e2)
        α: sim(e_1, e_2)

        Args:
            verb1, verb2: str
            modifier1, modifier2: str

        Returns:
            numpy.ndarray[numpy.float64]
        '''
        ex_vec1 = self.get_experience_vector(verb1, modifier1)
        ex_vec2 = self.get_experience_vector(verb2, modifier2)

        ex1_index = self.experiences.get_index(verb1, modifier1)
        try:
            sim_dict = self.experience_similarities[ex1_index]
        except:
            sim_dict = {}

        try:
            sim = float(sim_dict[modifier2])
        except:
            sim = 0.0

        mul_vec = self.calc_multiple_experiences_vector(ex_vec1, ex_vec2, sim)

        return mul_vec

    def get_multiple_experiences_vector_reflecting_similar_experiences(self, verb1, modifier1, verb2, modifier2, similar_count):
        '''
        Get the experience vector by calculating scores for multiple experiences

        v_e1e2 = α(v_e1 + v_e2)/2 + (1-α)(v_e1 AND v_e2)
        α: sim(e_1, e_2)

        Args:
            verb1, verb2: str
            modifier1, modifier2: str
            similar_count: int
        Returns:
            numpy.ndarray[numpy.float64]
        '''
        ex_vec1 = self.get_experience_vector_reflecting_similar_experiences(verb1, modifier1, similar_count)
        ex_vec2 = self.get_experience_vector_reflecting_similar_experiences(verb2, modifier2, similar_count)

        ex1_index = self.experiences.get_index(verb1, modifier1)
        try:
            sim_dict = self.experience_similarities[ex1_index]
        except:
            sim_dict = {}

        try:
            sim = float(sim_dict[modifier2])
        except:
            sim = 0.0

        mul_vec = self.calc_multiple_experiences_vector(ex_vec1, ex_vec2, sim)

        return mul_vec


    def show_geo_ranking_by_multiple_experiences(self, verb1, modifier1, verb2, modifier2, result_num):
        '''
        Show top n geos for multiple experiences

        Args:
            verb1, verb2: str
            modifier1, modifier2: str
            result_num: int
                the number of geos shown

        Returns:
            None
        '''

        mul_vec = self.get_multiple_experiences_vector(verb1, modifier1, verb2, modifier2)

        self.show_geo_ranking_by_vector(mul_vec, result_num)

    def show_geo_ranking_by_multiple_experiences_reflecting_similar_experiences(self, verb1, modifier1, verb2, modifier2, result_num, similar_count):
        '''
        Show top n geos for multiple experiences

        Args:
            verb1, verb2: str
            modifier1, modifier2: str
            result_num: int
                the number of geos shown
            similar_count: int

        Returns:
            None
        '''

        mul_vec = self.get_multiple_experiences_vector_reflecting_similar_experiences(verb1, modifier1, verb2, modifier2, similar_count)

        self.show_geo_ranking_by_vector(mul_vec, result_num)

    def get_experience_vector_reflecting_similar_experiences(self, verb, modifier, similar_count):
        '''
        Get the experience vector, the row of the experience reflecting similar experiences by an experience(a verb, a modifier)

        Args:
            verb: str
            modifier: str
            num: int

        Returns:
            numpy.ndarray[numpy.float64]
        '''
        ex_vec = self.get_experience_vector(verb, modifier).copy()
        ex_index = self.experiences.get_index(verb, modifier)
        sim_dict = self.experience_similarities[ex_index]

        ranking = sorted(sim_dict.items(), key = lambda x: x[1], reverse=True)

        for i in range(similar_count):
            try:
                sim_modifier = ranking[i][0]
                similarity = float(ranking[i][1])
                sim_ex_vec = self.get_experience_vector(verb, sim_modifier)
                ex_vec += similarity * sim_ex_vec
            except Exception as e:
                print(e)
                break

        # normalize
        if np.amax(ex_vec) * 1 != 0:
            ex_vec = ex_vec / np.amax(ex_vec) * 1

        return ex_vec

    def show_geo_ranking_by_experience_reflecting_similar_experiences(self, verb, modifier, similar_count, result_num):
        ex_vec = self.get_experience_vector_reflecting_similar_experiences(verb, modifier, similar_count)
        self.show_geo_ranking_by_vector(ex_vec, result_num)

    def read_experience_similarities(self, result_dir, num=200):
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

    def svd(self):
        """
        行列を特異値分解(SVD)する

        Returns:
            List<numpy.matrix>
            特異値分解された行列3つ
            特異値はリストで返される
        """
        #mat = np.matrix(mat)

        """
        full_matrices:
            1: UとVが正方行列に(次元が合わずに死ぬ??)
            0: UとVのかたちをいい感じに(とりあえずこれでなんとかしてる)
        """
        U, s, V = np.linalg.svd(self.scores, full_matrices=0)
        #print(s)

        return [U, s, V]

    def lsa(self, k):
        """
        行列にLSAを適用する

        Returns:
            numpy.matrix
            LSAを適用した結果
        """
        rank = np.linalg.matrix_rank(self.scores)
        # ランク以上の次元数を指定した場合は，ランク数分の特徴量を使用
        #npの仕様上，ランク以上分の特徴量を算出してるっぽい？
        # 負の値が入力された場合はk = 0 とする
        U, s, V = self.svd()
        if k > rank:
            k = rank
        if k < 0:
            k = 0

        #print("ランクk=%d 累積寄与率=%f" % (k, sum(s[:k]) / sum(s)))
        S = np.zeros((len(s),len(s)))
        S[:k, :k] = np.diag(s[:k]) #上からk個の特異値のみを使用

        lsa_mat = np.dot(U, np.dot(S, V))

        self.scores = lsa_mat
