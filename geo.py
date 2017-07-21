#!usr/local/bin/python3
# -*coding: utf-8

class Geo:
    '''
    This class represents a geographic feature(a restaurant in tabelog).
    The instance has an id(restaurant_id, unique in tabelog), a name, a url, a title and body of comment(pr in tabelog)
    '''

    def __init__(self, id, name, url, title, body):
        self.__id = id
        self.__name = name
        self.__url = url
        self.__title = title
        self.__body = body

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body
