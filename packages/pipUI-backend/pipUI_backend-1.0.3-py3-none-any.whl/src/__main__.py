import json

from flask import Flask, g, request

from autocomplete import Autocomplete
import startup

app = Flask(__name__)


@app.route("/autocomplete")
def autocomplete():
    return json.dumps(ac.search(request.form["word"]))


def main():
    startup.startup()
    ac = Autocomplete()
    app.run(host="localhost", port=10011)

