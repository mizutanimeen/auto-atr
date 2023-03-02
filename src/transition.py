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
import time

def Login(aDriver):
    #ログイン動作
    tIdInput = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "id"))
    )
    tIdInput.clear()
    tIdInput.send_keys(os.environ['ID'])
    tPassInput = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "pw"))
    )
    tPassInput.clear()
    tPassInput.send_keys(os.environ['PASSWORD'])
    tSendBtn = WebDriverWait(aDriver, 30).until(
        EC.element_to_be_clickable((By.ID, "submit-button"))
    )
    tSendBtn.click()

    #ログイン確認
    try:
        _ = WebDriverWait(aDriver, 30).until(
            EC.presence_of_element_located((By.ID, "large-button-class"))
        )
    except:
        raise ValueError("ログイン失敗")
    return #成功

def inputIndex(aElement):
    while True:
        tIndex = input('>> ')
        if tIndex.isdecimal() and int(tIndex) < len(aElement):
            return int(tIndex)

def ClassCoursePart(aDriver):
    tResult = []

    tClassBtn = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "large-button-class"))
    )
    tClassBtn.click()

    tClasses = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "class-list-item-name"))
    )
    for i in range(len(tClasses)):
        print(f"{i} : {tClasses[i].text}")
    print('クラスを選択してください。')
    tIndex = inputIndex(tClasses)
    tResult.append(tClasses[tIndex].text)
    tClasses[tIndex].click()

    tCourses = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "class-detail-item-name"))
    )
    for i in range(len(tCourses)):
        print(f"{i} : {tCourses[i].text}")
    print('コースを選択してください。')
    tIndex = inputIndex(tCourses)
    tResult.append(tCourses[tIndex].text)
    tCourses[tIndex].click()

    tParts = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "none-bookmark"))
    )
    for i in range(len(tParts)):
        print(f"{i} : {tParts[i].text}")
    print('パートを選択してください。')
    tIndex = inputIndex(tParts)
    tResult.append(tParts[tIndex].text)
    tParts[tIndex].click()
    tPart = tIndex + 1
    return tResult,tPart
