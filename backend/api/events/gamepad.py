from . import socketio
import paho.mqtt.publish as publish
@socketio.on("gamepad buttons")
def map_and_send_buttons(data):
    # ... manipulate data
    publish.single("navigation/send_controls", data) # to localhost:1883