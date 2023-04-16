import flask
app = flask.Flask(__name__)

from flask import Flask
from flask import request
from flask import json
from flask import render_template
from flask_moment import Moment
from sys import stderr
moment = Moment(app)


# solace comms setup
# for now a list of coords passed in
inputs = ("45.422195,-75.681503;45.423646,-75.682736;45.424803,-75.684954;45.426898,-75.686144;45.421772,-75.696036;45.419973,-75.695602;45.418594,-75.692945;45.409996,-75.699655;45.407108,-75.690199;45.402732,-75.693199;45.403115,-75.696691;45.422195,-75.681503")

@app.route("/")
def home():
    map_link = "https://www.google.com/maps/embed/v1/view?key=AIzaSyD4iE2xVSpkLLOXoyqT-RuPwURN3ddScAI&amp;center=-33.8569,151.2152&amp;zoom=18&amp;maptype=satellite"
    #map_generate(inputs)
    print(map_link, file=stderr)
    return render_template("home.html", map_link=map_link)

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
    url = "https://www.google.com/maps/dir/?api=1&origin=" + coords[0] + "&destination=" + coords[-1] + "travelmode=driving&waypoints="
    for x in range(1, (len(coords))):
        url = url + coords[x] + "%7C"
        x += 1
   
    return url




