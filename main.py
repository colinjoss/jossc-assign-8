from google.cloud import datastore
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def index():
    return "Please god"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)