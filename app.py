from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from tinydb import TinyDB
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
db = TinyDB('db.json')
app = Flask(__name__)
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
    messages = db.all()
    return render_template('index.html', user=request.remote_addr, messages=messages)

@socketio.on('message')
def handler(data):
    data = {'data': f"{dict(data)['user']}: {dict(data)['data']}"}
    print(data)
    db.insert(data)
    emit(
        'response',
        data, 
        broadcast=True
    )

@socketio.event
def connect():
    data = {'data': f'{request.remote_addr} connected.'}
    db.insert(data)
    emit(
        'response', 
        data,
        broadcast=True
    )

@socketio.event
def disconnect():
    data = {'data': f'{request.remote_addr} disconnected.'}
    db.insert(data)
    emit(
        'response', 
        {'data': data}, 
        broadcast=True
    )

if __name__ == '__main__':
    socketio.run(app)
