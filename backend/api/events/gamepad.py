from . import socketio, mqttc


@socketio.on("gamepad buttons")
def map_and_send_buttons(command):
  print(command)
  mqttc.publish("Motion Commands", command, qos=1) # to localhost:1883