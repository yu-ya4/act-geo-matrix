# experinece-geo-matrix
For my research, Experience-Geo-Matrix

## DB connection

```
$ ssh -f -N -C -L 10000:localhost:3306 ieyasu -p 22
$ ssh -f -N -C -L 20000:localhost:3306 ieyasu-berry -p 22
```

## import
```
form egmat import tabelog_searcher as ts
```

## search tabelog for reviews and save in database
```
searcher = ts.TabelogSearcher()
review_htmls, review_urls = searcher.search_for_reviews('彼女と飲む', 'kyoto', 'A2601', 'A260201', 'BC', 'BC04', '4596', '')
print(review_htmls)
# ['hogehogehogehtml',
'fugauga',
'hehehehe',...
]
print(review_urls)
# ['https://tabelog.com/tokyo/A1303/A130301/13090861/dtlrvwlst/B192731458/?use_type=0&srt=&sby=&rvw_part=all&lc=0&smp=1', 'https://tabelog.com/tokyo/A1310/A131002/13172383/dtlrvwlst/B109259930/?use_type=0&srt=&sby=&rvw_part=all&lc=0&smp=1', 'https://tabelog.com/fukuoka/A4001/A400203/40020640/dtlrvwlst/B122357957/?use_type=0&srt=&sby=&rvw_part=all&lc=0&smp=1', 'https://tabelog.com/tokyo/A1302/A130202/13123366/dtlrvwlst/B81693110/?use_type=0&srt=&sby=&rvw_part=all&lc=0&smp=1',
...]
reviews = searcher.parse_reviews(review_htmls, review_urls)
print(reviews)
# [
    {
        'review_id': 'B192731458',
        'restaurant_id': '13090861',
        'title': '初めてなのに懐かしい？コスパも抜群！駅近が魅力なもつ焼き店',
        'body': '心置きなく酔っ払えるのが嬉しくて彼女と飲む時は必ず記憶が曖昧なはちですが先日に限っては、はちの方が飲んでたくせに翌朝ポケットにおつりが入っていてさすがに青くなりました（すまん！次回！）そもそも飲んで帰ろー！と誘っておいて2000円しか持ってないし（え）でも2000円で足りたよ素晴らしきコストパフォーマンス！場所はマークシティ1F森本を覗くも当然ながら満席だったので、すぐ近くのこちらに流れてきました金曜日の夜ということもあり混んでいたけれど陽気が良かったので外のテーブルで乾杯♪とあるイベント帰りで少し飲んでいたため烏龍杯@400円からのスタートです定番のもつ煮込み@450円はお豆腐多めで嬉しい色んな種類が食べたかったので串焼きは「もつ焼きセット」@480円なるお任せ5本セットをチョイスそして最後に唐揚@500円を頼んだ彼女これが30代と40代の大きな差だよなぁと思いながら今宵も更けていったのでした。楽しかった！ちなみにポケットに300円（おつり）しかなくてバスのなくなった駅で一気に酔いが覚めたというのはナイショ。',
        'rate': 3.17,
        'url': 'https://tabelog.com/tokyo/A1303/A130301/13090861/dtlrvwlst/B192731458/?use_type=0&srt=&sby=&rvw_part=all&lc=0&smp=1',
        'html': 'hoehoeghoehgeoghehoeoh'
    },...
]
searcher.save_reviews(reviews)
```
## search tabelog for restaurants and save in database
```
searcher = ts.TabelogSearcher()
restaurant_htmls, restaurant_urls = tls.search_for_restaurants('', 'kyoto', 'A2601', '', 'RC', 'RC21', 'RC2199', '')
restaurants = tls.parse_restaurants(restaurant_htmls, restaurant_urls)

```

## get reviews from tabelog by specific restaurant url
```
restaurant_url = 'https://tabelog.com/kyoto/A2601/A260201/26003620/'
review_htmls, review_urls = searcher.get_reviews_from_tabelog_by_restaurant_url(restaurant_url)
reviews = searcher.parse_reviews(review_htmls, review_urls)
```

## get restaurant urls from database
```
restaurant_urls = searcher.get_restaurant_urls_from_db(10, 10)
print(restaurant_urls)
# ['https://tabelog.com/kyoto/A2601/A260605/26013639/', 'https://tabelog.com/kyoto/A2601/A260605/26011528/', 'https://tabelog.com/kyoto/A2601/A260604/26017862/', 'https://tabelog.com/kyoto/A2601/A260604/26024090/', 'https://tabelog.com/kyoto/A2601/A260604/26009098/', 'https://tabelog.com/kyoto/A2601/A260604/26014077/', 'https://tabelog.com/kyoto/A2601/A260604/26025100/', 'https://tabelog.com/kyoto/A2601/A260604/26002162/', 'https://tabelog.com/kyoto/A2601/A260604/26017476/', 'https://tabelog.com/kyoto/A2601/A260604/26022980/']

# レビューがデータベース上にないレストランをデータベースから取得
restaurant_urls = searcher.get_restaurant_urls_without_reviews_from_db(10, 10)
print(restaurant_urls)
# ['https://tabelog.com/kyoto/A2601/A260604/26010303/', 'https://tabelog.com/kyoto/A2601/A260604/26015141/', 'https://tabelog.com/kyoto/A2601/A260604/26027524/', 'https://tabelog.com/kyoto/A2601/A260604/26011487/', 'https://tabelog.com/kyoto/A2601/A260604/26009460/', 'https://tabelog.com/kyoto/A2601/A260604/26009502/', 'https://tabelog.com/kyoto/A2601/A260604/26011496/', 'https://tabelog.com/kyoto/A2601/A260604/26011489/', 'https://tabelog.com/kyoto/A2601/A260604/26003331/', 'https://tabelog.com/kyoto/A2601/A260604/26011691/']

```



## Read data

```
trs = TabelogReviews()
trs.read_reviews_from_database()

geos = Geos()
geos.read_geos_from_database()
```


## Make matrix

```
from matrix_maker import MatrixMaker
mm = MatrixMaker()
mm.get_scores_by_frequencies_of_reviews_with_experiences()

mat = mm.make_matrix()

ex_vec = mat.get_experience_vector('飲む', 'ちょっと')
mat.show_geo_ranking_by_vector(ex_vec, 10)

mat.show_geo_ranking_by_experience('飲む', 'ちょっと', 10)

# save as pickle
with open('../../data/matrix/natural_matrix.pickle', mode='wb') as f:
    pickle.dump(mat, f)


top 15 geos for the action "ちょっと
26000665 京極スタンド            （きょうごくすたんど）: 9.0
26000635 燻製と地ビール 和知            （くんせいとじびーるわち）: 8.0
26006432 伊右衛門サロン            （IYEMON SALON KYOTO）: 8.0
26002029 京都 五行            （きょうと ごぎょう）: 7.0
26007216 吟醸酒房　油長: 7.0
26001401 祇園サンボア            （ギオンサンボア）: 6.0
26004806 松川酒店: 5.0
26005004 だいやす            （かき屋 錦 だいやす）: 5.0
26002621 蕎麦の実 よしむら            （そばのみ よしむら）: 5.0
26001210 黄桜酒場            （【旧店名】カッパ天国 黄桜酒場）: 5.0
26005938 プラテロ            （PLATERO）: 5.0
26001147 bar K家 本館            （ケーヤ）: 5.0
26006028 フィゲラス スバコ・JR京都伊勢丹店: 4.0
26000091 百練            （ひゃくれん）: 4.0
26004778 酒肴屋 じじばば            （サケノアテヤ ジジババ）: 4.0


no index

top 15 geos for the action "たくさん
26000665 京極スタンド            （きょうごくすたんど）: 5.0
26007216 吟醸酒房　油長: 5.0
26001213 鳥せい 本店            （とりせい）: 4.0
26000635 燻製と地ビール 和知            （くんせいとじびーるわち）: 4.0
26005004 だいやす            （かき屋 錦 だいやす）: 3.0
26000829 楽庵            （らくあん）: 2.0
26023083 庶民: 2.0
26003098 居酒屋 あんじ 烏丸六角店: 2.0
26000818 味どころしん: 2.0
26002621 蕎麦の実 よしむら            （そばのみ よしむら）: 2.0
26002374 たつみ: 2.0
26012767 居酒屋ニューシンマチ: 2.0
26003757 清水家 錦 烏丸錦店: 2.0
26002029 京都 五行            （きょうと ごぎょう）: 2.0
26007406 ベジテジや 四条烏丸店: 2.0
```

## Operate MatrixMaker

```
# read from pickle
with open('../../data/matrix/natural_matrix.pickle', mode='rb') as f:
    mat = pickle.load(f)

# normalize
mat.normalize_at_row()

# reflect similarity for each experiences
mat.reflect_experience_similarity_in_matrix('../../data/similarities/0912/reviews_5_10/', 10)

```


## Experience, Experiences

```
from experience import Experience, Experiences
ex = Experience(1, '飲む', 'ちょっと')

exs = Experiences()
exs.read_experiences_from_database('ieyasu', 'chie-extracted2')
exs.get_index('飲む', 'ちょっと')

exs_2 = Experiences()
exs_2.read_experiences_from_database('ieyasu', 'chie-extracted')

exs.append(ex)
exs.extend(exs_2)


```
