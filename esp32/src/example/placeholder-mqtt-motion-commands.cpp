#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>


// WiFi
const char *ssid = "TeamB"; // Enter your Wi-Fi name
const char *password = "balobalo";  // Enter Wi-Fi password

// MQTT Broker
const char *mqtt_broker = "192.168.172.97";
const char *topic = "Motion Commands";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
String jsonBuffer;
void callback(char *topic, byte *payload, unsigned int length);
void setup() {
    // Set software serial baud to 115200;
    Serial.begin(115200);
    // Connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the Wi-Fi network");
    //connecting to a mqtt broker
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    while (!client.connected()) {
        String client_id = "esp32-client-";
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
        if (client.connect(client_id.c_str())) {
            Serial.println("Public EMQX MQTT broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }
    // Publish and subscribe
    client.publish(topic, "Hi, I'm ESP32 ^^");
    client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
}

void loop() {
    client.loop(); //mqtt client
}