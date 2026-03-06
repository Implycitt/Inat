from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

from driver import Driver

def getHeaderBody():
    with open("./in/message.txt", 'r') as file:
        wholeFile = file.read()
        header, body = map(str, wholeFile.split('\n\n'))
    return (header, body.strip('\n'))

def login(webDriver: Driver) -> None:
    email, password = map(str, (os.getenv('EMAIL'), os.getenv('PASSWORD')))
    primaryDriver = webDriver.driver
    webDriver.connectUrl("https://Inaturalist.org/login")

    emailField = primaryDriver.find_element(By.ID, "user_email")
    passwordField = primaryDriver.find_element(By.ID, "user_password")

    webDriver.typeIntoElement(emailField, email)
    webDriver.typeIntoElement(passwordField, password)

    webDriver.pressButton(primaryDriver.find_element(By.NAME, "commit"))

def sendMessage(webDriver: Driver) -> None:
    header, body = map(str, getHeaderBody())
    primaryDriver = webDriver.driver

    headerField = primaryDriver.find_element(By.ID, "message_subject")
    bodyField = primaryDriver.find_element(By.ID, "message_body")

    webDriver.typeIntoElement(headerField, header)
    webDriver.typeIntoElement(bodyField, body)

    webDriver.pressButton(primaryDriver.find_element(By.NAME, "commit"))

def Messenger() -> None:
    load_dotenv(dotenv_path="./in/.env")
    baseUrl = "https://www.inaturalist.org/messages/new?to="

    with open("./out/users.txt", 'r') as file:
        users: tuple() = tuple(line.strip('\n') for line in file)

    webDriver = Driver()
    login(webDriver)

    for user in users:
        messageUrl = baseUrl + user
        connectUrl(webDriver, messageUrl)
        sendMessage(webDriver)

