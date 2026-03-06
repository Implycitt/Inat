import requests
from bs4 import BeautifulSoup

def getPage(url: str) -> Response | None:
    response: Response = requests.get(url)

    if (response.status_code == 200):
        return response
    return False

def parsePageAll(page: Response, elementType: str, className: str) -> list:
    soup: BeautifulSoup = BeautifulSoup(page.text, 'html.parser')

    return soup.find_all(elementType, class_=className)

def parsePageSingle(page: Response, elementType: str, className: str) -> Tag:
    soup: BeautifulSoup = BeautifulSoup(page.text, 'html.parser')

    return soup.find(elementType, class_=className)

def parseWithinPage(page: Response, elementType: str, className: str) -> Tag:
    return page.find(elementType)[className]
    
def crawl(url: str, visitedUrls=set()) -> None:
    if url in visitedUrls:
        return

    visitedUrls.add(url)

    page: Response = getPage(url)

    if not page:
        print("page returned bad")
        return

    quotes = parsePageAll(page, 'span', 'text')

    print("Number of quotes: ", len(quotes))
        
    nextPage = parsePageSingle(page, 'li', 'next')
    if nextPage:
        nextUrl = parseWithinPage(nextPage, 'a', 'href')
        crawl(url + nextUrl, visitedUrls)

if __name__ == "__main__":
    url = "http://quotes.toscrape.com"
    crawl(url, set())
    
