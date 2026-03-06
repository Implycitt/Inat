from selenium import webdriver
from selenium.webdriver.common.by import By

def connectUrl(url: str) -> bool:
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        return driver
    except:
        return False

def terminate(driver: webdriver) -> None:
    driver.quit()

def typeIntoElement(element, text):
    return element.send_keys(text)

def submit(driver):
    submitButton = driver.find_element(By.TAG_NAME, "commit")
    print(submitButton)

def getHeaderBody():
    with open("message.txt", 'r') as file:
        wholeFile = file.read()
        header, body = wholeFile.split('\n\n')
    return (header, body)

if __name__ == "__main__":
    print(getHeaderBody())
