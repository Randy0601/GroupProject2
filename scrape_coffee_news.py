from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    ###############################################################################################################

    url = "https://dailycoffeenews.com/latest-news"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # results are returned as an iterable list
    listings = {}
    news_listings = []
    title_results = soup.find_all('article')

    # Loop through returned results  which contains list of news items
    for result in title_results:
        # Error handling
        try:
            # Identify and return news title
            news_title = result.find('h2').find('a').text
            # Identify and return news paragraph
            news_link = result.find('h2').find('a')["href"]

            # Print results only if title, price, and link are available
            if (news_title and news_link):
                print('-------------')
                print(news_title)
                print(news_link)
                news_listings.append({"news_title":news_title , "news_link":news_link})
        except AttributeError as e:
            print(e)

    listings["news_headlines"] = news_listings

    return listings

