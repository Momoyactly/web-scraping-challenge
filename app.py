from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scraper

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
mongo = PyMongo(app, uri=f"{conn}/mars_app")


@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraper()
    mars.update({},mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
