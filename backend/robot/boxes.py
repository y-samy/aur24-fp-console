import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

socketio = SocketIO()

# MQTT Broker details
MQTT_BROKER = "test.mosquitto.org" 
MQTT_PORT = 1883
MQTT_TOPIC = "robot/coordinates"  
mqtt_client = mqtt.Client()

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start() 
class Box:
    def __init__(self, dest_coords: dict, pickup_coords):
        self.dest_coords = dest_coords
        self.pickup_coords = pickup_coords
        self.is_picked_up = False

class BoxHandler:
    def __init__(self):
        self.boxes = []

    def pickup(self, box_num: int):
        self.boxes[box_num].is_picked_up = True

    def drop(self, box_num: int):
        self.boxes[box_num].is_picked_up = False

    def receive_coords(self, coords: str):
        coords = coords.split("&")
        if len(coords) < 2 or not all(coord.startswith(("X:", "Y:")) for coord in coords):
            print("Invalid coordinates format:", coords)
            return

        coords = {"X": coords[0][2:], "Y": coords[1][2:]}
        is_unique = True
        for box in self.boxes:
            if box.dest_coords == coords:
                is_unique = False
                break
        
        if is_unique:
            new_box = Box(coords, 1) 
            self.boxes.append(new_box)
            print("New box added:", coords)
            socketio.emit("new_scanned_data", {"coords": coords})
            mqtt_client.publish(MQTT_TOPIC, str(coords))  
