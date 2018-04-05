import flask
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', foo=42)


@app.route('/data')
def dataset():
    return flask.render_template('data_A.html')
