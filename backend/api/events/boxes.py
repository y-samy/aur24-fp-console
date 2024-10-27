from . import socketio
def push_new_box(coords):
    print(f"Sending box: {coords}")
    socketio.emit("new box", coords)