# act-geo-matrix
For my research, Action-geographic-Matrix

## DB connection

```
$ ssh -f -N -C -L 10000:localhost:3306 ieyasu -p 22
$ ssh -f -N -C -L 20000:localhost:3306 ieyasu-berry -p 22
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
mm = MatrixMaker('./actions/test_actions_0608.txt')
mm.get_scores_by_frequencies()
mat = mm.make_matrix()
mat.show_geo_ranking('ちょっと', 15)
mat.show_geo_ranking('hoge', 15)
mat.show_geo_ranking('たくさん', 15)

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
