from flask import Flask, render_template, Response
from robot.boxes import BoxHandler
from robot.vision.camera import VideoCamera
from robot.vision.decoding import QR

app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

box_handler = BoxHandler()
qr_decoder = QR(receiver_func=box_handler.receive_coords)
camera = VideoCamera(decoder_func=qr_decoder.decode)


@app.route("/video/feed")
def video_feed():
    return Response(
        gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/video/toggle_scanning")
def toggle_scanning():
    camera.toggle_scanning()
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
