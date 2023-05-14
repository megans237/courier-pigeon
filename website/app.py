import flask
app = flask.Flask(__name__)

from flask import Flask
from flask import request
from flask import json
from flask import render_template
from flask_moment import Moment
from sys import stderr
moment = Moment(app)

import os
from dotenv import load_dotenv
load_dotenv()

MAPS_KEY = os.getenv('MAPS_API_KEY')

print("If Error: Could not locate a Flask application, please enter <cd website>")

# import Common.solace_client
# import Common.common_datatypes as pigeon_dtype
# import Supervisor.router as router

# import dotenv
# import os
# import certifi
# import paho.mqtt.client as mqtt

# api key 

# solace comms setup

# for now a list of coords passed in
inputs = ("45.422195,-75.681503;45.423646,-75.682736;45.424803,-75.684954;45.426898,-75.686144;45.421772,-75.696036;45.419973,-75.695602;45.418594,-75.692945;45.409996,-75.699655;45.407108,-75.690199;45.402732,-75.693199;45.403115,-75.696691;45.422195,-75.681503")

@app.route("/")
def home():
    origin = (map_generate(inputs)[0])
    waypoints = (map_generate(inputs)[1])
    destination = (map_generate(inputs)[2])

    print(map, file=stderr)
    return render_template("home.html", MAPS_KEY=MAPS_KEY, origin=origin, waypoints=waypoints, destination=destination)


@app.route("/scan/")
def about():
    return render_template("about.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/test", methods=["POST"])
def test():
    output = request.get_json()
    print(output, file=stderr)
    print(type(output), file=stderr)
    result = json.loads(output) # converts json output to a python dict
    print(result) 
    print(type(result))
    return result


def map_generate(inputs):

    coords = inputs.split(";")
    print(len(coords))
    print(coords[0])

    origin = str(coords[0])

    waypoints = ""
    for x in range(1, (len(coords))-2):
        waypoints = waypoints + coords[x] + "|" 
        x += 1
        print(waypoints)
        print(x)
        if x == len(coords)-2:
            waypoints = waypoints[:-1]
   
    destination = coords[len(coords)-2]

    new_map_URL = "https://www.google.com/maps/embed/v1/directions?key=" + MAPS_KEY + "&origin=" + origin + "&waypoints=" + waypoints + "&destination=" + destination + "&zoom=14"
    print(new_map_URL)

    return origin, waypoints, destination


