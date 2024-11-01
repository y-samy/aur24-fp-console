from flask_socketio import emit
from .. import socketio, mqttc
from .localisation import handleReadings

@socketio.on("connect")
def handle_connect():
    print("A client has connected")
    emit("connected", {"message": "You are connected to the WebSocket server!"})

@socketio.on("disconnect")
def handle_disconnect():
    print("A client has disconnected")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to mqtt broker {reason_code}")
    client.subscribe("Encoders")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "Encoders":
        handleReadings(str(msg.payload, "utf-8").split(","))


mqttc.on_connect = on_connect
mqttc.on_message = on_message


from .boxes import push_new_box
from .gamepad import *


