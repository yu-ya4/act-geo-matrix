#!/usr/local/bin/python3
# -*- coding: utf-8

class TabelogReview:
    '''
    This class reprents a review of tabelog.
    The instance has a url, a store name, a title and a body of the review.
    '''

    def __init__(self, url, store_name, title, body):
        self.url = url
        self.store_name = store_name
        self.title = title
        self.body = body

    def get_url(self):
        return self.url

    def get_store_name(self):
        return self.store_name

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body
