from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os, sys
from dotenv import load_dotenv

class Driver:
    def __init__(self):
        if (sys.platform.startswith("linux")):
            self.driver = self.linuxWebdriver()
        self.driver = webdriver.Chrome()

    def linuxWebdriver(self) -> webdriver:
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
