from flask_socketio import emit
from .. import socketio

@socketio.on("connect")
def handle_connect():
    print("A client has connected")
    emit("connected", {"message": "You are connected to the WebSocket server!"})

@socketio.on("disconnect")
def handle_disconnect():
    print("A client has disconnected")

from .boxes import push_new_box
from .gamepad import *