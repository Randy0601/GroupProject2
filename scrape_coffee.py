# coding: utf-8
#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup



# Defining scrape & dictionary
def scrape():

    #Site Navigation
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=True)
    final_data = {}

## Coffee News

    def coffee_News():
        news_url = "http://www.ncausa.org/About-Coffee/What-is-Coffee"
    
        browser.visit(news_url)
        html = browser.html
    
        soup = BeautifulSoup(html, "html.parser")
        news_title = soup.find("h1").text
        #article = soup.findAll( "p", class_= "p1")
        #news_p = article.find( "p", class_= "p1")
        final_data["title"] = news_title
        # final_data["coffee_News"] = article[0] 
        final_data["coffee_News"] = "".join([p.text for p in soup.find_all("p", class_= "p1")])
    
    coffee_News()
    

    browser.quit()
    return final_data

