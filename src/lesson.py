from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import task.translation as translation
import task.listen as listen
import task.sort as sort

BASE_POINT = 80 #今後変えるかもしれないから定数に念のためしておく

def taskStart(aWait: WebDriverWait) -> None:
    tStartBtn = aWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]")))
    tStartBtn.click()
    aWait.until(EC.presence_of_all_elements_located)
    return 

def taskFinish(aWait: WebDriverWait) -> int:
    tScoreElement = aWait.until( EC.presence_of_element_located((By.CLASS_NAME, "View-Header-ResultScoreValue")) )
    tScore = int(tScoreElement.text)
    if tScore == 100:
        tEndBtn = aWait.until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div")) )
    else:
        tEndBtn = aWait.until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div[2]")) )
    tEndBtn.click()
    return tScore

def doTask(aDriver,aWait,aTaskName,aBaseDataPath) -> int:
    taskStart(aWait=aWait)
    
    print("回答開始")
    
    if aTaskName == "単語訳：英日": #ここら辺の名前の分岐、BW03みたいなやつ参照の方がよい？
        tColumnName = ["english","japanese"] #これよくなさそう
        tTaskManager = translation.TaskManager(aDriver=aDriver,aWait=aWait,aBaseDataPath=aBaseDataPath,aColumnName=tColumnName)
    elif aTaskName == "単語訳：日英":
        tColumnName = ["japanese","english"] #これよくなさそう
        tTaskManager = translation.TaskManager(aDriver=aDriver,aWait=aWait,aBaseDataPath=aBaseDataPath,aColumnName=tColumnName)
    elif aTaskName == "（聴）単語訳":
        tTaskManager = listen.TaskManager(aDriver=aDriver,aWait=aWait,aBaseDataPath=aBaseDataPath)
    elif aTaskName == "（聴）語句並べ替え":
        tTaskManager = sort.TaskManager(aDriver=aDriver,aWait=aWait)
    elif aTaskName == "語句並べ替え":
        tTaskManager = sort.TaskManager(aDriver=aDriver,aWait=aWait)
    else:
        raise ValueError(f"想定していない問題:{aTaskName}")
    
    tTaskManager.TaskRun()

    return taskFinish(aWait)

#指定パートの８０点未満の問題全てやる
def DoLesson(aDriver,aWait,aBaseDataPath):# -> list,list
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
