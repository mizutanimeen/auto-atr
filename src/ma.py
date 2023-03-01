from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import argparse

print(os.environ['ID'])
print(os.environ['PASS'])

parser = argparse.ArgumentParser(description='引数は必須')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('arg1', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
parser.add_argument('arg2', help='foooo')
parser.add_argument('--arg3')    # オプション引数（指定しなくても良い引数）を追加
parser.add_argument('-a', '--arg4')   # よく使う引数なら省略形があると使う時に便利

args = parser.parse_args()    # 4. 引数を解析

print('arg1='+args.arg1)
print('arg2='+args.arg2)
# print('arg3='+args.arg3)
# print('arg4='+args.arg4)

browser = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

#region 設定
USER = "220442122"
PASS = "220442122"
CSV_PATH = "./pre4_part3_s1.csv"
# CSV_PATH = "./pre4_part4_s1.csv"
PART = 3
# exeの場所指定
# 最大待ち時間
wait = WebDriverWait(driver=browser, timeout=100)
#endregion

#region ここは共通
#ページに移動
url_login = "https://atr.meijo-u.net/"
browser.get(url_login)
#ログイン動作
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.ID, "id"))
)
element.clear()
element.send_keys(USER)
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.ID, "pw"))
)
element.clear()
element.send_keys(PASS)
element = WebDriverWait(browser, 100).until(
    EC.element_to_be_clickable((By.ID, "submit-button"))
)
element.click()
#class
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.ID, "large-button-class"))
)
element.click()
#endregion
#region pre part
#Pre3-4  
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="class_container"]/div[1]/a'))
)
element.click()
#Pre4  
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="wpContents"]/div[2]/div[6]/div[1]'))
)
element.click()
# パート
element = WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="tab_root"]/li[{PART}]/a'))
)
element.click()
#endregion
print("ok")
print("ok")
print("ok")
print("ok")
print("ok")
print("ok")
#number番目の閉じてるバーを開く
def bar_open(number):
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="course-detail"]/div[{number}]'))
    )
    element.click()
def q_one_start(number):
    #レッスン number－1を開く
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="course-detail"]/div[{number}]/div[2]/div[2]/div[2]/div[1]'))
    )
    element.click()

    #レッスン n－１の開始ボタン
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME,'View-Button'))
    )
    element.click()
def q_two_start(number):
    #レッスン number－2を開く
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="course-detail"]/div[{number}]/div[2]/div[2]/div[2]/div[2]'))
    )
    element.click()

    #レッスン n－2の開始ボタン
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[3]'))
    )
    element.click()
def q_three_start(number):
    #レッスン number－3を開く
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="course-detail"]/div[{number}]/div[2]/div[3]/div[2]/div'))
    )
    element.click()
    #レッスン n－3の開始ボタン
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[2]'))
    )
    element.click()
def q_one(number):
    df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
    df = df.loc[:,["e","j"]]
    df = df.dropna(how='any',axis=0)
    df.to_csv(CSV_PATH, index = False, encoding='cp932')

    bar_open(number)
    q_one_start(number)
    wait.until(EC.presence_of_all_elements_located)
    time.sleep(2)

    e_space = ""
    j_space = ""
    is_full = True
    check = []
    while True:
        if len(browser.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(browser.find_elements(By.CLASS_NAME,'View-Button')) != 5: #ココ怪しい
            break
        df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
        e = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
        )
        j1 = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))
        )
        j2 = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
        )
        #データがない場合
        if df[df["e"] == e.text].empty:
            e_space = e.text
            j_space = j1.text #間違えた選択肢を２回踏まないように記録
            j1.click()
            time.sleep(4)
            if len(browser.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(browser.find_elements(By.CLASS_NAME,'View-Button')) != 5: #ココ怪しい
                break
            time.sleep(2)
            #合ってたら次のページにいってる
            e = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
            )
            #間違えたかどうか判定
            if e_space == e.text: #間違えたとき
                is_full = False
                j1 = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))#選択肢取り直して
                )
                j2 = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
                )
                if j_space == j1.text: #前回と違う選択肢を選ぶ
                    j2.click()
                    df = df.append({"e":e.text,"j":j2.text}, ignore_index=True)
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
                elif j_space == j2.text:
                    j1.click()
                    df = df.append({"e":e.text,"j":j1.text}, ignore_index=True)
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            else: #合ってたとき 
                df = df.append({"e":e.text,"j":j1.text}, ignore_index=True)
                df.to_csv(CSV_PATH, index = False, encoding='cp932')
            time.sleep(4)
        # 既にデータがある場合
        else:
            check.append(e.text)
            if df[df["e"] == e.text].iat[0,1] == j1.text:
                j1.click()
                if check.count(e.text) > 3:
                    check = []
                    df.loc[df["e"] == e.text,"j"] = j2.text
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            elif df[df["e"] == e.text].iat[0,1] == j2.text:
                j2.click()
                if check.count(e.text) > 3:
                    check = []
                    df.loc[df["e"] == e.text,"j"] = j1.text
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            if check.count(e.text) > 4:
                if check.count(e.text) % 2 == 0:
                    df.loc[df["e"] == e.text,"j"] = j1.text
                else:
                    df.loc[df["e"] == e.text,"j"] = j2.text
                df.to_csv(CSV_PATH, index = False, encoding='cp932')
            time.sleep(4)

    # [おわり]ボタン
    wait.until(EC.presence_of_all_elements_located)
    if is_full: #100%だと復習ボタンがでてこないので分岐
        element = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
        )
        element.click()
    else:
        element = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]'))
        )
        element.click()
    time.sleep(10)
def q_two(number):
    #region df
    df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
    df = df.loc[:,["e","j"]]
    df = df.dropna(how='any',axis=0)
    df.to_csv(CSV_PATH, index = False, encoding='cp932')
    #endregion
    #region question start
    bar_open(number)
    q_two_start(number)
    wait.until(EC.presence_of_all_elements_located)
    time.sleep(2)
    #endregion

    q_space = ""
    s_space = ""
    is_full = True
    check = []
    while True:
        if len(browser.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(browser.find_elements(By.CLASS_NAME,'View-Button')) != 4: #ココ怪しい
            break
        df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
        q = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
        )
        s1 = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))
        )
        s2 = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
        )

        #データがない場合
        if df[df["j"] == q.text].empty:
            q_space = q.text
            s_space = s1.text #間違えた選択肢を２回踏まないように記録
            s1.click()
            time.sleep(4)
            if len(browser.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(browser.find_elements(By.CLASS_NAME,'View-Button')) != 4: #ココ怪しい
                break
            time.sleep(2)
            #合ってたら次のページにいってる
            q = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
            )
            #間違えたかどうか判定
            if q_space == q.text: #間違えたとき
                is_full = False
                s1 = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))#選択肢取り直して
                )
                s2 = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
                )
                if s_space == s1.text: #前回と違う選択肢を選ぶ
                    s2.click()
                    df = df.append({"e":s2.text,"j":q.text}, ignore_index=True)
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
                elif s_space == s2.text:
                    s1.click()
                    df = df.append({"e":s1.text,"j":q.text}, ignore_index=True)
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            else: #合ってたとき 
                df = df.append({"e":s1.text,"j":q.text}, ignore_index=True)
                df.to_csv(CSV_PATH, index = False, encoding='cp932')
            time.sleep(4)
        # 既にデータがある場合
        else:
            check.append(q.text)
            if df[df["j"] == q.text].iat[0,0] == s1.text:
                s1.click()
                if check.count(q.text) > 3:
                    check = []
                    df.loc[df["j"] == q.text,"q"] = s2.text
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            elif df[df["j"] == q.text].iat[0,0] == s2.text:
                s2.click()
                if check.count(q.text) > 3:
                    check = []
                    df.loc[df["j"] == q.text,"e"] = s1.text
                    df.to_csv(CSV_PATH, index = False, encoding='cp932')
            if check.count(q.text) > 4:
                if check.count(q.text) % 2 == 0:
                    df.loc[df["j"] == q.text,"e"] = s1.text
                else:
                    df.loc[df["j"] == q.text,"e"] = s2.text
                df.to_csv(CSV_PATH, index = False, encoding='cp932')
            time.sleep(4)

    # [おわり]ボタン
    wait.until(EC.presence_of_all_elements_located)
    if is_full: #100%だと復習ボタンがでてこないので分岐
        element = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
        )
        element.click()
    else:
        element = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]'))
        )
        element.click()
    time.sleep(10)
def q_three(number):
    bar_open(number)
    q_three_start(number)
    wait.until(EC.presence_of_all_elements_located)
    time.sleep(1)

    while True:
        cards = browser.find_elements(By.CLASS_NAME,"View-DragDropCard-Word")
        if len(cards) <= 0:
            break
        for i in range(len(cards)):
            cards[i].click()
            time.sleep(0.1)
        element = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div'))
        )
        if element.text == "採点する":
            element.click()
            time.sleep(3)

    # [おわり]ボタン
    wait.until(EC.presence_of_all_elements_located)
    element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
    )
    element.click()
    time.sleep(10)

index = range(1,21)
# index = [20]
for i in index:
#     q_one(i)
#     q_two(i)
    q_three(i)


print("プログラム終了")

#パート３ //*[@id="tab_root"]/li[3]/a
# レッスンの閉じてるバー
# //*[@id="course-detail"]/div[1]
# //*[@id="course-detail"]/div[2]
# レッスン１
# //*[@id="course-detail"]/div[1]/div[2]/div[2]/div[2]/div[1]
# //*[@id="course-detail"]/div[1]/div[2]/div[2]/div[2]/div[2]
# //*[@id="course-detail"]/div[1]/div[2]/div[3]/div[2]/div
# レッスン２
# //*[@id="course-detail"]/div[2]/div[2]/div[2]/div[2]/div[1]
# //*[@id="course-detail"]/div[2]/div[2]/div[2]/div[2]/div[2]
# //*[@id="course-detail"]/div[2]/div[2]/div[3]/div[2]/div
# レッスン２０
# //*[@id="course-detail"]/div[20]/div[2]/div[2]/div[2]/div[1]

#パート４//*[@id="tab_root"]/li[4]/a
# レッスンの閉じてるバー
# //*[@id="course-detail"]/div[1]
#レッスン１
# //*[@id="course-detail"]/div[1]/div[2]/div[2]/div[2]/div[1]


def qn_score_get(n):
    score = []
    for i in range(1,21):
        bar_open(i)
        time.sleep(0.5)
        if n != 3:
            s = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,f'//*[@id="course-detail"]/div[{i}]/div[2]/div[2]/div[2]/div[{n}]/div[8]/div[1]'))
            )
        elif n == 3:
            s = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,f'//*[@id="course-detail"]/div[{i}]/div[2]/div[3]/div[2]/div/div[8]/div[1]'))
            )
        score.append(s.text)
    score = list(map(int,score))
    return score
        
def must_do_index(all_score):
    index = []
    for i in range(20):
        if all_score[i] < 80:
            index.append(i)
    return index

# ８０点以下のindex取得 1or2
# score = qn_score_get(1)
# score = qn_score_get(2)
# score = qn_score_get(3)
# print(score)
# index = must_do_index(score)
# print(index)



#カード
# View-DragDropCard-Word
# 選択されたカード、固定されたカード
#View-DragDropCard-Placed
#固定されたカード
# View-DragDropCard-Correct
