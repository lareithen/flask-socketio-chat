from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', user=request.remote_addr)

@socketio.on('message')
def handler(data):
    print(data)
    emit(
        'response',
        {'data': f"{dict(data)['user']}: {dict(data)['data']}"}, 
        broadcast=True
    )

@socketio.event
def connect():
    emit(
        'response', 
        {'data': f'{request.remote_addr} connected.'},
        broadcast=True
    )

@socketio.event
def disconnect():
    emit(
        'response', 
        {'data': f'{request.remote_addr} disconnected.'}, 
        broadcast=True
    )

if __name__ == '__main__':
    socketio.run(app)