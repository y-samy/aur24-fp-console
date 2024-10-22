# main.py
from flask import Flask, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from mqtt_client import create_mqtt_client, publish_message, stop_mqtt
from robot.boxes import BoxHandler
from robot.vision.camera import VideoCamera
from robot.vision.decoding import QR

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Create the MQTT client
mqtt_client = create_mqtt_client()

box_handler = BoxHandler()
qr_decoder = QR(receiver_func=box_handler.receive_coords)
camera = VideoCamera(camera_number=1, decoder_func=qr_decoder.decode)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video/feed")
def video_feed():
    return Response(
        gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

@socketio.on("connect")
def handle_connect():
    print("A client has connected")
    emit("connected", {"message": "You are connected to the WebSocket server!"})

@socketio.on("new_scanned_data")
def handle_new_scanned_data(data):
    coords = data.get('coords')
    # Publish coordinates to MQTT
    publish_message(mqtt_client, "robot/coordinates", str(coords))
    emit("scanning_toggled", {"status": "Data published to MQTT"}, broadcast=True)

@socketio.on("toggle_scanning")
def handle_toggle_scanning():
    print("Toggling scanning...")  
    camera.toggle_scanning()
    emit("scanning_toggled", {"status": "Scanning toggled"}, broadcast=True)
@socketio.on("request_localization_data")
def handle_request_localization_data():
    localization_data = {"x": box_handler.x, "y": box_handler.y}
    emit("localization_data", localization_data)

if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0", port=5000, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        stop_mqtt(mqtt_client)