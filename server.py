import flask
from flask import Flask
import subprocess
# from .plot import plot_the_stupid_dataset_in_glorious_3d


app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', foo=42)


@app.route('/data')
def dataset():
    subprocess.Popen(["python3", "plot.py"])
    return flask.render_template('data_A.html')


if __name__ == '__main__':
    app.run()
