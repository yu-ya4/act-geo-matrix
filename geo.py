#!usr/local/bin/python3
# -*coding: utf-8

import MySQLdb
import traceback
from configparser import ConfigParser

class Geo:
    '''
    This class represents a geographic feature(a restaurant in tabelog).
    The instance has an id(restaurant_id, unique in tabelog), a name, a url, a title and body of comment(pr in tabelog)
    '''

    def __init__(self, geo_id, name, url, title, body):
        '''
        Args:
            geo_id: int
            name: str
            url: str
            title: str
            body: str
        '''
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

    def __init__(self):
        '''
        Args:
            geos: list[Geo]
        '''
        # self.__geos = geos
        self.__geos = []

    @property
    def geos(self):
        return self.__geos

    def read_geos_from_database(self):
        '''
        Read Geos from database(restaurants in tabelog)

        Returns:
            None
        '''

        self.__init__()
        env = ConfigParser()
        env.read('./.env')
        try:
            db_connection = MySQLdb.connect(host=env.get('mysql', 'HOST'), user=env.get('mysql', 'USER'), passwd=env.get('mysql', 'PASSWD'), db=env.get('mysql', 'DATABASE'), charset=env.get('mysql', 'CHARSET'))
            cursor = db_connection.cursor()
            sql = 'SELECT id, restaurant_id, name, url, pr_comment_title, pr_comment_body FROM restaurants;'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                geo = Geo(int(row[1]), row[2], row[3], row[4], row[5])
                self.__geos.append(geo)

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        cursor.close()
        db_connection.close()

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
