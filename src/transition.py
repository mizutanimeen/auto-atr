from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import os

def Login(aWait: WebDriverWait) -> None:
    #ログイン動作
    tIdInput = aWait.until(EC.presence_of_element_located((By.ID, "id")))
    tIdInput.clear()
    tID = ""
    try:
        tID = os.environ['ID']
    except:
        pass
    finally:
        if tID == "":
            print("IDを入力してください。")
            tID = input('>> ')
    tIdInput.send_keys(tID)
    
    tPassInput = aWait.until(EC.presence_of_element_located((By.ID, "pw")))
    tPassInput.clear()
    tPassword = ""
    try:
        tPassword = os.environ['PASSWORD']
    except:
        pass
    finally:
        if tPassword == "":
            print("PASSWORDを入力してください。")
            tPassword = input('>> ')
    tPassInput.send_keys(tPassword)

    tSendBtn = aWait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
    tSendBtn.click()

    #ログイン確認
    try:
        _ = aWait.until(EC.presence_of_element_located((By.ID, "large-button-class")))
    except:
        raise ValueError("ログイン失敗")
    
    return #成功

def Setting(aDriver:webdriver.Remote,aWait: WebDriverWait) -> str:
    tMsg = ""

    tNameArea = aWait.until(EC.presence_of_element_located((By.ID, "nameArea")))
    tNameArea.click()

    tCheckLabels = aWait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/form/div/div/div[2]/div[10]//label[@class='label-checkbox']")))
    tCheckBoxs = aWait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/form/div/div/div[2]/div[10]//label[@class='label-checkbox']/input")))
    tCheckTexts = aWait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/form/div/div/div[2]/div[10]//label[@class='label-checkbox']/span")))
    for i in range(len(tCheckBoxs)):
        if tCheckBoxs[i].is_selected():
            tCheckLabels[i].click()
            tMsg += f"{tCheckTexts[i].text}\n"

    tSaveBtn = aWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div/div/div[2]/div[12]/a[2]")))
    tSaveBtn.click()

    Alert(aDriver).accept()
    
    tBackBtn = aWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/a/img")))
    tBackBtn.click()

    return tMsg

def inputIndex(aElement:EC.WebElement) -> int:
    while True:
        tIndex = input('>> ')
        if tIndex.isdecimal() and int(tIndex) < len(aElement):
            return int(tIndex)

#移動先と移動したパートを配列と文字で返してる
def ClassCoursePart(aWait: WebDriverWait) -> None:
    tResult = []

    tClassBtn = aWait.until(EC.presence_of_element_located((By.ID, "large-button-class")))
    tClassBtn.click()

    tClasses = aWait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "class-list-item-name")))
    for i in range(len(tClasses)):
        print(f"{i} : {tClasses[i].text}")

    print('クラスを選択してください。')
    tIndex = inputIndex(aElement=tClasses)
    tResult.append(tClasses[tIndex].text)
    tClasses[tIndex].click()

    tCourses = aWait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "class-detail-item-name")))
    for i in range(len(tCourses)):
        print(f"{i} : {tCourses[i].text}")

    print('コースを選択してください。')
    tIndex = inputIndex(aElement=tCourses)
    tResult.append(tCourses[tIndex].text)
    tCourses[tIndex].click()

    tParts = aWait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "none-bookmark")))
    for i in range(len(tParts)):
        print(f"{i} : {tParts[i].text}")

    print('パートを選択してください。')
    tIndex = inputIndex(aElement=tParts)
    tResult.append(tParts[tIndex].text)
    tParts[tIndex].click()

    tPart = str(tIndex + 1)
    return tResult,tPart
