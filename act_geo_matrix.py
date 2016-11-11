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
        urls = []
        store_names = []
        titles = []
        bodies = []
        for action in self.actions:
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
