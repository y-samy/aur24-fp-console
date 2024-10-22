from flask import Flask, Response
from robot.navigation.boxes import BoxHandler
from robot.vision.camera import VideoCamera
from robot.vision.decoding import QR

app = Flask(__name__)


box_handler = BoxHandler()
qr_decoder = QR(receiver_function=box_handler.receive_coords)
camera = VideoCamera(scanner_function=qr_decoder.decode, camera_number=0)

def gen_stream(cam):
    while True:
        frame = cam.get_frame()
        yield (b"--frame\r\n" b"Content-Type: application/octet-stream\r\n\r\n" + frame + b"\r\n\r\n")


@app.route("/video/feed")
def video_feed():
    return Response(
        gen_stream(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

@app.route("/video/set_source/<index>")
def video_set_source(index):
    camera.set_source(source_index=int(index))
    return Response(status=204)

@app.route("/video/feed/pause_resume")
def pause_video_feed():
    camera.pause_resume_stream()
    return Response(status=204)

@app.route("/video/toggle_scanning")
def toggle_scanning():
    camera.toggle_scanning()
    return Response(status=204)

@app.route("/video/scanning/set_algorithm/<algorithm>")
def set_scanning_algorithm(algorithm):
    qr_decoder.set_decoder(str(algorithm))
    return Response(status=204)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)
