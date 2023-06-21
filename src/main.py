from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
import traceback
import time

import transition
import lesson
import data

def main(aDriver:webdriver.Remote) -> None:
    tWait = WebDriverWait(driver=aDriver, timeout=30)

    tUrl = "https://atr.meijo-u.net"
    if requests.get(url=tUrl).status_code != 200:
        print(tUrl + "にアクセスできませんでした。")
        return
    aDriver.get(url=tUrl)
    aDriver.maximize_window()

    try:
        transition.Login(aWait=tWait)
    except:
        traceback.print_exc()
        print("IDやPASSWORDか異なっている可能性があります。\n.envを確認し間違っている場合は.envを書き換え\ndocker-compose up -d\nを実行してください")
        return
    print("ログイン成功")

    try:
        tMsg = transition.Setting(aDriver=aDriver,aWait=tWait)
    except:
        traceback.print_exc()
        return
    if len(tMsg) != 0:
        print("設定のメッセージの表示を編集し、以下のチェックを外しました。")
        print("(チェックしたものが学習後表示されます)")
        print(tMsg)

    try:
        tResult,tPart = transition.ClassCoursePart(aWait=tWait)
    except:
        traceback.print_exc()
        return
    print(f"{tResult}に移動")

    try:
        tBaseDataPath = data.GetBasePath(aCourse=tResult[1],aPart=tPart)
    except:
        traceback.print_exc()
        return

    for i in range(1,3):
        print(f"-----{i}回目-----")
        try:
            tResult,tLessResult = lesson.Do(aDriver=aDriver,aWait=tWait,aBaseDataPath=tBaseDataPath)
        except:
            traceback.print_exc()
            return
    print("-----全ての結果-----")
    for i in tResult:
        print(i)
    print("-----80点未満の結果-----")
    for i in tLessResult:
        print(i)
    return

if __name__ == "__main__":
    try:
        print("START")
        tStartTime = time.time()
        tDriver = webdriver.Remote(
            command_executor = os.environ["SELENIUM_URL"],
            options = webdriver.ChromeOptions()
        )
        main(aDriver=tDriver)
    finally:
        tDriver.quit()
        print(f"経過時間：{format((time.time() - tStartTime)/60, '.2f')}分")
        print("FINISH")
