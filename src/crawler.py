from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from driver import Driver

import messenger

unvisitedUrls = set()
webDriver = Driver()
primaryDriver = webDriver.driver

def findNext() -> set:
    userLinks = primaryDriver.find_elements(By.CLASS_NAME, "userlink")
    userLinks += primaryDriver.find_elements(By.CLASS_NAME, "large")
    userLinks = prettyUserList(userLinks)
    print(userLinks)

def prettyUserList(userLinks: set) -> set:
    outLinks = set()
    for element in userLinks:
        outLinks.add(element.text)
    return outLinks

def crawl(unvisistedUrls: set) -> None:
    pass

if __name__ == "__main__":
    load_dotenv(dotenv_path="./in/.env")
    webDriver.connectUrl("https://inaturalist.org/people")
    messenger.login(webDriver)
    findNext()
    input()
