import cv2
from os import name as platform
from cv2_enumerate_cameras import enumerate_cameras


class VideoCamera(object):
    def __init__(self, scanner_function, camera_number=0):
        self.__preferred_enum_apis = {
            "nt": cv2.CAP_MSMF,
            "posix": cv2.CAP_GSTREAMER
        }  # enumerating API preferences according to OS
        self.__enum_api = self.__preferred_enum_apis[platform]
        self.__cameras = []
        self.__pause = False  # stream should start out unpaused
        self.__scanning = False  # scanning should be turned on on-demand
        self.__send_to_scanner = scanner_function  # called when scanning is on, captured frame is passed as parameter
        self.__video = cv2.VideoCapture()
        self.set_source(camera_number)
        self.__video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.__video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def set_source(self, source_index):
        # TODO: add handling for no cameras found
        if source_index > len(self.__cameras) or source_index < 0:
            source_index = 0 # permissive input validation - input is not user dependent
        self.__video.open(source_index, apiPreference=self.__enum_api)

    def get_sources(self):
        for cam in enumerate_cameras(self.__enum_api):
            self.__cameras = []
            self.__cameras.append(cam.name)
        return self.__cameras

    def pause_resume_stream(self):
        self.__pause = not self.__pause
        return self.__pause
    
    def is_scanning(self):
        return self.__scanning
    
    def toggle_scanning(self):
        self.__scanning = not self.__scanning

    def get_frame(self):
        if self.__pause:
            return b""
        _, frame = self.__video.read()  # TODO: add more error handling
        if self.__scanning:
            self.__send_to_scanner(frame)
        if frame is None:
            return b""
        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()

    def __del__(self):
        self.__video.release()