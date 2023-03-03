from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import util

#みずらい変数名なんとかしないと
def TaskOneTwoNotExistData(aDriver,aData,aDataPath,aQuestionElement,aSelectionsElement,aColumnName):
    tOldQuestionText = aQuestionElement.text
    tOldSelectionsText = [aSelectionsElement[0].text,aSelectionsElement[1].text]
    aSelectionsElement[0].click()
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        tNewData = pd.DataFrame(
            data={aColumnName[0]: [tOldQuestionText], 
                aColumnName[1]: [tOldSelectionsText[0]]}
        )
        aData = pd.concat([aData,tNewData],ignore_index=True)
        aData.to_csv(aDataPath, index = False, encoding='utf_8')
        return True
    except: pass
    
    tQuestionElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
    )
    tSelectionsElement = util.GetSelectionsElement(aDriver)
    
    #間違っていた場合
    if tOldQuestionText == tQuestionElement.text: 
        tSelectionsElement[1].click() if tOldSelectionsText[0] == tSelectionsElement[0].text else tSelectionsElement[0].click()
        tNewData = pd.DataFrame(
            data={aColumnName[0]: [tOldQuestionText], 
                aColumnName[1]: [tOldSelectionsText[1]]}
        )
   
    #合っていた場合
    else:
        tNewData = pd.DataFrame(
            data={aColumnName[0]: [tOldQuestionText], 
                aColumnName[1]: [tOldSelectionsText[0]]}
        )
        
    aData = pd.concat([aData,tNewData],ignore_index=True)
    aData.to_csv(aDataPath, index = False, encoding='utf_8')
    return False

def TaskOneTwoExistData(aDriver,aData,aDataPath,aQuestionElement,aSelectionsElement,aColumnName):
    tOldQuestionText = aQuestionElement.text

    if aData[aData[aColumnName[0]] == aQuestionElement.text][aColumnName[1]].iat[0] == aSelectionsElement[0].text:
        aSelectionsElement[0].click()
        aData.loc[aData[aColumnName[0]] == tOldQuestionText,aColumnName[1]] = aSelectionsElement[1].text
    elif aData[aData[aColumnName[0]] == aQuestionElement.text][aColumnName[1]].iat[0] == aSelectionsElement[1].text:
        aSelectionsElement[1].click()
        aData.loc[aData[aColumnName[0]] == tOldQuestionText,aColumnName[1]] = aSelectionsElement[0].text
   
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        return True
    except: pass
    tQuestionElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
    )
    # データがおかしい時
    if tQuestionElement.text == tOldQuestionText:
        aData.to_csv(aDataPath, index = False, encoding='utf_8')
    return False
                

def TaskThreeNotExistData(aDriver,aData,aDataPath,aSelectionsElement,aOldSelectionsText):
    aSelectionsElement[0].click()
    try: #終了判定
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        tNewData = pd.DataFrame(
            data={"one": [aOldSelectionsText[0]], 
                "two":  [aOldSelectionsText[1]],
                "ans": [aOldSelectionsText[0]]}
        )
        aData = pd.concat([aData,tNewData],ignore_index=True)
        aData.to_csv(aDataPath, index = False, encoding='utf_8')
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
    aData.to_csv(aDataPath, index = False, encoding='utf_8')
    return False

#処理合ってるかわからん、条件が冗長でわかりずらい、なんとかする
def TaskThreeExistData(aDriver,aData,aDataPath,aSelectionsElement,aOldSelectionsText):
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
        aData.to_csv(aDataPath, index = False, encoding='utf_8')
    return False

