#!/usr/local/bin/python3
# -*- coding: utf-8

class TabelogReview:
    '''
    This class reprents a review of tabelog.
    The instance has a url, a store name, a title and a body of the review.

    '''

    def __init__(self, url, store_name, title, body):
        self.__url = url
        self.__store_name = store_name
        self.__title = title
        self.__body = body

    @property
    def url(self):
        return self.__url

    @property
    def store_name(self):
        return self.__store_name

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body
