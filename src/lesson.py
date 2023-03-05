from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

import data
import util
import task

BASE_POINT = 80 #今後変えるかもしれないから定数に念のためしておく

def taskThreeRun(aDriver, aFilePath):
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        return
    except: pass

    tData = pd.read_csv(aFilePath, sep=",", encoding='utf_8')
    tSelectionsElement = util.GetSelectionsElement(aDriver)
    tOldSelectionsText = [tSelectionsElement[0].text,tSelectionsElement[1].text]

    #データがない場合
    if tData[((tData["one"] == tOldSelectionsText[0]) | (tData["one"] == tOldSelectionsText[1])) &\
         ((tData["two"] == tOldSelectionsText[0]) | (tData["two"] == tOldSelectionsText[1]))].empty: #キー直打ちやめる
        if task.TaskThreeNotExistData(aDriver,tData,aFilePath,tSelectionsElement,tOldSelectionsText):
            return
    else: #データがある場合
        if task.TaskThreeExistData(aDriver,tData,aFilePath,tSelectionsElement,tOldSelectionsText):
            return

    taskThreeRun(aDriver,aFilePath)
    return

#（聴）単語訳
def taskThree(aDriver,aWait,aBaseDataPath):
    print("3start")
    tFilePath = aBaseDataPath + "li.csv"
    data.FileLiIfNotExistCreate(tFilePath)
    data.DataLiOrganization(tFilePath)
    aWait.until(EC.presence_of_all_elements_located) #whileの中ではページ遷移してないから使えなさそう

    print("回答開始")
    taskThreeRun(aDriver,tFilePath)
    return 

def taskFourRun(aDriver,aWait):
    try:
        tCards = WebDriverWait(aDriver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'View-DragDropCard-Word'))
        )
    except:
        return
    for i in range(len(tCards)):
        tCards[i].click()
        time.sleep(0.5)
    tBtn = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div'))
    )
    if tBtn.text == "採点する":
        tBtn.click()
        time.sleep(3)
    taskFourRun(aDriver,aWait)
    return

#語句並べ替え
def taskFour(aDriver,aWait):
    aWait.until(EC.presence_of_all_elements_located) #whileの中ではページ遷移してないから使えなさそう
    
    print("回答開始")
    taskFourRun(aDriver,aWait)
    return

def taskStart(aDriver) -> None:
    tStartBtn = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]"))
    )
    tStartBtn.click()
    return 

def taskFinish(aDriver) -> int:
    tScore = WebDriverWait(aDriver, 30).until( EC.presence_of_element_located((By.CLASS_NAME, "View-Header-ResultScoreValue")) )
    tScore = int(tScore.text)
    if tScore == 100:
        tEndBtn = WebDriverWait(aDriver, 30).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div")) )
    else:
        tEndBtn = WebDriverWait(aDriver, 30).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div[2]")) )
    tEndBtn.click()
    return tScore

def doTask(aDriver,aWait,aTaskName,aBaseDataPath):
    taskStart(aDriver=aDriver)
    aWait.until(EC.presence_of_all_elements_located)
    print("回答開始")
    
    if aTaskName == "単語訳：英日": #ここら辺の名前の分岐、BW03みたいなやつ参照の方がよい？
        tColumnName = ["english","japanese"] #これよくなさそう
        tTaskManager = task.TranslationTaskManager(aDriver=aDriver,aWait=aWait,aFilePath=aBaseDataPath,aColumnName=tColumnName)
    elif aTaskName == "単語訳：日英":
        tColumnName = ["japanese","english"] #これよくなさそう
        tTaskManager = task.TranslationTaskManager(aDriver=aDriver,aWait=aWait,aFilePath=aBaseDataPath,aColumnName=tColumnName)
    elif aTaskName == "（聴）単語訳":
        taskThree(aDriver,aWait,aBaseDataPath)
    elif aTaskName == "（聴）語句並べ替え":
        taskFour(aDriver,aWait)
    elif aTaskName == "語句並べ替え":
        taskFour(aDriver,aWait)
    else:
        raise ValueError(f"想定していない問題:{aTaskName}")
    
    tTaskManager.TaskRun()

    return taskFinish(aDriver)

#指定パートの８０点未満の問題全てやる
def DoLesson(aDriver,aWait,aBaseDataPath):
    tResult = []
    tLessResult = []
    tTaskLen = 0

    for i in range(20):
        aWait.until(EC.presence_of_all_elements_located)
        tBars = WebDriverWait(aDriver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-detail-unit-bar'))
        )
        tBars[i].click()
        if i == 0:
            tTasksScore = WebDriverWait(aDriver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-hiscore']"))
            )
            tTaskLen = len(tTasksScore)

        for j in range(tTaskLen):
            aWait.until(EC.presence_of_all_elements_located) 
            tTasksName = WebDriverWait(aDriver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-name pre-wrap']"))
            )
            tTasksScore = WebDriverWait(aDriver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-hiscore']"))
            )

            if not(tTasksScore[j].text.isdecimal() and int(tTasksScore[j].text) >= BASE_POINT):
                tTaskName = tTasksName[j].text
                print(f"[レッスン{i+1}]<{tTaskName}>が{BASE_POINT}点未満のため実行")
                tTasksName[j].click()
                tScore = doTask(aDriver,aWait,tTaskName,aBaseDataPath)

                print(f"結果{tScore}点")
                tResult.append(f"[レッスン{i+1}]<{tTaskName}>:{tScore}点")
                if tScore < BASE_POINT:
                    tLessResult.append(f"[レッスン{i+1}]<{tTaskName}>:{tScore}点")
                time.sleep(10)
                #スタンプ獲得も回避しないと
                #戻ってきたら点数確認してリトライするか確認、ループで、2回以上はさすがにスキップとか

    return tResult,tLessResult
