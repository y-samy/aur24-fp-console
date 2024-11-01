from flask import Blueprint, Response
from .. import camera, qr_decoder

video_routes = Blueprint('video_routes', __name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@video_routes.route("/feed")
def video_feed():
    return Response(
        gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

@video_routes.route("/get_cameras", methods=['GET'])
def video_get_cameras():
    cameras = camera.get_sources()
    return Response(status=204)

@video_routes.route("/set_camera/<i>", methods=['GET'])
def video_set_camera(i):
    camera.set_source(int(i))
    return Response(status=204)

@video_routes.route("/feed/pause/<on_or_off>", methods=['GET'])
def video_pause_resume(on_or_off):
    if on_or_off == "on":
        if not camera.get_pause_state():
            camera.toggle_pause()
    elif on_or_off == "off":
        if camera.get_pause_state():
            camera.toggle_pause()
    return Response(status=204)

@video_routes.route("/configure_scanning/<options>", methods=['GET'])
def video_configure_scanning(options):
    print(options)
    options = str(options)
    if options == "off":
        if camera.is_scanning():
            camera.toggle_scanning()
    else:
        if not camera.is_scanning():
            camera.toggle_scanning()
        qr_decoder.set_decoder(algorithm=options)
    return Response(status=204)