import flask
from flask import Flask
import subprocess
# from .plot import plot_the_stupid_dataset_in_glorious_3d


app = Flask(__name__)
graph_thingy = None


@app.route('/')
def index():
    return flask.render_template('index.html', foo=42)


@app.route('/intro/<track>')
def intro(track):
    return flask.render_template('intro.html', next='data', track=track)


@app.route('/data')
def dataset():
    global graph_thingy
    graph_thingy = subprocess.Popen(["python3", "plot.py"])
    return flask.render_template('data_A.html')


@app.route('/ducks')
def foo():
    if graph_thingy:
        graph_thingy.kill()
    return 'Hello World'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
