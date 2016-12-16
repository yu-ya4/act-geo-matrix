#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview
from tabelog_review_searcher import TabelogReviewSearcher
from act_geo_matrix import ActGeoMatrix
import MeCab

if __name__ == '__main__':
    # tr = TabelogReview(1, '鳥貴族 出町柳前店', '爆飲みするなら！', '出町柳周辺で学生さんが爆飲みするのにピッタシなお店です．')
    # print(tr.get_body())

    mat = ActGeoMatrix('./actions_飲む.txt', './tabelog_reviews_sep')
    mat.show_geo_ranking('大勢で飲む', 30)
    print('\n')
    mat.reflect_action_similarity_in_matrix('replace_5_5', 10)
    mat.show_geo_ranking('大勢で飲む', 50)
    exit()

    # for row in mat.matrix:
    #     count = 0
    #     for i in row:
    #         count += i
    #     print(count)
    #
    # print(mat.actions)
    exit()
    # action_list = []
    # f_a = open('./actions_飲む.txt', 'r')
    # for line in f_a:
    #     action = line.replace('\n', '')
    #     action_list.append(action)
    #
    # trs = TabelogReviewSearcher()
    #
    # for action in action_list:
    #     query = action[:-2] + ' ' + "飲む"
    #     reviews = trs.search(query)
    #     f_urls = open('./tabelog_reviews_sep/urls/' + action + '.txt', 'w')
    #     f_store_names = open('./tabelog_reviews_sep/store_names/' + action + '.txt', 'w')
    #     f_titles = open('./tabelog_reviews_sep/titles/' + action + '.txt', 'w')
    #     f_bodies = open('./tabelog_reviews_sep/bodies/' + action + '.txt', 'w')
    #
    #     for review in reviews:
    #         f_urls.write(review.get_url() + '\n')
    #         f_store_names.write(review.get_store_name() + '\n')
    #         f_titles.write(review.get_title() + '\n')
    #         f_bodies.write(review.get_body() + '\n')
    #     f_urls.close()
    #     f_store_names.close()
    #     f_titles.close()
    #     f_bodies.close()
