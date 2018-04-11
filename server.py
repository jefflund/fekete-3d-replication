import flask
from flask import Flask, request
import subprocess
import xml.etree.ElementTree as ET


TRACKS = {'U1': ['TP', 'P1', 'TD', 'D2'],
          'U2': ['TD', 'D1', 'TP', 'P2'],
          'U3': ['TP', 'P2', 'TD', 'D1'],
          'U4': ['TD', 'D2', 'TP', 'P1']}
DATSETS = {'TP': 'homicide',
           'P1': 'carmortality',
           'P2': 'suicide',
           'TD': 'co2',
           'D1': 'army',
           'D2': 'hiv'}


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


def get_task(track):
    if 'train' in request.path:
        return 'TP', TRACKS[track].index('TP')
    return [(t,i) for i,t in enumerate(TRACKS[track]) if t in ('P1','P2')][0]


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
    nxt = 'trans/{}/0'.format(track)
    return flask.render_template('intro.html', next=nxt, track=track)


@app.route('/trans/<track>/<int:idx>')
def transition_page(track, idx):
    task = TRACKS[track][idx]
    return flask.render_template('transition.html', next='data', track=track, task=task, idx=idx)


@app.route('/physical/<track>', methods=['GET'])
@app.route('/physical/train/<track>', methods=['GET'])
def physical_data(track):
    task, idx = get_task(track)
    info = task_info(DATSETS[task])
    print('TRACK:', track)
    print('TASK:', task, DATSETS[task], idx)
    return flask.render_template('data.html', data=info)



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
