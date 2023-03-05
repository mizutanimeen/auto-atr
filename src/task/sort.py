from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TaskManager():
    driver: webdriver.Remote
    wait: WebDriverWait

    def __init__(self,aDriver: webdriver.Remote,aWait: WebDriverWait) -> None:
        self.driver = aDriver
        self.wait = aWait
        return 

    def TaskRun(self) -> None:
        try:
            tCards = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'View-DragDropCard-Word')))
        except:
            return
        for i in range(len(tCards)):
            tCards[i].click()
            time.sleep(0.5)
        tBtn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div')))
        if tBtn.text == "採点する":
            tBtn.click()
            time.sleep(3)

        self.TaskRun()
        return