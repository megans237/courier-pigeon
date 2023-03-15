from flask import Flask
import flask
import json
from flask_cors import CORS

app = Flask(__name__)


@app.route("/")
def hello():
    return "lets do some fuckin web dev"

@app.route('/users', methods=["GET"])
def users():
    print("users endpoint reached...")
    with open("users.json", "r") as f:
        data = json.load(f)
        data.append({
            "username": "user4",
            "pets": ["hamster"]
        })
        return flask.jsonify(data)

if __name__ == "__main__":
    app.run("localhost", 4002)

CORS(app)

FLASK_APP=app.py

