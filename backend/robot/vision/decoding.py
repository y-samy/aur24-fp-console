import cv2
import numpy as np
from pyzbar.pyzbar import decode


class QR:
    def __init__(self, receiver_func):
        self.decoder = "pyzbar"
        self.send_code = receiver_func

    def decode(self, frame):
        for qrcode in decode(frame):
            code = str(qrcode.data, "utf-8")
            self.send_code(code)
            pts = np.array([qrcode.polygon], np.int32)
            pts = pts.reshape(-1, 1, 2)
            cv2.polylines(frame, [pts], True, (255, 0, 0), 3)
            pts2 = qrcode.rect
            cv2.putText(
                frame,
                code,
                (pts2[0], pts2[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 255),
                2,
            )
