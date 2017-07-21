#!usr/local/bin/python3
# -*coding: utf-8

class Geo:
    '''
    This class represents a geographic feature(a restaurant in tabelog).
    The instance has an id(restaurant_id, unique in tabelog), a name, a url, a title and body of comment(pr in tabelog)
    '''

    def __init__(self, geo_id, name, url, title, body):
        self.__geo_id = geo_id
        self.__name = name
        self.__url = url
        self.__title = title
        self.__body = body

    @property
    def geo_id(self):
        return self.__geo_id

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

class Geos:
    '''
    a list of Geo
    '''

    def __init__(self, geos):
        '''
        Args:
            geos: list[Geo]
        '''
        self.__geos = geos

    @property
    def geos(self):
        return self.__geos

    def append(self, another_geo):
        '''
        append a Geo to the geos

        Args:
            another_geo: Geo
        Returns:
            None
        '''
        self.__geos.append(another_geo)

    def extend(self, another_geos):
        '''
        extend the Geos by another Geos

        Args:
            another_geos: Geos
        Returns:
            None
        '''
        self.__geos.extend(another_geos.geos)
