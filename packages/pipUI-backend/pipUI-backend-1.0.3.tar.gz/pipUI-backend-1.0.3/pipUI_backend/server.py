import json

from flask import Flask, g, request
from flask.json import jsonify

from pipUI_backend.autocomplete import Autocomplete
import pipUI_backend.startup as startup
import pipUI_backend.pypiscraper as pypiscraper

app = Flask(__name__)


@app.route("/package_info")
def package_info():
    return jsonify(pypiscraper.get_meta(request.args["pkg_name"]))


@app.route("/autocomplete")
def autocomplete():
    return jsonify(ac.search(request.args["word"]))


def main():
    startup.startup()
    ac = Autocomplete()
    app.run(host="localhost", port=5000)


if __name__ == "__main__":
    startup.startup()
    ac = Autocomplete()
    app.run(host="localhost", port=5000)

