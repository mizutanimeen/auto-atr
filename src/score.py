from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import lesson

def qn_score_get(aDriver,n):
    score = []
    for i in range(1,21):
        lesson.bar_open(i)
        time.sleep(0.5)
        if n != 3:
            s = WebDriverWait(aDriver, 10).until(
                EC.presence_of_element_located((By.XPATH,f'//*[@id="course-detail"]/div[{i}]/div[2]/div[2]/div[2]/div[{n}]/div[8]/div[1]'))
            )
        elif n == 3:
            s = WebDriverWait(aDriver, 10).until(
                EC.presence_of_element_located((By.XPATH,f'//*[@id="course-detail"]/div[{i}]/div[2]/div[3]/div[2]/div/div[8]/div[1]'))
            )
        score.append(s.text)
    score = list(map(int,score))
    return score
        
def must_do_index(all_score):
    index = []
    for i in range(20):
        if all_score[i] < 80:
            index.append(i)
    return index