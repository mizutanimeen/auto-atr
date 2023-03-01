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

def login(aDriver):
    print("login")
    #ページに移動
    url_login = "https://atr.meijo-u.net/"
    aDriver.get(url_login)
    #ログイン動作
    element = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "id"))
    )
    element.clear()
    element.send_keys(os.environ['ID'])
    element = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.ID, "pw"))
    )
    element.clear()
    element.send_keys(os.environ['PASSWORD'])
    element = WebDriverWait(aDriver, 30).until(
        EC.element_to_be_clickable((By.ID, "submit-button"))
    )
    element.click()
    print("ok")
    print("ok")
    print("ok")
    print("ok")
    print("ok")
    exit(1)
    #class
    element = WebDriverWait(aDriver, 100).until(
        EC.presence_of_element_located((By.ID, "large-button-class"))
    )
    element.click()
    #Pre3-4  
    element = WebDriverWait(aDriver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="class_container"]/div[1]/a'))
    )
    element.click()
    #Pre4  
    element = WebDriverWait(aDriver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wpContents"]/div[2]/div[6]/div[1]'))
    )
    element.click()
    # パート
    PART = 1 #ココ引数に変える
    element = WebDriverWait(aDriver, 100).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="tab_root"]/li[{PART}]/a'))
    )
    element.click()
