参考URL:https://qiita.com/ha_ru/items/86dfaae4c92e4a7be13f

https://kurozumi.github.io/selenium-python/waits.html

http://localhost:7900/ にアクセスし接続を押しパスワードに「secret」をいれ送信すれば見て確認できる。


プロジェクトの一番上で以下のコマンドを実行する

docker-compose build --no-cache

docker-compose up -d --build

docker exec -it auto-atr python main.py


.sample_envを参考に.envを作成しdocker-composeと同じディレクトリに置いてください

中止する場合は CTRL + C
 
現在 pre3_4にのみ対応済み

dockerを使えばすぐに開発できるのでpre3_4以外にも一部使えるので改良してみてもいいかもしれませんね

issue作る
答えをcsvで管理しているのがあまりよくない。いちいちpushしないと共有できない。クライドDBとか使えばリアルタイムで共有できる。
並べ替え問題が１００点しか取れない
答えがない場合、答えファイルを作成しユーザーに一度時間をかけて間違えながら一周する許可をとってテストを作る。
IDとPASSWORDをenvにかいてるけど書いてない場合、プロンプト上で必要になったときに入力できるようにする、また、フラッグでも渡せるようにする。
クラスとかの選択もリアルタイムじゃなくてenvとフラッグで渡せるようにする
１度に１つのパートの80点未満のレッスンのみ実行させる。これを自由度高くしたい


最終的には自分でweb開いて確認してね


pythonの書き方わからん

pre3_4とか先生によって問題違うか確認とれてない、答えはpre3_4,CDごとにわけてるから先生ごと、年ごとに違う場合,答えが使い物にならない


csvのファイル名
pre3 -> c3
pre4 -> c4
中級c -> cc
中級d -> cd
パートn -> pn
パート1 -> p1

英日と日英は同じ問題だったため同じファイルを使う
単語訳：英日 -> je
単語訳：日英 -> je 
（聴）単語訳 -> li
語句並べ替え -> ファイルなし

pre3パート1単語訳：英日 -> c3p1je.csv
中級cパート2（聴）単語訳 -> ccp2li.csv
中級cパート3語句並べ替え -> なし