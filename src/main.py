from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

import transition

def main():
    print("START")
    tDriver = webdriver.Remote(
        command_executor = os.environ["SELENIUM_URL"],
        options = webdriver.ChromeOptions()
    )
    print("Login START")
    transition.login(tDriver)

if __name__ == "__main__":
    main()