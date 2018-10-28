from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_coffee

app = Flask(__name__)


app.config["MONGO_DBNAME"] = "coffee"
app.config["MONGO_URI"] = "mongodb://localhost:27017/coffee"

mongo = PyMongo(app)

@app.route("/")
def index():
    final_data = mongo.db.final_data.find_one()
    return render_template("index.html", final_data = final_data)

@app.route("/scrape")
def scrape():
    final_data = mongo.db.final_data
    final_data_coffee = scrape_coffee.scrape()
    final_data.update({}, final_data_coffee, upsert=True)
    # return redirect("http://localhost:5000/", code=302)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)