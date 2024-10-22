import cv2
import numpy as np
from pyzbar.pyzbar import decode as pzb_decode_frame
from pyzbar.pyzbar import ZBarSymbol
from qreader import QReader

cv_decoder = cv2.QRCodeDetector()
cv_decode_frame = cv_decoder.detectAndDecodeMulti
qreader_decoder = QReader()
qreader_decode_frame = qreader_decoder.detect_and_decode


class QR:

    def __init__(self, receiver_function, algorithm="pyzbar"):
        self.__decoders = { "pyzbar": self.__pzb_algorithm, "cv": self.__cv_algorithm, "qreader": self.__qreader_algorithm}
        self.decode = self.__decoders[algorithm]
        self.set_receiver(receiver_function)

    def set_receiver(self, receiver_function):
        self.__send_text = receiver_function

    def set_decoder(self, algorithm="pyzbar"):
        self.decode = self.__decoders[algorithm]

    # Most efficient, great detection and decoding, poor handling of angled codes
    def __pzb_algorithm(self, frame):
        for qrcode in pzb_decode_frame(frame, symbols=[ZBarSymbol.QRCODE]):
            text = str(qrcode.data, "utf-8")
            obj_id = self.__send_text(text)
            pts = np.array([qrcode.polygon], np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
            corners = qrcode.rect  # top-left corner's coordinates
            cv2.putText(
                frame,
                obj_id,
                (corners[0], corners[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

    # Least efficient, worse decoding in general, better handling of angled codes
    def __cv_algorithm(self, frame):
        detected, decoded_text, points, _ = cv_decode_frame(frame)
        if detected:
            for text, pts in zip(decoded_text, points):
                if text:
                    obj_id = self.__send_text(text)
                    color = (0, 255, 0)
                    max_y = None  # y decreases as you go up somehow
                    for p in pts.astype(int):
                        p = p.tolist()
                        if max_y is None:
                            max_y = p[1]
                            corner = tuple(p)
                        elif max_y > p[1]:
                            corner = tuple(p)
                            max_y = p[1]
                    cv2.putText(
                        frame,
                        obj_id,
                        corner,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        1,
                        cv2.LINE_AA,
                    )
                else:
                    color = (0, 0, 255)
                cv2.polylines(frame, [pts.astype(int)], True, color, 3)

    # Most resource intensive, most accurate
    def __qreader_algorithm(self, frame):
        decoded_text, code_geometry = qreader_decode_frame(image=frame, return_detections=True)
        for i, qr in enumerate(decoded_text):
            if qr is not None:
                color = (0, 255, 0)
                obj_id = self.__send_text(qr)
                corner = code_geometry[i]["bbox_xyxy"].astype(int)
                cv2.putText(frame, obj_id, (corner[0], corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                color = (0, 0, 255)
            cv2.polylines(frame, [code_geometry[i]["polygon_xy"].astype(int)], True, color, 3)
