from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

import data
import util
import task

#問題を終わるとやった場所は開いたまま
#別のところをやると他は閉じる

BASE_POINT = 80 #今後変えるかもしれないから定数に念のためしておく

def q_one(number,aDriver,aWait):
    e_space = ""
    j_space = ""
    is_full = True
    check = []
    while True:
        aWait.until(EC.presence_of_all_elements_located)
        if len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) != 5: #ココ怪しい
            break
        df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
        e = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
        )
        j1 = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))
        )
        j2 = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
        )
        #データがない場合
        if df[df["e"] == e.text].empty:
            e_space = e.text
            j_space = j1.text #間違えた選択肢を２回踏まないように記録
            j1.click()
            time.sleep(4)
            if len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) != 5: #ココ怪しい
                break
            time.sleep(2)
            #合ってたら次のページにいってる
            e = WebDriverWait(aDriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
            )
            #間違えたかどうか判定
            if e_space == e.text: #間違えたとき
                is_full = False
                j1 = WebDriverWait(aDriver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))#選択肢取り直して
                )
                j2 = WebDriverWait(aDriver, 10).until(
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
    aWait.until(EC.presence_of_all_elements_located)
    if is_full: #100%だと復習ボタンがでてこないので分岐
        element = WebDriverWait(aDriver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
        )
        element.click()
    else:
        element = WebDriverWait(aDriver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]'))
        )
        element.click()
    time.sleep(10)
def q_two(number,aDriver,aWait):
    #region df
    df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
    df = df.loc[:,["e","j"]]
    df = df.dropna(how='any',axis=0)
    df.to_csv(CSV_PATH, index = False, encoding='cp932')
    #endregion
    #region question start
    BarOpen(number)
    q_two_start(number)
    aWait.until(EC.presence_of_all_elements_located)
    time.sleep(2)
    #endregion

    q_space = ""
    s_space = ""
    is_full = True
    check = []
    while True:
        if len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) != 4: #ココ怪しい
            break
        df = pd.read_csv(CSV_PATH, sep=",", encoding='cp932')
        q = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
        )
        s1 = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))
        )
        s2 = WebDriverWait(aDriver, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
        )

        #データがない場合
        if df[df["j"] == q.text].empty:
            q_space = q.text
            s_space = s1.text #間違えた選択肢を２回踏まないように記録
            s1.click()
            time.sleep(4)
            if len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) > 0 and len(aDriver.find_elements(By.CLASS_NAME,'View-Button')) != 4: #ココ怪しい
                break
            time.sleep(2)
            #合ってたら次のページにいってる
            q = WebDriverWait(aDriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
            )
            #間違えたかどうか判定
            if q_space == q.text: #間違えたとき
                is_full = False
                s1 = WebDriverWait(aDriver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))#選択肢取り直して
                )
                s2 = WebDriverWait(aDriver, 10).until(
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
    aWait.until(EC.presence_of_all_elements_located)
    if is_full: #100%だと復習ボタンがでてこないので分岐
        element = WebDriverWait(aDriver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
        )
        element.click()
    else:
        element = WebDriverWait(aDriver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]'))
        )
        element.click()
    time.sleep(10)
def q_three(number,aDriver,aWait):
    BarOpen(number)
    q_three_start(number)
    aWait.until(EC.presence_of_all_elements_located)
    time.sleep(1)

    while True:
        cards = aDriver.find_elements(By.CLASS_NAME,"View-DragDropCard-Word")
        if len(cards) <= 0:
            break
        for i in range(len(cards)):
            cards[i].click()
            time.sleep(0.1)
        element = WebDriverWait(aDriver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div'))
        )
        if element.text == "採点する":
            element.click()
            time.sleep(3)

    # [おわり]ボタン
    aWait.until(EC.presence_of_all_elements_located)
    element = WebDriverWait(aDriver, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div'))
    )
    element.click()
    time.sleep(10)

def taskOneRun(aDriver,aWait,aDataPath,aColumnName):
    #View-GeneralProgressIcon-correct
    #View-GeneralProgressIcon-noncorrect の数で満点か、合ってたか間違っていたか判断できる？
    try: #終了判定 #確定で時間かかるの微妙
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        return
    except: pass

    tData = pd.read_csv(aDataPath, sep=",", encoding='utf_8')
    tQuestionElement = WebDriverWait(aDriver, 30).until( EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')) )
    tSelectionsElement = util.GetSelectionsElement(aDriver)
    print(tQuestionElement.text)

    if tData[tData[aColumnName[0]] == tQuestionElement.text].empty: #データがない場合
        tSelectionsElement[0].click()
        try: #終了判定 #確定で時間かかるの微妙
            _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return 
        except: pass
        time.sleep(3)
        task.TaskOneNotExistData(aDriver,tData,aDataPath,tQuestionElement,tSelectionsElement,aColumnName)
    else: #データがある場合
        task.TaskOneExistData(aDriver,tData,aDataPath,tQuestionElement,tSelectionsElement,aColumnName)

    time.sleep(3)
    taskOneRun(aDriver,aWait,aDataPath,aColumnName) #再帰

#単語訳：英日
def taskOne(aDriver,aWait,aBaseDataPath):
    tColumnName = ["english","japanese"] #これよくない

    tDataPath = aBaseDataPath + "je.csv"
    data.FileEnJpIfNotExistCreate(tDataPath)
    data.DataEnJpOrganization(tDataPath)
    aWait.until(EC.presence_of_all_elements_located) #whileの中ではページ遷移してないから使えなさそう
    print("回答開始")
    taskOneRun(aDriver,aWait,tDataPath,tColumnName)
    return
#単語訳：日英
def taskTwo(aDriver,aWait,aBaseDataPath):
    pass
#（聴）単語訳
def taskThree(aDriver,aWait,aBaseDataPath):
    pass
#語句並べ替え
def taskFour(aDriver,aWait):
    pass


def doTask(aDriver,aWait,aTaskName,aBaseDataPath):
    tStartBtn = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]"))
    )
    tStartBtn.click()
    if aTaskName == "単語訳：英日":
        taskOne(aDriver,aWait,aBaseDataPath)
    elif aTaskName == "単語訳：日英":
        taskTwo(aDriver,aWait,aBaseDataPath)
    elif aTaskName == "（聴）単語訳":
        taskThree(aDriver,aWait,aBaseDataPath)
    elif aTaskName == "語句並べ替え":
        taskFour(aDriver,aWait)
    else:
        pass #エラー処理いる？
    return

#指定パートの８０点未満の問題全てやる
def DoLesson(aDriver,aWait,aBaseDataPath):
    aWait.until(EC.presence_of_all_elements_located)
    tBars = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-detail-unit-bar'))
    )
    for i in range(len(tBars)):
        tBars[i].click()
        tTasksName = WebDriverWait(aDriver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-detail-brix-name'))
        )
        tTasksScore = WebDriverWait(aDriver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-detail-brix-hiscore'))
        )
        for j in range(len(tTasksScore)):
            if not(tTasksScore[j].text.isdecimal() and int(tTasksScore[j].text) >= BASE_POINT):
                tTaskName = tTasksName[j].text
                print(f"[レッスン{i+1}]<{tTaskName}>が{BASE_POINT}点未満のため実行")
                tTasksName[j].click()
                doTask(aDriver,aWait,tTaskName,aBaseDataPath)
                time.sleep(100)
                #戻ってきたら点数確認してリトライするか確認、ループで、2回以上はさすがにスキップとか
    return
