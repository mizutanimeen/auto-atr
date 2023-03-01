from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os


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
