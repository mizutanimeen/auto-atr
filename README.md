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
回答速度を選べる 1~5
正答率を選べる 80 ~ 100



最終的には自分でweb開いて確認してね


pythonの書き方わからん

pre3_4とか先生によって問題違うか確認とれてない、答えはpre3_4,CDごとにわけてるから先生ごと、年ごとに違う場合,答えが使い物にならない


csvのファイル名
クラスの後ろについてる(SG00)みたいなSG00をファイル名として使う
SG18p3je.csv

Pre3 -> SG17

Pre4 -> SG18

パート1 -> p1

英日と日英は同じ問題だったため同じファイルを使う
単語訳：英日 -> je
単語訳：日英 -> je 
（聴）単語訳 -> li
語句並べ替え -> ファイルなし

中級Cパート２単語訳：英日 -> SG09p2je.csv

ファイル名周りコードに直書きなのどうにかしたい

答えの共有するアイディアがいちいちプッシュするしかアイデアがないので答えを新しく作った人はプルリクもらえると助かります

https://bluebirdofoz.hatenablog.com/entry/2021/06/07/221747#:~:text=%E6%A6%82%E8%A6%81-,GitHub%E3%81%A7%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%BC%E6%A8%A9%E9%99%90%E3%81%AE%E3%81%AA%E3%81%84%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AB%E3%83%97%E3%83%AB%E3%83%AA%E3%82%AF,%E3%82%92%E8%A1%8C%E3%81%86%E5%BF%85%E8%A6%81%E3%81%8C%E3%81%82%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82

答えがない問題も時間がかかるのを許容できるならできる


pandas 1.5.3
https://pandas.pydata.org/docs/user_guide/index.html#user-guide