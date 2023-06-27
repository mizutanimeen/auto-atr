from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

from . import util

TRANSLATION_COLUMN_NAME=["english","japanese"]

class TaskManager():
    driver: webdriver.Remote
    wait: WebDriverWait
    filePath: str
    data: pd.DataFrame
    columnName: list[str] #[questionColumnName,selectionColumnName]

    def __init__(self,aDriver: webdriver.Remote,aWait: WebDriverWait,aBaseDataPath: str,aColumnName: list[str]) -> None:
        if not len(aColumnName) == 2:
            raise ValueError("TaskManagerに渡されたColumnNameの数が２つではありません: ",aColumnName)
        self.driver = aDriver
        self.wait = aWait
        self.filePath = aBaseDataPath + "je.csv"
        self.columnName = aColumnName

        self.TranslationFileIfNotExistCreate()
        self.TranslationDataOrganization()
        return 
    
    def TranslationFileIfNotExistCreate(self) -> None:
        if not os.path.isfile(self.filePath):   
            with open(self.filePath, "w") as f:   # ファイルを作成
                f.write(f"{TRANSLATION_COLUMN_NAME[0]},{TRANSLATION_COLUMN_NAME[1]}\n")#直書きしてるのよくない
        return

    #空白の要素や英語、日本語以外のカラム削除、重複データ削除
    def TranslationDataOrganization(self) -> None: 
        tData = pd.read_csv(self.filePath, sep=",", encoding='utf_8')
        tData = tData.loc[:,TRANSLATION_COLUMN_NAME]
        tData = tData.dropna(how='any',axis=0)
        tData = tData.drop_duplicates(subset=f"{TRANSLATION_COLUMN_NAME[0]}",keep=False)
        tData = tData.drop_duplicates(subset=f"{TRANSLATION_COLUMN_NAME[1]}",keep=False)
        tData.to_csv(self.filePath, sep=",", index = False, encoding='utf_8')
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

    def Run(self) -> None:
        try: #終了判定
            _ = WebDriverWait(driver=self.driver, timeout=5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return
        except: pass

        self.ReadData()
        tQuestionElement = self.wait.until( EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')) )
        tSelectionsElement = util.GetSelectionElements(aWait=self.wait)
        
        #見ずらいから外に出しとく
        tQuestionData = self.data[self.columnName[0]]
        tEquals = (tQuestionData == tQuestionElement.text)

        if self.data[tEquals].empty: #データがない場合
            if self.TaskNotExistData(tQuestionElement,tSelectionsElement):
                return
        else: #データがある場合
            if self.TaskExistData(tQuestionElement,tSelectionsElement):
                return

        self.Run() #再帰
        return 

    def TaskNotExistData(self,aQuestionElement,aSelectionsElement) -> bool:
        tOldQuestionText = aQuestionElement.text
        tOldSelectionsText = [aSelectionsElement[0].text,aSelectionsElement[1].text]
        aSelectionsElement[0].click()
        try: #終了判定
            _ = WebDriverWait(driver=self.driver, timeout=5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            self.SaveData(tOldQuestionText,tOldSelectionsText[0])
            return True
        except: pass
        
        tQuestionElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')))
        tSelectionsElement = util.GetSelectionElements(aWait=self.wait)
        
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
            _ = WebDriverWait(driver=self.driver, timeout=5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
            return True
        except: pass

        tQuestionElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination')))
        if tQuestionElement.text == tOldQuestionText: # 間違っていた時
            self.data.to_csv(self.filePath, index = False, encoding='utf_8')# 間違いが確定したためファイルに保存する

        return False
