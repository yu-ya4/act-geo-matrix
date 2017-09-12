#!/usr/local/bin/python3
# -*- coding: utf-8

from tabelog_review import TabelogReview, TabelogReviews
from geo import Geo, Geos
from experience import Experience, Experiences
from tabelog_searcher import TabelogSearcher
from matrix_maker import MatrixMaker
from act_geo_matrix import ActGeoMatrix
import MeCab
import sys
sys.path.append('../chiebukuro')
from chiebukuro_analyzer import ChiebukuroAnalyzer
import pickle

if __name__ == '__main__':

    # exs = Experiences()
    # exs.read_experiences_from_database('test0')
    # print(exs.experiences)
    # i = exs.get_index('飲む', ['ちょと'])
    # print(i)
    # exit()

    # trs = TabelogReviews()
    # trs.read_reviews_from_database()
    #
    # geos = Geos()
    # geos.read_geos_from_database()
    # exit()
    #
    # mm = MatrixMaker()
    # mm.get_scores_by_frequencies()
    # mat = mm.make_matrix()
    # with open('../../data/matrix/natural_matrix.pickle', mode='wb') as f:
    #     pickle.dump(mat, f)
    # exit()

    with open('../../data/matrix/natural_matrix.pickle', mode='rb') as f:
        mat = pickle.load(f)
    mat.normalize_at_row()
    mat.show_geo_ranking('飲む', ['ちょっと'], 15)
    mat.show_geo_ranking('飲む', ['女性と'], 15)
    mat.show_geo_ranking('飲む', ['美味しく'], 15)
    # exit()
    mat.reflect_experience_similarity_in_matrix('../../data/similarities/test/drink_10_5_three/', 10)
    mat.show_geo_ranking('飲む', ['ちょっと'], 15)
    mat.show_geo_ranking('飲む', ['女性と'], 15)
    mat.show_geo_ranking('飲む', ['美味しく'], 15)
    exit()

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
    # tls = TabelogSearcher()
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
    #
    # area_list = tls.get_area_list_from_db()
    # # restaurant_urls = tls.get_restaurant_urls_from_db(10,3669)
    # cat_list = [('BC', 'BC01', ''), ('BC', 'BC02', ''), ('BC', 'BC03', ''), ('BC', 'BC04', ''), ('BC', 'BC05', ''), ('BC', 'BC06', ''), ('BC', 'BC07', ''), ('BC', 'BC99', ''),
    #     ('RC', 'RC21', 'RC2101'), ('RC', 'RC21', 'RC2102'), ('RC', 'RC21', 'RC2199')]
    #
    # for area in area_list:
    #     if (area[0] == 'osaka' and area[2] not in saved_area_list) or area[2] == 'A270103':
    #         print(area)
    #         for cat in cat_list:
    #             print(cat)
    #             restaurant_htmls = tls.search_for_restaurants('', area[0], area[1], area[2], cat[0], cat[1], cat[2], '')
    #             restaurants = tls.parse_restaurants(restaurant_htmls[0], restaurant_htmls[1])
    #             tls.save_restaurants(restaurants)
    # exit()



    tls = TabelogSearcher('ieyasu')
    saved_area_list = tls.get_saved_area_in_db()
    # restaurant_urls = [
    #     'http://tabelog.com/kyoto/A2601/A260603/26011408/'
    #     ]
    restaurant_urls = tls.get_restaurant_urls_from_db(100000, 0, 'A280501')
    restaurant_urls += tls.get_restaurant_urls_from_db(100000, 0, 'A280502')
    restaurant_urls += tls.get_restaurant_urls_from_db(100000, 0, 'A280503')
    restaurant_urls += tls.get_restaurant_urls_from_db(100000, 0, 'A280504')
    restaurant_urls += tls.get_restaurant_urls_from_db(100000, 0, 'A280505')

    print(len(restaurant_urls))
    flg = True
    for restaurant_url in restaurant_urls:
        # if restaurant_url == 'https://tabelog.com/hyogo/A2801/A280102/28000411/':
        #     flg = True

        if flg:
            review_htmls = tls.get_reviews_from_restaurant(restaurant_url)
            reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
            print(len(reviews))
            tls.save_reviews(reviews)
    tls.db_connection.close()
    exit()





    # tls = TabelogSearcher('ieyasu')
    # saved_area_list = tls.get_saved_area_in_db()
    # # restaurant_urls = [
    # #     'http://tabelog.com/kyoto/A2601/A260603/26011408/'
    # #     ]
    # for saved_area in saved_area_list:
    #     restaurant_urls = tls.get_restaurant_urls_from_db(100000, 0, saved_area)
    #     print(saved_area)
    #
    #     for restaurant_url in restaurant_urls:
    #         review_htmls = tls.get_reviews_from_restaurant(restaurant_url)
    #         reviews = tls.parse_reviews(review_htmls[0], review_htmls[1])
    #         print(len(reviews))
    #         tls.save_reviews(reviews)
    # tls.db_connection.close()
    # exit()
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
