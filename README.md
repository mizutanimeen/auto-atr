参考URL:https://qiita.com/ha_ru/items/86dfaae4c92e4a7be13f

https://kurozumi.github.io/selenium-python/waits.html

http://localhost:7900/ にアクセスし接続を押しパスワードに「secret」をいれ送信すれば見て確認できる。


プロジェクトの一番上で以下のコマンドを実行する

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


pythonの書き方わからん


