import requests
from json import loads as jsonify


def handle_encoder_data():
    imu_data = jsonify((requests.get("http://192.168.172.75:8080/get?linX&linY&gyrZ")).content)["buffer"]
    
    readings = ["linX", "linY", "gyrZ"]
    for i in readings:
        print(f"{i},{imu_data[i]["buffer"][0]}")
        

