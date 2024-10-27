import requests
from json import loads as jsonify


def handle_encoder_data(encoderData):
    # imu_data = jsonify(
    #     (requests.get("http://192.168.172.75:8080/get?linX&gyrZ")).content
    # )["buffer"]

    # readings = ["linX", "gyrZ"]
    # aX = imu_data["linX"]["buffer"][0]
    # gZ = imu_data["gyrZ"]["buffer"][0]
    print(encoderData)
