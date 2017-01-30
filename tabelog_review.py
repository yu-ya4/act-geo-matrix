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

class TabelogReviews:
    '''
    This class represents a list of Review.
    '''

    def __init__(self, reviews_path):
        self.__reviews = self.__read_reviews(reviews_path)

    @property
    def reviews(self):
        return self.__reviews

    def __read_reviews(self, reviews_path):
        '''
        '''
        f_urls = open(reviews_path + 'urls.txt', 'r')
        urls = [line.replace('\n', '') for line in f_urls]
        f_urls.close()

        f_store_names = open(reviews_path + 'store_names.txt', 'r')
        store_names = [line.replace('\n', '') for line in f_store_names]
        f_store_names.close()

        f_titles = open(reviews_path + 'titles.txt', 'r')
        titles = [line.replace('\n', '') for line in f_titles]
        f_titles.close()

        f_bodies = open(reviews_path + 'bodies.txt', 'r')
        bodies = [line.replace('\n', '') for line in f_bodies]
        f_bodies.close()

        try:
            reviews = [TabelogReview(urls[i], store_names[i], titles[i], bodies[i]) for i in range(len(urls))]
        except Exception as e:
            print(e)
            reviews = []

        return reviews

    def get_review_counts_for_each_geo(self, geos):
        '''
        count reviews for each geographic feature(store name)

        Args:
            geos: list[str]
                a list of geographic feature names
        Returns:
            list[float]
                a list of counts of review for each geographic feature
        '''
        counts = len(geos) * [0]
        for review in self.reviews:
            try:
                geo_index = geos.index(review.store_name)
                counts[geo_index] += 1.0
            except ValueError as ve:
                print(ve)

        return counts
