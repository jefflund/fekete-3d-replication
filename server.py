import flask
from flask import Flask, request
import subprocess
import datetime
import xml.etree.ElementTree as ET


TRACKS = {'U1': ['TP', 'P1', 'TD', 'D2'],
          'U2': ['TD', 'D1', 'TP', 'P2'],
          'U3': ['TP', 'P2', 'TD', 'D1'],
          'U4': ['TD', 'D2', 'TP', 'P1']}
DATSETS = {'TP': 'homicide',
           'P1': 'carmortality',
           'P2': 'suicide',
           'TD': 'externaldebt',
           'D1': 'army',
           'D2': 'hiv'}
TRANS_ROUTE = {'TP': 'physical/train/',
               'P1': 'physical/',
               'P2': 'physical/',
               'TD': 'digital/train/',
               'D1': 'digital/',
               'D2': 'digital/'}


# create server
app = Flask(__name__)
graph_thingy = None
start_time = None


# Helper Functions
def el_val(k,v):
    def _element_value(el):
        d = {'false': False, 'string': el.text, 'key': el.text, 'array': [e.text for e in el]}
        return d.get(el.tag, None)
    return _element_value(k), _element_value(v)


def task_info(ds):
    """parse the compare task info from XML for the specified dataset"""
    tree = ET.parse('tasks/{}.plist'.format(ds))
    comp = tree.getroot()[0][1][2]  # compare task xml
    i = iter(comp)
    data = [el_val(*e) for e in zip(i,i)]
    return dict(data)


def get_task(track):
    if 'train' in request.path:
        if 'physical' in request.path:
            return 'TP', TRACKS[track].index('TP')
        return 'TD', TRACKS[track].index('TD')
    else:
        if 'physical' in request.path:
            return [(t,i) for i,t in enumerate(TRACKS[track]) if t in ('P1','P2')][0]
        return [(t, i) for i, t in enumerate(TRACKS[track]) if t in ('D1', 'D2')][0]


def data_nxt(track, idx):
    if idx >= 3:
        return 'finish/{}/{}'.format(track, idx+1)
    return 'trans/{}/{}'.format(track, idx+1)


def clean_up():
    if graph_thingy:
        graph_thingy.kill()


def log_time(track, idx):
    global start_time
    if start_time:
        end_time = datetime.datetime.now()
        diff = (end_time - start_time).total_seconds()
        with open('time_logs.txt', 'a+') as f:
            f.write(_csv(track, idx, start_time, end_time, diff, is_training(track, idx)))
        start_time = None


def _csv(*items):
    return ''.join(str(i)+', ' for i in items)+'\r\n'


def is_training(track, idx):
    return TRACKS[track][idx] == 'TP' or TRACKS[track][idx] == 'TD'


# server routing
@app.route('/')
def index():
    clean_up()
    return flask.render_template('index.html')


@app.route('/intro/<track>')
@app.route('/intro/<track>/<int:intro_idx>')
def intro(track, intro_idx=0):
    clean_up()
    if intro_idx == 0:
        return flask.render_template('intro-A.html', track=track)
    elif intro_idx == 1:
        return flask.render_template('intro-B.html', track=track)
    elif intro_idx == 2:
        return flask.render_template('intro-C.html', track=track)
    elif intro_idx == 3:
        global graph_thingy
        graph_thingy = subprocess.Popen(["python3", "plot.py", DATSETS['TD']])
        return flask.render_template('play-with-it-digital.html', track=track)
    elif intro_idx == 4:
        return flask.render_template('play-with-it-physical.html', track=track)


@app.route('/trans/<track>/<int:idx>')
def transition_page(track, idx):
    clean_up()
    log_time(track, idx)
    task = TRACKS[track][idx]
    info = task_info(DATSETS[task])
    nxt = TRANS_ROUTE[task] + track
    return flask.render_template('transition.html', next=nxt, data=info)


@app.route('/physical/<track>', methods=['GET'])
@app.route('/physical/train/<track>', methods=['GET'])
def physical_data(track):
    clean_up()
    task, idx = get_task(track)
    info = task_info(DATSETS[task])
    nxt = data_nxt(track, idx)
    global start_time
    start_time = datetime.datetime.now()
    return flask.render_template('data.html', data=info, next=nxt)


@app.route('/digital/<track>', methods=['GET'])
@app.route('/digital/train/<track>', methods=['GET'])
def digital_data(track):
    clean_up()
    task, idx = get_task(track)
    info = task_info(DATSETS[task])
    # pull up the graph
    global graph_thingy
    graph_thingy = subprocess.Popen(["python3", "plot.py", DATSETS[task]])
    # return the page
    nxt = data_nxt(track, idx)
    global start_time
    start_time = datetime.datetime.now()
    return flask.render_template('data.html', data=info, next=nxt)


@app.route('/finish/<track>/<int:idx>')
def finish(track, idx):
    clean_up()
    log_time(track, idx)
    return flask.render_template('finish.html')


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0')
