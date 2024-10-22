# to get localazation data
import paho.mqtt.client as mqtt
# MQTT Broker details
MQTT_BROKER = "test.mosquitto.org" 
MQTT_PORT = 1883
MQTT_TOPIC = "robot/coordinates"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    # Subscribe to a topic if needed
    client.subscribe(MQTT_TOPIC)
def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
# Create a new client instance
def create_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client

# Publish a message to a topic
def publish_message(client, topic, message):
    client.publish(topic, message)

# Function to stop the MQTT loop
def stop_mqtt(client):
    client.loop_stop()
    client.disconnect()
