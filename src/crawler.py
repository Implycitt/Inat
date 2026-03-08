from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from driver import Driver

import messenger

def findNext() -> set:
    userLinks = primaryDriver.find_elements(By.CLASS_NAME, "userlink")
    userLinks += primaryDriver.find_elements(By.CLASS_NAME, "large")
    userLinks = prettyUserList(userLinks)
    return createUserLinks(userLinks)

def findWithin() -> set:
    possibleFriends = primaryDriver.find_elements(By.TAG_NAME, "a").get_attribute("href")
    friends = set([i.text for i in possibleFriends if i[1:6] == "people"])
    friends = createUserLinks(friends)
    return friends

def prettyUserList(userLinks: set) -> set:
    outLinks = set()
    for element in userLinks:
        outLinks.add(element.text)
    return outLinks

def createUserLinks(userLinks: set) -> set:
    outURLs = set()
    base = "https://inaturalist.org/people/"
    for user in userLinks:
        outURLs.add(base+str(user))
    return outURLs


def crawl(unvisistedUrls: set) -> None:
    while (len(unvisitedUrls) != 0):
       findNext() 

if __name__ == "__main__":
    unvisitedUrls = set()
    webDriver = Driver()
    primaryDriver = webDriver.driver
    load_dotenv(dotenv_path="./in/.env")
    webDriver.connectUrl("https://inaturalist.org/people")
    messenger.login(webDriver)
    firstRound = findNext()

    input()
