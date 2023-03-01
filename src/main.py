from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import traceback
import requests

import transition


def main(aDriver):
    print("START")
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
    transition.Class(aDriver)

if __name__ == "__main__":
    try:
        tDriver = webdriver.Remote(
            command_executor = os.environ["SELENIUM_URL"],
            options = webdriver.ChromeOptions()
        )
        main(tDriver)
    finally:
        tDriver.quit()
