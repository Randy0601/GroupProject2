from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}

    ###############################################################################################################

    #Scraping Mars news title and description from https://mars.nasa.gov/news/?    page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())

    # results are returned as an iterable list

    news_listings = []
    results = soup.find_all('li', class_="slide") 

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            news_title = result.find('div', class_="image_and_description_container").find('div', class_="list_text").find('div', class_="content_title").find("a").text
            # Identify and return price of listing
            news_paragraph = result.find('div', class_="image_and_description_container").find('div', class_="list_text").find('div', class_="article_teaser_body").text

            # Print results only if title, price, and link are available
            if (news_title and news_paragraph):
    #             print('-------------')
    #             print(news_title)
    #             print(news_paragraph)
                news_listings.append({"news_title":news_title , "news_paragraph":news_paragraph})
        except AttributeError as e:
            print(e)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #mars_image_url = soup.find('div', class_="carousel_container").find('div', class_="carousel_items").find('article', class_="carousel_item").find('div', class_="default floating_text_area ms-layer").find('footer').find('a', class_="button fancybox").find('data-fancybox-href').text
    featured_image_url = "https://www.jpl.nasa.gov"

    featured_image_url += soup.find('div', class_="carousel_container").find('div', class_="carousel_items").find('article', class_="carousel_item").find('div', class_="default floating_text_area ms-layer").find('footer').find('a', class_="button fancybox")['data-fancybox-href']
    print(featured_image_url)

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.find('div', class_="ProfileTimeline").find('div', class_="stream-container").find('div', class_="stream").find('ol', class_="stream-items js-navigable-stream").find('li', class_="js-stream-item").find('div', class_ = "content").find('div', class_ = "js-tweet-text-container").find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    print(mars_weather)

    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    tables

    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Parameter','Value']
    mars_facts_df.head(10)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('Cerberus')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    cerberus_img_url = "https://astrogeology.usgs.gov"
    cerberus_img_url += soup.find('div', class_="wrapper").find('div', class_="container").find('div', class_="wide-image-wrapper").find('img', class_="wide-image")["src"]

    print(cerberus_img_url)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('Schiaparelli')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    schiaparelli_img_url = "https://astrogeology.usgs.gov"
    schiaparelli_img_url += soup.find('div', class_="wrapper").find('div', class_="container").find('div', class_="wide-image-wrapper").find('img', class_="wide-image")["src"]

    print(schiaparelli_img_url)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('Syrtis')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    syrtis_img_url = "https://astrogeology.usgs.gov"
    syrtis_img_url += soup.find('div', class_="wrapper").find('div', class_="container").find('div', class_="wide-image-wrapper").find('img', class_="wide-image")["src"]

    print(syrtis_img_url)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('Valles')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    valles_img_url = "https://astrogeology.usgs.gov"
    valles_img_url += soup.find('div', class_="wrapper").find('div', class_="container").find('div', class_="wide-image-wrapper").find('img', class_="wide-image")["src"]

    print(valles_img_url)

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": valles_img_url},
        {"title": "Cerberus Hemisphere", "img_url": cerberus_img_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_img_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_img_url},
    ]

    print(hemisphere_image_urls)

    ###############################################################################################################

    return listings
