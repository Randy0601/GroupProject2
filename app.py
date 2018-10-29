import requests
import json
import scrape_coffee
import scrape_coffee_news
from twitter import *
from flask import Flask, jsonify, render_template, request, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/coffee"
mongo = PyMongo(app)

@app.route("/")
def index():
    final_data = mongo.db.final_data.find_one()
    if (final_data is None):
        scrape()
        final_data = mongo.db.final_data.find_one()
    return render_template("index.html", final_data = final_data)

@app.route("/index.html")
def indexpage():
    final_data = mongo.db.final_data.find_one()
    if (final_data is None):
        scrape()
        final_data = mongo.db.final_data.find_one()
    return render_template("index.html", final_data = final_data)

@app.route("/tweets.html")
def tweets():
    return render_template('tweets.html')

@app.route("/findcoffee.html")
def findCoffee():
    return render_template('findcoffee.html')

@app.route("/stats.html")
def stats():
    return render_template('stats.html')

@app.route("/trends.html")
def ustrends():
    return render_template('trends.html')

@app.route("/funfacts.html")
def funfacts():
    return render_template('funfacts.html')

@app.route("/news.html")
def news():
    listings = mongo.db.listings.find_one()
    if (listings is None):
        scrapeCoffeeNews()
        listings = mongo.db.listings.find_one()
    return render_template("news.html", listings=listings)


yelp_header = {'Content-Type': 'application/json','Authorization': 'Bearer FsbmD61belea3BdBgk7oUqIrd2Vva_RMWTR4YPlucKLIVDGAM7qgNbZahcnP9PR40d2-5mnSgkB9LRyXflZJRiDf1y5UGxHAtL7JjT44JwsLGpIYXaVkgJNuWWHLW3Yx'}
twitter_header = {'Authorization': 'Bearer 1024005802112286720-tewTubcOAEiWSruFzKspp8oOrkKTeD'}

twitter_token = "1024005802112286720-tewTubcOAEiWSruFzKspp8oOrkKTeD"
twitter_token_secret = "WAQiyuFxAHuFBxhnKZ5pUABrSKtNLe6EMn9JHlVpmzRkR"
twitter_consumer_key = "f8mvOcjx2FW6fmLmrt4ZenOaQ"
twitter_consumer_secret = "TyKX2k9YIvlQjXiVvHINGecWpXqVVNodkmmOjuHlW1WrlBZayX"

t = Twitter(
    auth=OAuth(twitter_token, twitter_token_secret, twitter_consumer_key, twitter_consumer_secret))

@app.route('/getYelpReview/<searchLocation>/<sortby>')
def getYelpReview(searchLocation,sortby):
    print("Search Location:" + searchLocation)
    print("Sortby value:" + sortby)
    yelp_url = "https://api.yelp.com/v3/businesses/search?term=coffee&limit=20&location="
    yelp_url += searchLocation
    yelp_url += "&sort_by="
    yelp_url += sortby
    # url += api_key
    print("Url :" + yelp_url)
    response = requests.get(yelp_url,headers=yelp_header ).json()
    # Print the fact stored within the response
    print(response)
    return jsonify(response)

@app.route('/getCoffeeTweets/<searchKeyword>')
def getCoffeeTweets(searchKeyword):
    print("Inside getCoffeeTweets")
    # Search for the latest tweets about #pycon
    response = t.search.tweets(q=searchKeyword,lang="en",tweet_mode='extended')
    print(response)
    return jsonify(response)

@app.route('/scrapeCoffeeNews')
def scrapeCoffeeNews():
    listings = mongo.db.listings
    listings_data = scrape_coffee_news.scrape()
    listings.update({}, listings_data, upsert=True)
    return news()

@app.route('/scrape')
def scrape():
    listings = mongo.db.final_data
    listings_data = scrape_coffee.scrape()
    listings.update({}, listings_data, upsert=True)
    return indexpage()

if __name__ == "__main__":
    app.run(debug=True)
