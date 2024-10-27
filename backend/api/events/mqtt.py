import paho.mqtt.client as mqtt
from .localization import handle_encoder_data

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to mqtt broker {reason_code}")
    client.subscribe("Encoders")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "Encoders":
        handle_encoder_data(msg.payload)



mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.on_connect = on_connect
mqttc.on_message = on_message