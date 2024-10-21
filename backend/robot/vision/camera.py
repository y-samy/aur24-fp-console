import cv2
from os import name as platform
from cv2_enumerate_cameras import enumerate_cameras
from flask import Response


class VideoCamera(object):
    def __init__(self, scanner_function, camera_number=0):
        self.__preferred_enum_apis = {
            "nt": cv2.CAP_MSMF
        }  # enumerating API preferences according to OS
        self.__enum_api = self.__preferred_enum_apis[platform]  # setting the preference
        self.__pause = False  # stream should start out unpaused
        self.__scanning = False  # scanning should be turned on on-demand
        self.__send_to_scanner = scanner_function  # called when scanning is on, captured frame is passed as parameter
        self.__video = cv2.VideoCapture()  # source not set yet
        self.set_source(camera_number)  # choose the first camera by default (index 0)
        # setting dimensions
        self.__video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.__video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def set_source(self, source_index):
        self.__video.open(source_index, apiPreference=self.__enum_api)

    def pause_resume_stream(self):
        self.__pause = not self.__pause  # toggles the pause or resume state
        return self.__pause  # may be used for verification

    def toggle_scanning(self):
        self.__scanning = (
            not self.__scanning
        )  # toggles whether the scanning function should be called every frame
        return self.__scanning  # may be used for verification

    def get_frame(self):
        # return empty bytes if stream is paused
        if self.__pause:
            return b""
        _, frame = self.__video.read()  # TODO: add more error handling
        if self.__scanning:
            self.__send_to_scanner(frame)
        # returns empty bytes if the frame is not yet obtainable
        if frame is None:
            return b""
        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()

    def __del__(self):
        self.__video.release()
