#!/usr/local/bin/python3
# -*- coding: utf-8

class TabelogReview:

    def __init__(self, id, store_name, title, body):
        self.id = id
        self.store_name = store_name
        self.title = title
        self.body = body


    def get_body(self):
        return self.body
