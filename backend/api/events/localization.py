import requests

def handle_encoder_data(encoder_data):
    imu_data = requests.get("http://192.168.172.75:8080/get?accX&accY&accZ&gyrX&gyrY&gyrZ")
    