from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import util

#みずらい変数名なんとかしないと
def TaskOneNotExistData(aDriver,aData,aDataPath,aQuestionElement,aSelectionElements,aColumnName):
    tOldQuestionText = aQuestionElement.text
    tQuestionElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
    )
    tOldSelectionsText = [aSelectionElements[0].text,aSelectionElements[1].text]
    tSelectionsElement = util.GetSelectionsElement(aDriver)
    
    #間違っていた場合
    if tOldQuestionText == tQuestionElement.text: 
        tSelectionsElement[1].click() if tOldSelectionsText[0] == tSelectionsElement[0].text else tSelectionsElement[0].click()
        aData = aData.append({aColumnName[0]:tOldQuestionText,aColumnName[1]:tOldSelectionsText[1]}, ignore_index=True)
   
    #合っていた場合
    else:
        aData = aData.append({aColumnName[0]:tOldQuestionText,aColumnName[1]:tOldSelectionsText[0]}, ignore_index=True)
    
    aData.to_csv(aDataPath, index = False, encoding='utf_8')
    return

#間違って記録された時の対処必要だわ
def TaskOneExistData(aDriver,aData,aDataPath,aQuestionElement,aSelectionElements,aColumnName):
    tOldQuestionText = aQuestionElement.text

    if aData[aData[aColumnName[0]] == aQuestionElement.text].iat[0,1] == aSelectionElements[0].text:
        aSelectionElements[0].click()
        aData.loc[aData[aColumnName[0]] == tOldQuestionText,aColumnName[1]] = aSelectionElements[1].text
    elif aData[aData[aColumnName[0]] == aQuestionElement.text].iat[0,1] == aSelectionElements[1].text:
        aSelectionElements[1].click()
        aData.loc[aData[aColumnName[0]] == tOldQuestionText,aColumnName[1]] = aSelectionElements[0].text
   
    try: #終了判定 #確定で時間かかるの微妙
        _ = WebDriverWait(aDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"View-ResultNavi")))
        return 
    except: pass
    tQuestionElement = WebDriverWait(aDriver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME,'View-TrialExamination'))
    )
    # データがおかしい時
    if tQuestionElement.text == tOldQuestionText:
        aData.to_csv(aDataPath, index = False, encoding='utf_8')
                