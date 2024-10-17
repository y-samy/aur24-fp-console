import cv2
import numpy as np
from pyzbar.pyzbar import decode

class VideoCamera(object):
    def __init__(self, coords_parser):
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 640)
        self.video.set(4, 480)
        self.update_boxes = coords_parser

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        for barcode in decode(frame):
            box_coords = str(barcode.data, "utf-8")
            self.update_boxes(box_coords)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape(-1, 1, 2)
            cv2.polylines(frame, [pts], True, (255, 0, 0), 3)
            pts2 = barcode.rect
            cv2.putText(
                frame,
                box_coords,
                (pts2[0], pts2[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 255),
                2,
            )
        success, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
