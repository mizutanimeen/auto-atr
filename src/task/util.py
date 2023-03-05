from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def GetSelectionsElement(aWait: WebDriverWait):# -> any,any
    tSelectionElementOne = aWait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[1]/div[1]')))
    tSelectionElementTwo = aWait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/div/div[5]/div/div[2]/div[1]')))
    return [tSelectionElementOne,tSelectionElementTwo]
