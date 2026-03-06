from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

class Driver:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def connectUrl(self, url: str) -> bool:
        try:
            self.driver.get(url)
            return True
        except:
            return False

    def terminate(self) -> None:
        self.driver.quit()

    def typeIntoElement(self, element, text):
        return element.send_keys(text)

    def pressButton(self, buttonElement):
        buttonElement.click()
