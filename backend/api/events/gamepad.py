from . import socketio
import json

#import paho.mqtt.publish as publish
@socketio.on("gamepad buttons")
def map_and_send_buttons(command, commandValue):
  print(command)
  print(commandValue)
    # ... manipulate data
#    publish.single("navigation/send_controls", data) # to localhost:1883