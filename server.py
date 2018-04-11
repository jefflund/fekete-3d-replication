import flask
from flask import Flask
import subprocess
import xml.etree.ElementTree as ET


# Helper Functions
def el_val(k,v):
    def _element_value(el):
        d = {'false': False, 'string': el.text, 'key': el.text, 'array': [e.text for e in el]}
        return d.get(el.tag, None)
    return _element_value(k), _element_value(v)


def task_info(ds):
    tree = ET.parse('tasks/{}.plist'.format(ds))
    comp = tree.getroot()[0][1][2]  # compare task xml
    i = iter(comp)
    data = [el_val(*e) for e in zip(i,i)]
    return dict(data)


# create server
app = Flask(__name__)
graph_thingy = None


# server routing
@app.route('/')
def index():
    if graph_thingy:
        graph_thingy.kill()
    return flask.render_template('index.html')


@app.route('/intro/<track>')
def intro(track):
    return flask.render_template('intro.html', next='data', track=track)


@app.route('/data')
def digital_data():
    # debug xml parsing
    _ds = 'food'
    info = task_info(_ds)
    print(_ds+':', info)
    # pull up the graph
    global graph_thingy
    graph_thingy = subprocess.Popen(["python3", "plot.py", _ds])
    # return the page
    return flask.render_template('data.html', data=info)


@app.route('/ducks')
def foo():
    if graph_thingy:
        graph_thingy.kill()
    return 'Hello World'


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0')
