#!/usr/local/bin/python3
# -*- coding: utf-8

class TabelogReviewSearcher:

    def __init__(self):
        self.url = 'https://tabelog.com/kyoto/0/0/rvw/COND-0-0-2-0/D-dt/'
        # self.parameters = '/?rvw_part=all&sw=%E9%A3%B2%E3%82%80'
        self.parameters = '/?rvw_part=all&sw=ちょっと飲む'

    def get_request(self):
        return self.url + '1' + self.parameters
