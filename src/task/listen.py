from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import task.util as util

import data

class TaskManager():
    driver: webdriver.Remote
    wait: WebDriverWait
    filePath: str
    data: pd.DataFrame
    columnName: str[3] #[one,two,ans]

    def __init__(self,aDriver: webdriver.Remote,aWait: WebDriverWait,aBaseDataPath: str) -> None:
        self.driver = aDriver
        self.wait = aWait
        self.filePath = aBaseDataPath + "li.csv"
        self.columnName = ["one","two","ans"]

        data.ListenFileIfNotExistCreate(self.filePath)
        data.ListenDataOrganization(self.filePath)
        return 
    
    def ReadData(self) -> None:
        tData = pd.read_csv(self.filePath, sep=",", encoding='utf_8')
        self.data = tData
        return 
    
    def SaveData(self,aSelectionText:str[2],aAnswerText: str) -> None:
        tNewData = pd.DataFrame(
            data={self.columnName[0]: [aSelectionText[0]], 
                self.columnName[1]: [aSelectionText[1]],
                self.columnName[2]: [aAnswerText]}
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
        tSelectionsElement = util.GetSelectionsElement(self.driver)
        tOldSelectionsText = [tSelectionsElement[0].text,tSelectionsElement[1].text]

        #データがない場合
        if self.data[((self.data["one"] == tOldSelectionsText[0]) | (self.data["one"] == tOldSelectionsText[1])) &\
            ((self.data["two"] == tOldSelectionsText[0]) | (self.data["two"] == tOldSelectionsText[1]))].empty: #キー直打ちやめる
            if self.TaskNotExistData(self,tSelectionsElement,tOldSelectionsText):
                return
        else: #データがある場合
            if self.TaskExistData(self,tSelectionsElement,tOldSelectionsText):
                return

        self.TaskRun()
        return

    def TaskNotExistData(self,aSelectionsElement,aOldSelectionsText) -> bool:
        aSelectionsElement[0].click()
        try: #終了判定
            _ = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            self.SaveData([aOldSelectionsText[0],aOldSelectionsText[1]],aOldSelectionsText[0])
            return True
        except: pass
        
        tSelectionsElement = util.GetSelectionsElement(self.driver)

        tCheck = []
        tCheck.append((tSelectionsElement[0].text == aOldSelectionsText[0]) or (tSelectionsElement[0].text == aOldSelectionsText[1]))
        tCheck.append((tSelectionsElement[1].text == aOldSelectionsText[1]) or (tSelectionsElement[0].text == aOldSelectionsText[1]))

        if tCheck[0] and tCheck[1]:#間違ってた時
            tSelectionsElement[1].click() if aOldSelectionsText[0] == tSelectionsElement[0].text else tSelectionsElement[0].click()
            self.SaveData([aOldSelectionsText[0],aOldSelectionsText[1]],aOldSelectionsText[1])
        else:#当たっていた時
            self.SaveData([aOldSelectionsText[0],aOldSelectionsText[1]],aOldSelectionsText[0])

        return False

    def TaskExistData(self,aSelectionsElement,aOldSelectionsText) -> bool:
        tEqualsList = []
        for i,j in [[0,0],[0,1],[1,0],[1,1]]:
            tEqualsList.append(self.data[self.columnName[i]] == aOldSelectionsText[j])
        tEquals = ((tEqualsList[0] | tEqualsList[1]) & (tEqualsList[2] | tEqualsList[3]))

        if self.data[tEquals][self.columnName[2]].iat[0] == aSelectionsElement[0].text:
            aSelectionsElement[0].click()
            self.data.loc[tEquals,self.columnName[2]] = aSelectionsElement[1].text
        else:
            aSelectionsElement[1].click()
            self.data.loc[tEquals,self.columnName[2]] = aSelectionsElement[0].text
        
        try: #終了判定
            _ = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return True
        except: pass

        tSelectionsElement = util.GetSelectionsElement(self.driver)

        tEqualsList = []
        for i,j in [[0,0],[0,1],[1,0],[1,1]]:
            tEqualsList.append(tSelectionsElement[i].text == aOldSelectionsText[j])

        # データがおかしい時
        if (tEqualsList[0] or tEqualsList[1]) and (tEqualsList[2] or tEqualsList[3]):
            self.data.to_csv(self.filePath, index = False, encoding='utf_8')

        return False
