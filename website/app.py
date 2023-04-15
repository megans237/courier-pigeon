# Entry point for the application.
# from . import app    # For application discovery by the 'flask' command.
# from . import views  # For import side-effects of setting up routes.

import flask
app = flask.Flask(__name__)

from flask import Flask
from flask import render_template
from flask_moment import Moment
moment = Moment(app)
# from . import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scan/")
def about():
    return render_template("about.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


def map_generate(inputs):

    coords = inputs.split(";")
    url = "https://www.google.com/maps/dir/?api=1&origin=" + coords[0] + "&destination=" + coords[-1] + "travelmode=driving&waypoints="
    for x in range(1, (len(coords))):
        url = url + coords[x] + "%7C"
        x += 1

    return url


