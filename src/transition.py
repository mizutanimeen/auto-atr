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
    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "id"))
    )
    tElement.clear()
    tElement.send_keys(os.environ['ID'])
    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "pw"))
    )
    tElement.clear()
    tElement.send_keys(os.environ['PASSWORD'])
    tElement = WebDriverWait(aDriver, 30).until(
        EC.element_to_be_clickable((By.ID, "submit-button"))
    )
    tElement.click()

    #ログイン確認
    try:
        tElement = WebDriverWait(aDriver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login_err_content"))
        )
    except:
        return #ログイン成功
    raise ValueError("ログイン失敗")

def inputIndex(aElement):
    while True:
        tIndex = input('>> ')
        if tIndex.isdecimal() and int(tIndex) < len(aElement):
            return int(tIndex)

def ClassCoursePart(aDriver):
    tMessage = ""

    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "large-button-class"))
    )
    tElement.click()

    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "class-list-item-name"))
    )
    for i in range(len(tElement)):
        print(f"{i} : {tElement[i].text}")
    print('クラスを選択してください。')
    tIndex = inputIndex(tElement)
    tMessage += f"{tElement[tIndex].text}\n"
    tElement[tIndex].click()

    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "class-detail-item-name"))
    )
    for i in range(len(tElement)):
        print(f"{i} : {tElement[i].text}")
    print('コースを選択してください。')
    tIndex = inputIndex(tElement)
    tMessage += f"{tElement[tIndex].text}\n"
    tElement[tIndex].click()

    tElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "none-bookmark"))
    )
    for i in range(len(tElement)):
        print(f"{i} : {tElement[i].text}")
    print('パートを選択してください。')
    tIndex = inputIndex(tElement)
    tMessage += f"{tElement[tIndex].text}\n"
    tElement[tIndex].click()
    return tMessage
