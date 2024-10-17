from flask import Flask, render_template, Response
from robot.boxes import BoxHandler
from robot.vision import VideoCamera

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("../ui/src/index.js")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


box_handler = BoxHandler()
camera = VideoCamera(box_handler.receive_coords)
camera.do_scanning()

@app.route("/video_feed")
def video_feed():
    return Response(
        gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
