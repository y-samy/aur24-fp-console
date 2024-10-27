from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from robot.navigation.boxes import BoxHandler
from robot.vision.camera import VideoCamera
from robot.vision.decoding import QR

from .events.mqtt import mqttc

box_handler = BoxHandler()
qr_decoder = QR(receiver_function=box_handler.receive_coords)
camera = VideoCamera(scanner_function=qr_decoder.decode, camera_number=1, scanning=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# api routes
from .routes import video_routes
app.register_blueprint(video_routes, url_prefix='/video')

# mqtt
mqttc.connect(host="localhost")
mqttc.loop_start()

# api events
from .events import *
box_handler.set_callback_on_new_box(push_new_box)

