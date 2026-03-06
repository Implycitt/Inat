from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

def connectUrl(driver: webdriver, url: str) -> bool:
    try:
        driver.get(url)
        return driver
    except:
        return False

def terminate(driver: webdriver) -> None:
    driver.quit()

def typeIntoElement(element, text):
    return element.send_keys(text)

def pressButton(buttonElement):
    buttonElement.click()

def getHeaderBody():
    with open("./in/message.txt", 'r') as file:
        wholeFile = file.read()
        header, body = map(str, wholeFile.split('\n\n'))
    return (header, body.strip('\n'))

def login(driver: webdriver) -> None:
    email, password = map(str, (os.getenv('EMAIL'), os.getenv('PASSWORD')))
    connectUrl(driver, "https://www.inaturalist.org/login")

    emailField = driver.find_element(By.ID, "user_email")
    passwordField = driver.find_element(By.ID, "user_password")

    typeIntoElement(emailField, email)
    typeIntoElement(passwordField, password)

    pressButton(driver.find_element(By.NAME, "commit"))

def sendMessage(driver: webdriver) -> None:
    header, body = map(str, getHeaderBody())

    headerField = driver.find_element(By.ID, "message_subject")
    bodyField = driver.find_element(By.ID, "message_body")

    typeIntoElement(headerField, header)
    typeIntoElement(bodyField, body)

    pressButton(driver.find_element(By.NAME, "commit"))

def Messenger() -> None:
    load_dotenv(dotenv_path="./in/.env")
    baseUrl = "https://www.inaturalist.org/messages/new?to="

    with open("./out/users.txt", 'r') as file:
        users: tuple() = tuple(line.strip('\n'), for line in file)

    driver = webdriver.Chrome()
    login(driver)

    for user in users:
        messageUrl = baseUrl + user
        connectUrl(driver, messageUrl)
        sendMessage(driver)

