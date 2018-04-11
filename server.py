import flask
from flask import Flask
import subprocess
import xml.etree.ElementTree as ET
# from .plot import plot_the_stupid_dataset_in_glorious_3d


def el_val(k,v):
    def _element_value(el):
        d = {'false': False, 'string': el.text, 'key': el.text, 'array': [e.text for e in el]}
        return d.get(el.tag, None)
    return _element_value(k), _element_value(v)


def parse_xml(ds):
    tree = ET.parse('tasks/{}.plist'.format(ds))
    comp = tree.getroot()[0][1][2]  # compare task xml
    i = iter(comp)
    data = [el_val(*e) for e in zip(i,i)]
    return data


app = Flask(__name__)
graph_thingy = None


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/intro/<track>')
def intro(track):
    return flask.render_template('intro.html', next='data', track=track)


@app.route('/data')
def dataset():
    # debug xml parsing
    _ds = 'army'
    _data = parse_xml(_ds)
    print(_ds+':', _data)
    # pull up the graph
    global graph_thingy
    graph_thingy = subprocess.Popen(["python3", "plot.py"])
    # return the page
    return flask.render_template('data_A.html')


@app.route('/ducks')
def foo():
    if graph_thingy:
        graph_thingy.kill()
    return 'Hello World'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
