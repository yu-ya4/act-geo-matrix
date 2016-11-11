#!/usr/local/bin/python3
# -*- coding: utf-8

class ActGeoMatrix:
    def __init__(self):
        self.actions = []
        self.geos = []

    def read_actions(self, actions_filename):
        self.actions = []
        f_a = open(actions_filename, 'r')
        for line in f_a:
            action = line.replace('\n', '')
            self.actions.append(action)
