import cv2


class VideoCamera(object):
    def __init__(self, camera_number, decoder_func):
        self.video = cv2.VideoCapture(camera_number)
        self.video.set(3, 640)
        self.video.set(4, 480)
        self.send_for_decode = decoder_func
        self.scanning = False

    def toggle_scanning(self):
        self.scanning = not self.scanning
        return self.scanning

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if self.scanning:
            self.send_for_decode(frame)
        success, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
