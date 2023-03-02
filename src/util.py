from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os


def GetSelectionsElement(aDriver):
    tSelectionElementOne = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]'))
    )
    tSelectionElementTwo = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]'))
    )
    return [tSelectionElementOne,tSelectionElementTwo]
