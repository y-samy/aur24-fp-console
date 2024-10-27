from . import socketio
import json
import paho.mqtt.publish as publish

@socketio.on("gamepad buttons")
def map_and_send_buttons(command):
  print(command)
  publish.single("Motion Commands", command) # to localhost:1883