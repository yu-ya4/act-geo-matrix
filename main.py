#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from geo import Geo, Geos
from experience import Experience, Experiences
from tabelog_searcher import TabelogSearcher
from matrix_maker import MatrixMaker
from experience_geo_matrix import ExperienceGeoMatrix
import MeCab
import sys
sys.path.append('../chiebukuro')
from chiebukuro_analyzer import ChiebukuroAnalyzer
import pickle
from experimenter import Experimenter, Experimenters, read_experiment_results, merge_correct_dict_dicts
import random
import numpy as np

if __name__ == '__main__':

    # exs1 = Experimenters()
    # exs2 = Experimenters()
    #
    # ex1 = Experimenter('女性と安く飲む')
    # ex2 = Experimenter('安く飲む')
    # ex3 = Experimenter('女性と飲む')
    #
    # exs1.append(ex1)
    #
    # exs2.append(ex2)
    # exs2.append(ex3)
    #
    # exs1.extend(exs2)

    # for ex in exs1.experimenters:
    #     print(ex.label)

    # correct_dict_dict1 = read_experiment_results('../../data/experiments/0924/0924ashida.csv')
    # correct_dict_dict2 = read_experiment_results('../../data/experiments/0924/0924okino.csv')
    #
    # merged_dict = merge_correct_dict_dicts(correct_dict_dict1, correct_dict_dict2)
    #
    # label_list = [
    # '美味しく', '一人で', '初めて', '少し', '友達と', '大量に', '久しぶりに', '楽しく', '昼間から', '友人と',
    # 'みんなで', '朝から', 'ちょっと', 'ゆっくり', 'いっぱい', ('女性と', 'ちょっと'), ('女性と', '安く'), ('みんなで', '安く'), ('昼間から', '彼女と'),
    # ('友達と', '朝まで'), ('友達と', 'オシャレに'), ('夜中に', '静かに'), ('一人で', '気軽に'), ('カウンターで', '美味しく'), ('仕事で', '個室で')
    # ]
    #
    # v = '飲む'
    #
    # single = [0.0, 0.0, 0.0, 0.0]
    # multple = [0.0, 0.0, 0.0, 0.0]
    # all_exp = [0.0, 0.0, 0.0, 0.0]
    #
    # for label in label_list:
    #     # print(merged_dict[label])
    #     if isinstance(label, str):
    #         m = label
    #         exp = Experimenter(label)
    #         exp.update_correct_dict(merged_dict[label])
    #
    #         with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #             mat = pickle.load(f)
    #
    #         # natural
    #         exp_vec_nat = mat.get_experience_vector(v, m)
    #         result_list_nat = mat.convert_experience_vector_to_result_list(exp_vec_nat, 10)
    #         ndcg_nat = exp.get_value_of_ndcg(result_list_nat, 10)
    #         # sim
    #         mat.read_experience_similarities('../../data/similarities/0918/reviews_10_15/')
    #         exp_vec_sim = mat.get_experience_vector_reflecting_similar_experiences(v, m, 5)
    #         result_list_sim = mat.convert_experience_vector_to_result_list(exp_vec_sim, 10)
    #         ndcg_sim = exp.get_value_of_ndcg(result_list_sim, 10)
    #
    #         # weight-sim
    #         mat.read_experience_similarities('../../data/similarities/0918/reviews_10_three_15/')
    #         exp_vec_w_sim = mat.get_experience_vector_reflecting_similar_experiences(v, m, 5)
    #         result_list_w_sim = mat.convert_experience_vector_to_result_list(exp_vec_w_sim, 10)
    #         ndcg_w_sim = exp.get_value_of_ndcg(result_list_w_sim, 10)
    #
    #         # lsa
    #         mat.lsa(200)
    #         exp_vec_lsa = mat.get_experience_vector(v, m)
    #         result_list_lsa = mat.convert_experience_vector_to_result_list(exp_vec_lsa, 10)
    #         ndcg_lsa = exp.get_value_of_ndcg(result_list_lsa, 10)
    #
    #         single[0] += ndcg_nat
    #         single[1] += ndcg_lsa
    #         single[2] += ndcg_sim
    #         single[3] += ndcg_w_sim
    #
    #         # print(label)
    #         # print('nat: ' + str(ndcg_nat))
    #         # print('lsa: ' + str(ndcg_lsa))
    #         # print('sim: ' + str(ndcg_sim))
    #         # print('w_sim: ' + str(ndcg_w_sim))
    #
    #     else:
    #         # multple
    #         m = label[0]
    #         mm = label[1]
    #         label = label[0] + label[1]
    #         exp = Experimenter(label)
    #         exp.update_correct_dict(merged_dict[label])
    #
    #         with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #             mat = pickle.load(f)
    #
    #         # natural
    #         exp_vec_nat = mat.get_multiple_experiences_vector(v, m, v, mm)
    #         result_list_nat = mat.convert_experience_vector_to_result_list(exp_vec_nat, 10)
    #         ndcg_nat = exp.get_value_of_ndcg(result_list_nat, 10)
    #
    #         # lsa
    #         mat.lsa(200)
    #         exp_vec_lsa = mat.get_multiple_experiences_vector(v, m, v, mm)
    #         result_list_lsa = mat.convert_experience_vector_to_result_list(exp_vec_lsa, 10)
    #         ndcg_lsa = exp.get_value_of_ndcg(result_list_lsa, 10)
    #
    #         # sim
    #         with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #             smat = pickle.load(f)
    #         smat.normalize_at_row()
    #         smat.read_experience_similarities('../../data/similarities/0918/reviews_10_15/')
    #         exp_vec_sim = smat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m ,v, mm, 5)
    #         result_list_sim = smat.convert_experience_vector_to_result_list(exp_vec_sim, 10)
    #         ndcg_sim = exp.get_value_of_ndcg(result_list_sim, 10)
    #
    #         # weight-sim
    #         with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #             wmat = pickle.load(f)
    #         wmat.normalize_at_row()
    #         wmat.read_experience_similarities('../../data/similarities/0918/reviews_10_three_15/')
    #
    #         exp_vec_w_sim = wmat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m ,v, mm, 5)
    #         result_list_w_sim = wmat.convert_experience_vector_to_result_list(exp_vec_w_sim, 10)
    #         ndcg_w_sim = exp.get_value_of_ndcg(result_list_w_sim, 10)
    #
    #         multple[0] += ndcg_nat
    #         multple[1] += ndcg_lsa
    #         multple[2] += ndcg_sim
    #         multple[3] += ndcg_w_sim
    #
    #         # print(label)
    #         # print('nat: ' + str(ndcg_nat))
    #         # print('lsa: ' + str(ndcg_lsa))
    #         # print('sim: ' + str(ndcg_sim))
    #         # print('w_sim: ' + str(ndcg_w_sim))
    #
    # single = np.array(single)
    # multple = np.array(multple)
    # all_exp = single + multple
    # print(single/15)
    # print(multple/10)
    # print(all_exp/25)
    # exit()
    #
    #     # exp_vec = mat.get_experience_vector(v, m)
    #     # result_list = mat.convert_experience_vector_to_result_list(exp_vec, 10)
    #     # print(result_list)
    #     # print(exp.get_value_of_dcg(result_list, 10))
    #     # for i in result_list:
    #     #     print(exp.correct_dict[i])
    #     #
    #     # print(exp.get_value_of_dcg(ideal, 10))
    #     # print(ideal[:10])
    #     # for i in ideal[:10]:
    #     #     print(exp.correct_dict[i])
    #     # print(exp.get_value_of_ndcg(result_list, 10))
    #     # # exit()
    #     # # print(exp.correct_dict)
    #
    # exit()
    #
    # exp = Experimenter('女性と安く飲む')
    # c_ids = [26026420, 26004778]
    # exp.update_correct_dict(c_ids)
    #
    # with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #     mat = pickle.load(f)
    #
    # # print(mat.experience_similarities)
    # v = '飲む'
    # m = '少し'
    # mm = '個室で'
    #
    # # mat.show_geo_ranking_by_experience(v, m, 10)
    # # mat.show_geo_ranking_by_experience(v, mm, 10)
    # # print('------------------------------')
    #
    # # natural
    # mat.show_geo_ranking_by_experience(v, m, 10)
    #
    # exp_vec1 = mat.get_experience_vector(v, m)
    # res1 = mat.convert_experience_vector_to_result_list(exp_vec1, 10)
    #
    # # sim
    # mat.read_experience_similarities('../../data/similarities/0918/reviews_10_15/')
    # mat.show_geo_ranking_by_experience_reflecting_similar_experiences(v, m, 5, 10)
    #
    # exp_vec2 = mat.get_experience_vector_reflecting_similar_experiences(v, m, 5)
    # res2 = mat.convert_experience_vector_to_result_list(exp_vec2, 10)
    #
    # # weight-sim
    # mat.read_experience_similarities('../../data/similarities/0918/reviews_10_three_15/')
    # mat.show_geo_ranking_by_experience_reflecting_similar_experiences(v, m, 5, 10)
    #
    # exp_vec3 = mat.get_experience_vector_reflecting_similar_experiences(v, m, 5)
    # res3 = mat.convert_experience_vector_to_result_list(exp_vec3, 10)
    #
    # # lsa
    # mat.lsa(200)
    # mat.show_geo_ranking_by_experience(v, m, 10)
    #
    # exp_vec4 = mat.get_experience_vector(v, m)
    # res4 = mat.convert_experience_vector_to_result_list(exp_vec4, 10)
    #
    # all_res = res1 + res2 + res3 + res4
    # set_res = list(set(all_res))
    #
    # print(len(all_res))
    # print(len(set_res))
    # random.shuffle(set_res)
    #
    # for res in set_res:
    #     print(res.url)
    # exit()
    #
    #
    # # natural
    # mat.show_geo_ranking_by_multiple_experiences(v, m, v, mm, 10)
    #
    # exp_vec1 = mat.get_experience_vector(v, m)
    # res1 = mat.convert_experience_vector_to_result_list(exp_vec1, 10)
    #
    # # lsa
    # mat.lsa(200)
    # mat.show_geo_ranking_by_multiple_experiences(v, m, v, mm, 10)
    #
    # exp_vec2 = mat.get_experience_vector(v, m)
    # res2 = mat.convert_experience_vector_to_result_list(exp_vec2, 10)
    #
    # # sim
    # with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #     smat = pickle.load(f)
    # smat.normalize_at_row()
    # smat.read_experience_similarities('../../data/similarities/0918/reviews_10_15/')
    # # smat.show_geo_ranking_by_multiple_experiences_reflecting_similar_experiences(v, m, v, mm, 10, 5)
    #
    # s_vec = smat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m ,v, mm, 5)
    # smat.show_geo_ranking_by_vector(s_vec, 10)
    #
    # exp_vec3 = smat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m, v, mm, 5)
    # res3 = smat.convert_experience_vector_to_result_list(exp_vec3, 10)
    #
    #
    # # weight-sim
    # with open('../../data/matrix/normalized_matrix.pickle', mode='rb') as f:
    #     wmat = pickle.load(f)
    # wmat.normalize_at_row()
    # wmat.read_experience_similarities('../../data/similarities/0918/reviews_10_three_15/')
    # # wmat.show_geo_ranking_by_multiple_experiences_reflecting_similar_experiences(v, m, v, mm, 10, 5)
    #
    # w_vec = wmat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m ,v, mm, 5)
    # wmat.show_geo_ranking_by_vector(w_vec, 10)
    #
    # exp_vec4 = smat.get_multiple_experiences_vector_reflecting_similar_experiences(v, m, v, mm, 5)
    # res4 = smat.convert_experience_vector_to_result_list(exp_vec4, 10)
    #
    # all_res = res1 + res2 + res3 + res4
    # set_res = list(set(all_res))
    #
    # print(len(all_res))
    # print(len(set_res))
    # random.shuffle(set_res)
    #
    # for res in set_res:
    #     print(res.url)


    #
    # mm = MatrixMaker()
    # mm.get_scores_by_frequencies()
    # mat = mm.make_matrix()
    # with open('../../data/matrix/natural_matrix.pickle', mode='wb') as f:
    #     pickle.dump(mat, f)
    # exit()

    # with open('../../data/matrix/natural_matrix.pickle', mode='rb') as f:
    #     mat = pickle.load(f)
    # mat.normalize_at_row()
    # mat.show_geo_ranking('飲む', ['ちょっと'], 15)
    # mat.show_geo_ranking('飲む', ['女性と'], 15)
    # mat.show_geo_ranking('飲む', ['美味しく'], 15)
    # # exit()
    # mat.reflect_experience_similarity_in_matrix('../../data/similarities/0912/reviews_5_10/', 10)
    # mat.show_geo_ranking('飲む', ['ちょっと'], 15)
    # mat.show_geo_ranking('飲む', ['女性と'], 15)
    # mat.show_geo_ranking('飲む', ['美味しく'], 15)
    # exit()

    # # mat.show_geo_ranking_by_multipule_actions(['ちょっと', '水'], 10)
    # mat.normalize_at_row()
    # for query in queries:
    #     print(query)
    #     mat.show_geo_ranking(query, 10)
    #     print('\n')
    # print('ちょっとみんな')
    # mat.show_geo_ranking_by_multipule_actions(['ちょっと', 'みんな'], 10)
    # print('\n')
    # print('-----------------------------------------')
    # # print(mat.scores)
    # # mat.read_action_similarities('./actions/similarities_100/', 5)
    # mat.reflect_action_similarity_in_matrix('./actions/similarity20170607/drink_5_5/', 5)
    # for query in queries:
    #     print(query)
    #     mat.show_geo_ranking('ちょっと', 10)
    #     print('\n')
    #
    # print('ちょっとみんな')
    # mat.show_geo_ranking_by_multipule_actions(['ちょっと', 'みんな'], 10)
    #
    #
    # exit()

    # areas = [
    #     {'兵庫': ['hyogo', [
    #                     {'川西市':['A1234', [
    #                                 {'大和': ['A123401', [
    #                                             {'畦野駅': 'R1234'},
    #                                             {'梅田駅': 'R1234'}
    #                                                     ]
    #                                         ]
    #                                 },
    #                                 {'多田': ['A123402', [
    #                                             {'多田駅': 'R1244'},
    #                                             {'日生駅': 'R1245'}
    #                                                     ]
    #                                         ]
    #                                 }
    #                                     ]
    #                                 ]
    #                     },
    #                     {'神戸市':['A1244', [
    #                                 {'灘': ['A124455', [
    #                                             {'神戸駅': 'R1222'},
    #                                             {'新神戸駅': 'R1221'}
    #                                                     ]
    #                                         ]
    #                                 }
    #
    #                                     ]
    #                                 ]
    #                     }
    #                     ]
    #             ]
    #     },
    #     {'大阪': ['ohsaka', [
    #                     {'大阪市':['A1444', [
    #                                 {'難波': ['A144444', [
    #                                             {'難波駅': 'R4444'}
    #                                                     ]
    #                                         ]
    #                                 },
    #                                 {'多': ['A123411', [
    #                                                     ]
    #                                         ]
    #                                 }
    #                                     ]
    #                                 ]
    #                     },
    #                     {'葛西市':['A3344', [
    #                                 {'hoge': ['A125445', [
    #                                             {'fuga駅': 'R12'},
    #                                             {'hage': 'R121'}
    #                                                     ]
    #                                         ]
    #                                 }
    #
    #                                     ]
    #                                 ]
    #                     }
    #                     ]
    #             ]
    #     }
    # ]
    # tls = TabelogSearcher('ieyasu')
    # review_htmls = tls.get_reviews_from_restaurant('https://tabelog.com/osaka/A2701/A270101/27052831/')
    # print(review_htmls[1])
    # print(len(review_htmls[1]))
    #
    # exit()
    #
    # tls = TabelogSearcher()
    # review_htmls = tls.search_for_reviews('彼女', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '', '4596')
    # reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
    # print(reviews)

    # tls = TabelogSearcher()
    # # review_htmls = tls.search_for_reviews('彼女', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '4596')
    # # reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
    # restaurant_htmls = tls.search_for_restaurants('', 'kyoto', 'A2601', '', 'RC', 'RC21', 'RC2199', '')
    # restaurants = tls.parse_restaurants(restaurant_htmls[0], restaurant_htmls[1])
    # print(len(restaurants))
    # tls.save_restaurants(restaurants)

    # import requests
    # tls = TabelogSearcher()
    # restaurant_url = 'https://tabelog.com/kyoto/A2601/A260201/26022882/'
    # res = requests.get(restaurant_url)
    # restaurant_html = res.text
    # restaurants = tls.parse_restaurants([restaurant_html], [restaurant_url])
    # print(len(restaurants))
    # tls.save_restaurants(restaurants)
    # print(restaurants)


    # tls = TabelogSearcher('ieyasu')
    # saved_area_list = tls.get_saved_area_in_db()
    # area_list = tls.get_area_list_from_db()
    # # print(saved_area_list)
    # # print(area_list)
    # # exit()
    # # restaurant_urls = tls.get_restaurant_urls_from_db(10,3669)
    # # cat_list = [('BC', 'BC01', ''), ('BC', 'BC02', ''), ('BC', 'BC03', ''), ('BC', 'BC04', ''), ('BC', 'BC05', ''), ('BC', 'BC06', ''), ('BC', 'BC07', ''), ('BC', 'BC99', ''),
    # #     ('RC', 'RC21', 'RC2101'), ('RC', 'RC21', 'RC2102'), ('RC', 'RC21', 'RC2199')]
    # cat_list = [('MC', 'MC01', ''), ('MC', 'MC11', ''), ('MC', 'MC21', ''),
    #             ('CC', 'CC01', ''), ('CC', 'CC02', ''), ('CC', 'CC03', ''), ('CC', 'CC04', ''), ('CC', 'CC05', ''), ('CC', 'CC06', ''), ('CC', 'CC99', ''),
    #             ('SC', 'SC01', 'SC0101'), ('SC', 'SC01', 'SC0102'), ('SC', 'SC01', 'SC0103'), ('SC', 'SC01', 'SC0199'),
    #             ('SC', 'SC02', 'SC0201'), ('SC', 'SC02', 'SC0202'), ('SC', 'SC02', 'SC0203'), ('SC', 'SC02', 'SC0299'),
    #             ('YC', 'YC01', ''), ('YC', 'YC02', ''), ('YC', 'YC99', ''),
    #             ('RC', 'RC01', 'RC0101'), ('RC', 'RC01', 'RC0102'), ('RC', 'RC01', 'RC0103'), ('RC', 'RC01', 'RC0104'), ('RC', 'RC01', 'RC0105'), ('RC', 'RC01', 'RC0106'), ('RC', 'RC01', 'RC0107'), ('RC', 'RC01', 'RC0108'), ('RC', 'RC01', 'RC0109'), ('RC', 'RC01', 'RC0110'), ('RC', 'RC01', 'RC0111'), ('RC', 'RC01', 'RC0112'), ('RC', 'RC01', 'RC0199'),
    #             ('RC', 'RC02', 'RC0201'), ('RC', 'RC02', 'RC0202'), ('RC', 'RC02', 'RC0203'), ('RC', 'RC02', 'RC0204'), ('RC', 'RC02', 'RC0209'), ('RC', 'RC02', 'RC0211'), ('RC', 'RC02', 'RC0212'), ('RC', 'RC02', 'RC0213'), ('RC', 'RC02', 'RC0219'),
    #             ('RC', 'RC03', 'RC0301'), ('RC', 'RC03', 'RC0302'), ('RC', 'RC03', 'RC0303'), ('RC', 'RC03', 'RC0304'),
    #             ('RC', 'RC04', 'RC0401'), ('RC', 'RC04', 'RC0402'), ('RC', 'RC04', 'RC0403'), ('RC', 'RC04', 'RC0404'), ('RC', 'RC04', 'RC0411'), ('RC', 'RC04', 'RC0412'), ('RC', 'RC04', 'RC0499'),
    #             ('RC', 'RC12', 'RC1201'), ('RC', 'RC12', 'RC1202'), ('RC', 'RC12', 'RC1203'), ('RC', 'RC12', 'RC1204'), ('RC', 'RC12', 'RC1205'), ('RC', 'RC12', 'RC1299'),
    #             ('RC', 'RC13', 'RC1301'), ('RC', 'RC13', 'RC1302'),
    #             ('RC', 'RC14', 'RC1401'), ('RC', 'RC14', 'RC1402'), ('RC', 'RC14', 'RC1403'), ('RC', 'RC14', 'RC1404'), ('RC', 'RC14', 'RC1405'), ('RC', 'RC14', 'RC1406'), ('RC', 'RC14', 'RC1407'), ('RC', 'RC14', 'RC1408'), ('RC', 'RC14', 'RC1409'),
    #             ('RC', 'RC22', 'RC2201'), ('RC', 'RC22', 'RC2202'), ('RC', 'RC22', 'RC2203'),
    #             ('RC', 'RC23', ''), ('RC', 'RC99', 'RC9901'), ('RC', 'RC99', 'RC9904'), ('RC', 'RC99', 'RC9903'), ('RC', 'RC99', 'RC9999')
    #             ]
    #
    # for area in area_list:
    #     if (area[0] == 'kyoto' and area[1] == 'A2601'):
    #         print(area)
    #         for cat in cat_list:
    #             print(cat)
    #             restaurant_htmls = tls.search_for_restaurants('', area[0], area[1], area[2], cat[0], cat[1], cat[2], '')
    #             restaurants = tls.parse_restaurants(restaurant_htmls[0], restaurant_htmls[1])
    #             tls.save_restaurants(restaurants)
    # exit()



    # tls = TabelogSearcher('ieyasu')
    # saved_area_list = tls.get_saved_area_in_db()
    # restaurant_urls = [
    #     'http://tabelog.com/kyoto/A2601/A260603/26011408/'
    #     ]
    # restaurant_urls = tls.get_restaurant_urls_without_reviews_from_db(1000, 0, 'A270501')
    #
    # print(len(restaurant_urls))
    # flg = True
    # for restaurant_url in restaurant_urls:
    #     # if restaurant_url == 'https://tabelog.com/hyogo/A2801/A280102/28000411/':
    #     #     flg = True
    #
    #     if flg:
    #         review_htmls = tls.get_reviews_from_restaurant(restaurant_url)
    #         reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
    #         print(len(reviews))
    #         tls.save_reviews(reviews)
    # tls.db_connection.close()
    # exit()





    tls = TabelogSearcher('ieyasu-berry')
    saved_area_list = tls.get_saved_area_in_db()
    # restaurant_urls = [
    #     'http://tabelog.com/kyoto/A2601/A260603/26011408/'
    #     ]
    flg = False
    skip_list = ['A260605', 'A260604', 'A260603', 'A260602']
    for saved_area in saved_area_list:
        if saved_area in skip_list:
            continue
        restaurant_urls = tls.get_restaurant_urls_without_reviews_from_db(100000, 0, saved_area)
        print(saved_area)
        print(len(restaurant_urls))
        # if saved_area == 'A260201':
        #     restaurant_urls += 'https://tabelog.com/kyoto/A2601/A260201/26005726/'

        for restaurant_url in restaurant_urls:
            if restaurant_url == 'https://tabelog.com/kyoto/A2601/A260201/26003620/':
                flg = True
            if flg == False:
                continue
            review_htmls = tls.get_reviews_from_restaurant(restaurant_url)
            reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
            print(len(reviews))
            tls.save_reviews(reviews)
    tls.db_connection.close()
    exit()
    # reviews.write_review('./reviews/20170607/飲む/')
    # exit()
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
    # trs = TabelogReviews('./reviews/20170607/飲む/')
    # all_text = ''
    # for tr in trs.reviews:
    #     all_text += (tr.title + '\n' + tr.body + '\n')
    # ca = ChiebukuroAnalyzer(all_text)
    # modifiers_frequences = ca.get_modifiers_frequences('飲む', '../chiebukuro/pattern')
    # fw1 = open('actions/20170607飲む.txt', 'w')
    # fw2 = open('actions/20170607飲むfreq.txt', 'w')
    #
    # for key, val in sorted(modifiers_frequences.items(), key=lambda x:x[1], reverse=True):
    #     fw1.write(key + '\n')
    #     fw2.write(key + ' ' + str(val) + '\n')
    #
    # fw1.close()
    # fw2.close()
    # exit()

    # geos = trs.get_geo_names()
    # fw = open('./geos/20170607飲む.txt', 'w')
    # for geo in geos:
    #     fw.write(geo + '\n')
    #
    # fw.close()
    # exit()
