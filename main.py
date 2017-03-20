#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from tabelog_review_searcher import TabelogReviewSearcher
from matrix_maker import MatrixMaker
from act_geo_matrix import ActGeoMatrix
import MeCab

if __name__ == '__main__':
    # tr = TabelogReview(1, '鳥貴族 出町柳前店', '爆飲みするなら！', '出町柳周辺で学生さんが爆飲みするのにピッタシなお店です．')
    # # print(tr.get_body())
    # trs1 = TabelogReviews('./reviews/tabelog_searched_by_sep_actions/ちょっと飲む/')
    # print(len(trs1.reviews))
    # trs2 = TabelogReviews('./reviews/tabelog_searched_by_sep_actions/おしゃれに飲む/')
    # print(len(trs2.reviews))
    # trs1.extend(trs2)
    # print(len(trs1.reviews))
    # trs1.append(tr)
    # print(len(trs1.reviews))
    # print(trs1.reviews[1881].title)
    #
    # action_list = []
    # f_a = open('./actions/action_飲む_extended.txt', 'r')
    # for line in f_a:
    #     action = line.replace('\n', '')
    #     action_list.append(action)
    # f_a.close()
    #
    # trs = TabelogReviews('')
    # for action in action_list:
    #     t = TabelogReviews('./reviews/search_test/' + action + '/')
    #     trs.extend(t)
    # geos = trs.get_geo_names()
    # fw = open('./geos/search_test_geos.txt', 'w')
    # for geo in geos:
    #     fw.write(geo + '\n')
    #
    # fw.close()
    # exit()

    mm = MatrixMaker(actions_filename='./actions/action_飲む_extended.txt', geos_filename='./geos/search_test_geos.txt')
    mm.get_scores_by_review_counts_for_each_geo('./reviews/search_test/')
    mat = mm.make_matrix()
    # print(mat.actions[1])
    # sum = 0
    # for s in mat.scores[1]:
    #     if s != 0.0:
    #         sum += s
    #         print(s)
    # print(sum)
    mat.show_geo_ranking('仕事終わりに飲む', 20)
    print('\n')
    mat.normalize_at_row()
    mat.show_geo_ranking('仕事終わりに飲む', 10)
    print('\n')
    # print(mat.scores)
    # mat.read_action_similarities('./actions/similarities_100/', 5)
    mat.reflect_action_similarity_in_matrix('./actions/similarities_100/', 3)
    mat.show_geo_ranking('仕事終わりに飲む', 10)

    exit()
    fre = trs.get_review_counts_for_each_geo(['くれしま',  'やよい軒', '吉野家'])
    print(fre)
    exit()
    mat = ActGeoMatrix('./actions/actions_飲む.txt', './tabelog_reviews_sep')
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
    # exit()
    # action_list = []
    # f_a = open('./actions/actions_飲む.txt', 'r')
    # i = 1
    # for line in f_a:
    #     action = line.replace('\n', '')
    #     action_list.append(action)
    # f_a.close()
    #
    # trs = TabelogReviewSearcher()
    # action = '軽く一杯飲む'
    # # query = action[:-2] + ' ' + "飲む"
    # query = "軽く 一杯 飲む"
    # reviews = trs.search(query)
    # reviews.write_review('./reviews/search_test/' + action + '/')

    # for action in action_list:
    #     query = action[:-2] + ' ' + "飲む"
    #     reviews = trs.search(query)
    #     reviews.write_review('./reviews/search_test/' + action + '/')


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
