import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import util

import data

class TranslationTaskManager():
    driver: webdriver.Remote
    wait: WebDriverWait
    filePath: str
    data: pd.DataFrame
    columnName: str[2] #[questionColumnName,selectionColumnName]

    def __init__(self,aDriver: webdriver.Remote,aWait: WebDriverWait,aBaseDataPath: str,aColumnName: str[2]) -> None:
        self.driver = aDriver
        self.wait = aWait
        self.filePath = aBaseDataPath + "je.csv"
        self.columnName = aColumnName

        data.TranslationFileIfNotExistCreate(self.filePath)
        data.TranslationDataOrganization(self.filePath)
        return 
    
    def ReadData(self) -> None:
        tData = pd.read_csv(self.filePath, sep=",", encoding='utf_8')
        self.data = tData
        return 
    
    def SaveData(self,aQuestionText:str,aSelectionText:str) -> None:
        tNewData = pd.DataFrame(
            data={self.columnName[0]: [aQuestionText], 
                self.columnName[1]: [aSelectionText]}
        )
        self.data = pd.concat([self.data,tNewData],ignore_index=True)
        self.data.to_csv(self.filePath, index = False, encoding='utf_8')
        return 

    def TaskRun(self) -> None:
        try: #終了判定
            _ = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return
        except: pass

        self.ReadData()
        tQuestionElement = self.wait.until( EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')) )
        tSelectionsElement = util.GetSelectionsElement(self.driver)
        print(tQuestionElement.text) # ログの出し方どうなん
        
        #見ずらいから外に出しとく
        tQuestionData = self.data[self.columnName[0]]
        tEquals = (tQuestionData == tQuestionElement.text)

        if self.data[tEquals].empty: #データがない場合
            if self.TaskNotExistData(self,tQuestionElement,tSelectionsElement):
                return
        else: #データがある場合
            if self.TaskExistData(self,tQuestionElement,tSelectionsElement):
                return

        self.TaskRun() #再帰
        return 

    def TaskNotExistData(self,aQuestionElement,aSelectionsElement) -> bool:
        tOldQuestionText = aQuestionElement.text
        tOldSelectionsText = [aSelectionsElement[0].text,aSelectionsElement[1].text]
        aSelectionsElement[0].click()
        try: #終了判定
            _ = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            self.SaveData(tOldQuestionText,tOldSelectionsText[0])
            return True
        except: pass
        
        tQuestionElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')))
        tSelectionsElement = util.GetSelectionsElement(self.driver)
        
        #間違っていた場合
        if tOldQuestionText == tQuestionElement.text: 
            tSelectionsElement[1].click() if tOldSelectionsText[0] == tSelectionsElement[0].text else tSelectionsElement[0].click()
            self.SaveData(tOldQuestionText,tOldSelectionsText[1])
        #合っていた場合
        else:
            self.SaveData(tOldQuestionText,tOldSelectionsText[0])

        return False   

    def TaskExistData(self,aQuestionElement,aSelectionsElement) -> bool:
        tOldQuestionText = aQuestionElement.text
        tSelectionsText = [aSelectionsElement[0].text,aSelectionsElement[1].text]
        #見ずらいから外に出しとく
        tQuestionData = self.data[self.columnName[0]]
        tEquals = (tQuestionData == tOldQuestionText)
        tSelectionOfEquals = self.data[tEquals][self.columnName[1]].iat[0]

        if tSelectionOfEquals == tSelectionsText[0]:
            aSelectionsElement[0].click()
            self.data.loc[tEquals, self.columnName[1]] = tSelectionsText[1] #間違っていた時のために予めローカルデータを書き換えておく
        elif tSelectionOfEquals == tSelectionsText[1]:
            aSelectionsElement[1].click()
            self.data.loc[tEquals, self.columnName[1]] = tSelectionsText[0] #間違っていた時のために予めローカルデータを書き換えておく
    
        try: #終了判定
            _ = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return True
        except: pass

        tQuestionElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')))
        if tQuestionElement.text == tOldQuestionText: # 間違っていた時
            self.data.to_csv(self.filePath, index = False, encoding='utf_8')# 間違いが確定したためファイルに保存する

        return False

def TaskThreeNotExistData(aDriver,aData,aFilePath,aSelectionsElement,aOldSelectionsText):
    aSelectionsElement[0].click()
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        tNewData = pd.DataFrame(
            data={"one": [aOldSelectionsText[0]], 
                "two":  [aOldSelectionsText[1]],
                "ans": [aOldSelectionsText[0]]}
        )
        aData = pd.concat([aData,tNewData],ignore_index=True)
        aData.to_csv(aFilePath, index = False, encoding='utf_8')
        return True
    except: pass
    tSelectionsElement = util.GetSelectionsElement(aDriver)
    #間違ってた時
    if ((tSelectionsElement[0].text == aOldSelectionsText[0]) or (tSelectionsElement[0].text == aOldSelectionsText[1])) and\
         ((tSelectionsElement[1].text == aOldSelectionsText[1]) or (tSelectionsElement[0].text == aOldSelectionsText[1])): #キー直打ちやめる
        tSelectionsElement[1].click() if aOldSelectionsText[0] == tSelectionsElement[0].text else tSelectionsElement[0].click()
        tNewData = pd.DataFrame(
            data={"one": [aOldSelectionsText[0]], 
                "two":  [aOldSelectionsText[1]],
                "ans": [aOldSelectionsText[1]]}
        )

    else:#当たっていた時
        tNewData = pd.DataFrame(
            data={"one": [aOldSelectionsText[0]], 
                "two":  [aOldSelectionsText[1]],
                "ans": [aOldSelectionsText[0]]}
        )
    aData = pd.concat([aData,tNewData],ignore_index=True)
    aData.to_csv(aFilePath, index = False, encoding='utf_8')
    return False

#処理合ってるかわからん、条件が冗長でわかりずらい、なんとかする
def TaskThreeExistData(aDriver,aData,aFilePath,aSelectionsElement,aOldSelectionsText):
    if aData[((aData["one"] == aOldSelectionsText[0]) | (aData["one"] == aOldSelectionsText[1])) &\
         ((aData["two"] == aOldSelectionsText[0]) | (aData["two"] == aOldSelectionsText[1]))]["ans"].iat[0] == aSelectionsElement[0].text:
        aSelectionsElement[0].click()
        aData.loc[(aData["one"] == aOldSelectionsText[0] | aData["one"] == aOldSelectionsText[1]) &\
         ((aData["two"] == aOldSelectionsText[0]) | (aData["two"] == aOldSelectionsText[1])),"ans"] = aSelectionsElement[1].text
    else:
        aSelectionsElement[1].click()
        aData.loc[(aData["one"] == aOldSelectionsText[0] | aData["one"] == aOldSelectionsText[1]) &\
         ((aData["two"] == aOldSelectionsText[0]) | (aData["two"] == aOldSelectionsText[1])),"ans"] = aSelectionsElement[0].text
    
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        return True
    except: pass

    tSelectionsElement = util.GetSelectionsElement(aDriver)
    
    # データがおかしい時
    if ((tSelectionsElement[0].text == aOldSelectionsText[0]) or (tSelectionsElement[0].text == aOldSelectionsText[1])) and \
        ((tSelectionsElement[1].text == aOldSelectionsText[0]) or (tSelectionsElement[1].text == aOldSelectionsText[1])):
        aData.to_csv(aFilePath, index = False, encoding='utf_8')
    return False

