#!/usr/local/bin/python3
# -*- coding: utf-8

from act_geo_matrix import ActGeoMatrix

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

    def read_actions(self, actions_filename):
        '''
        read actions list from text file

        Args:
            actions_filename: str
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
        '''
        f_g = open(geos_filename, 'r')
        geos = [line.replace('\n', '') for line in f_g]
        f_g.close()
        return geos

    def make(self):
        '''
        Args:

        Return:
            ActGeoMatrix
        '''

        matrix = ActGeoMatrix()

        return matrix