from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import translation
from . import listen
from . import sort

def start(aWait: WebDriverWait) -> None:
    tStartBtn = aWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]")))
    tStartBtn.click()
    aWait.until(EC.presence_of_all_elements_located)
    return 

def finish(aWait: WebDriverWait) -> int:
    tScoreElement = aWait.until( EC.presence_of_element_located((By.CLASS_NAME, "View-Header-ResultScoreValue")) )
    tScore = int(tScoreElement.text)
    if tScore == 100:
        tEndBtn = aWait.until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div")) )
    else:
        tEndBtn = aWait.until( EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div[2]/div[2]")) )
    tEndBtn.click()
    return tScore

def Do(aDriver: webdriver.Remote,aWait: WebDriverWait,aTaskName:str,aBaseDataPath:str) -> int:
    start(aWait=aWait)
    
    print("回答開始")
    
    if aTaskName == "単語訳：英日": #ここら辺の名前の分岐、BW03みたいなやつ参照の方がよい？
        tColumnName = [translation.TRANSLATION_COLUMN_NAME[0],translation.TRANSLATION_COLUMN_NAME[1]]
        tTaskManager = translation.TaskManager(aDriver=aDriver,aWait=aWait,aBaseDataPath=aBaseDataPath,aColumnName=tColumnName)
    elif aTaskName == "単語訳：日英":
        tColumnName = [translation.TRANSLATION_COLUMN_NAME[1],translation.TRANSLATION_COLUMN_NAME[0]]
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

    return finish(aWait=aWait)