from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import task.task as task

BASE_POINT = 80

#指定パートの８０点未満の問題全てやる
def DoLesson(aDriver: webdriver.Remote,aWait: WebDriverWait,aBaseDataPath:str):# -> list,list
    tResult = []
    tLessResult = []
    tTaskLen = 0

    for i in range(20):
        aWait.until(EC.presence_of_all_elements_located)
        tBars = aWait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-detail-unit-bar')))
        tBars[i].click()
        if i == 0:
            tTasksScore = aWait.until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-hiscore']")))
            tTaskLen = len(tTasksScore)

        for j in range(tTaskLen):
            tTasksName = aWait.until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-name pre-wrap']")))
            tTasksScore = aWait.until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[2]/div/div[7]/div[{i+1}]/div[2]//div[@class='course-detail-brix-hiscore']")))

            if not(tTasksScore[j].text.isdecimal() and int(tTasksScore[j].text) >= BASE_POINT):
                tTaskName = tTasksName[j].text
                print(f"[レッスン{i+1}]<{tTaskName}>が{BASE_POINT}点未満のため実行")
                tTasksName[j].click()

                tScore = task.Do(aDriver=aDriver,aWait=aWait,aTaskName=tTaskName,aBaseDataPath=aBaseDataPath)

                print(f"結果{tScore}点")
                tResult.append(f"[レッスン{i+1}]<{tTaskName}>:{tScore}点")
                if tScore < BASE_POINT:
                    tLessResult.append(f"[レッスン{i+1}]<{tTaskName}>:{tScore}点")
                    
                time.sleep(1)

    return tResult,tLessResult
