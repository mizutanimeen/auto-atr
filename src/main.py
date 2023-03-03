from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
import traceback
from selenium import webdriver
import time

import transition
import lesson
import data

def main(aDriver):
    tUrl = "https://atr.meijo-u.net"
    if requests.get(tUrl).status_code != 200:
        print(tUrl + "にアクセスできませんでした。")
        return
    aDriver.get(tUrl)

    try:
        transition.Login(aDriver)
    except:
        traceback.print_exc()
        print("IDやPASSWORDか異なっている可能性があります。\n.envを確認し間違っている場合は.envを書き換え\ndocker-compose up -d --build\nを実行してください")
        return
    print("ログイン成功")

    try:
        tResult,tPart = transition.ClassCoursePart(aDriver)
    except:
        traceback.print_exc()
        return
    print(f"{tResult}に移動")

    try:
        tBaseDataPath = data.GetBaseDataPath(tResult[1],tPart)
    except:
        traceback.print_exc()
        return

    try:
        tWait = WebDriverWait(driver=tDriver, timeout=30)
        tResult,tLessResult = lesson.DoLesson(aDriver,tWait,tBaseDataPath)
    except:
        traceback.print_exc()
        return
    print("-----全ての結果-----")
    for i in tResult:
        print(i)
    print("-----80点未満の結果-----")
    for i in tLessResult:
        print(i)

if __name__ == "__main__":
    try:
        print("START")
        tStartTime = time.time()
        tDriver = webdriver.Remote(
            command_executor = os.environ["SELENIUM_URL"],
            options = webdriver.ChromeOptions()
        )
        main(tDriver)
    finally:
        tDriver.quit()
        print(f"経過時間：{format((time.time() - tStartTime)/60, '.2f')}分")
        print("FINISH")
