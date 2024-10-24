from . import socketio
@socketio.on("gamepad on_pressed")
def map_and_send_buttons(data):
    print(data)