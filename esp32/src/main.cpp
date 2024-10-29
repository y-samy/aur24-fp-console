#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>
//Connects to WiFi and sets up the MQTT client, subscribing to the "robot/move" topic for receiving movement commands

// WiFi credentials
const char* ssid = "TeamB";
const char* password = "balobalo";
// MQTT Broker
const char *mqtt_broker = "192.168.159.97";
const char *topic = "Encoders";
const int mqtt_port = 1883; 

WiFiClient espClient;
PubSubClient client(espClient);
String jsonBuffer;

void callback(char *topic, byte *payload, unsigned int length);

// Motor pins
const int motor1Pin1 = 15; // Motor 1 direction pin 1
const int motor1Pin2 = 16; // Motor 1 direction pin 2
const int motorSpeed1 = 19; // Motor 1 speed pin (PWM) left
const int motor2Pin1 = 17; // Motor 2 direction pin 1
const int motor2Pin2 = 18; // Motor 2 direction pin 2
const int motorSpeed2 = 20; // Motor 2 speed pin (PWM) right

// Encoder pins
const int encoder1PinA = 34; // Encoder 1 A pin
const int encoder1PinB = 35; // Encoder 1 B pin
const int encoder2PinA = 32; // Encoder 2 A pin
const int encoder2PinB = 33; // Encoder 2 B pin 
void updateEncoder1A();
void updateEncoder1B();
void updateEncoder2A();
void updateEncoder2B();
void reconnect();
// Servo pins & variables
Servo servo1;
Servo gripper;

int servo1Pin = 17;
int gripperPin = 18;
int min_angle = 0;
int max_angle = 180;


// Variables for motor speed and encoder counts
volatile int encoder1Count = 0;
volatile int encoder2Count = 0;
const int maxSpeed = 255;
unsigned long lastPublishTime = 0;



// function to handle the input 

// movements functions
void motorMotion(int leftPwm, int rightPwm) {

    analogWrite(motorSpeed1, leftPwm);
    analogWrite(motorSpeed2, rightPwm);

   } 
void armMotion(int direction){ 

  int current_angle = min_angle;

  if( direction > 0 ){
    for(int i=5; i<=180; i += 5){
      servo1.write(current_angle + i);
  }
  }else if(direction < 0){
    for(int i=180; i>0; i -= 5){
      servo1.write(current_angle - i);
  }
  }
  current_angle = servo1.read();
} 
void gripMotion(int direction){
    int current_angle = min_angle;

  if( direction > 0 ){
    for(int i=5; i<=180; i += 5){
      gripper.write(current_angle + i);
  }
  }else if(direction < 0){
    for(int i=180; i>0; i -= 5){
      gripper.write(current_angle - i);
  }
  }
  current_angle = gripper.read();
}

void callback(char* topic, byte* payload, unsigned int length) {
    payload[length] = '\0'; // Null-terminate the string
    int command[4];
    for(int i=0; i<4; i++){
      if( command[0] == 0){ //input value is for arm
        armMotion( command[1] );
      }else if( command[0]==1 ){ //input value is for grip
          gripMotion( command[1] );
      }else if( command[0]==2 || command[0]==3 ){ //input values are for motors
          motorMotion( command[1], command[2] ); //left_motor , right_motor
      }
    
    }
}

// Publish encoder input
void publishEncoderStates(const char* topic) {

   if (client.publish(topic, encoder1Count + "," + encoder2Count)) {
    Serial.println("Message sent successfully");
  } else {
    Serial.println("Message failed to send");
  }
  }

// Encoder update functions
void updateEncoder1A() {
    if (digitalRead(encoder1PinA) > digitalRead(encoder1PinB) ) {
        encoder1Count++;
    } else {
        encoder1Count--;
    }
    
}

void updateEncoder1B() {
    if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
        encoder1Count++;
    } else {
        encoder1Count--;
    }
}  
void updateEncoder2A() {
    if (digitalRead(encoder2PinA) > digitalRead(encoder2PinB) ) {
        encoder2Count++;
    } else {
        encoder2Count--;
    }
}

void updateEncoder2B() {
    if (digitalRead(encoder2PinA) == digitalRead(encoder2PinB)) {
        encoder2Count++;
    } else {
        encoder2Count--;
    }
}


// Reconnect to MQTT broker
void reconnect() {
    String client_id = "esp32-client-";
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
        if (client.connect(client_id.c_str())) {
            Serial.println("connected");
            client.subscribe("Motion Commands"); // Subscribe to the movement topic "robot/move"
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            delay(2000);
        }
    }
}

// Setup
void setup() {
    Serial.begin(115200);
    
    ESP32PWM::allocateTimer(0);
	  ESP32PWM::allocateTimer(1);
	  ESP32PWM::allocateTimer(2);
	  ESP32PWM::allocateTimer(3);
	  servo1.setPeriodHertz(50);    // standard 50 hz servo
	  servo1.attach(servo1Pin, 1000, 2000);
    servo1.setPeriodHertz(50);    // standard 50 hz servo
	  servo1.attach(gripperPin, 1000, 2000);

    // Motor pins
    pinMode(motor1Pin1, OUTPUT);
    pinMode(motor1Pin2, OUTPUT);
    pinMode(motorSpeed1, OUTPUT);
    pinMode(motor2Pin1, OUTPUT);
    pinMode(motor2Pin2, OUTPUT);
    pinMode(motorSpeed2, OUTPUT);
    
    // Encoder pins
    pinMode(encoder1PinA, INPUT_PULLUP);
    pinMode(encoder1PinB, INPUT_PULLUP);
    pinMode(encoder2PinA, INPUT_PULLUP);
    pinMode(encoder2PinB, INPUT_PULLUP);
    
    attachInterrupt(encoder1PinA, updateEncoder1A, RISING);  //Interrupts are attached to encoder A pins to detect changes and update the encoder counts
    attachInterrupt(encoder1PinB, updateEncoder1B, RISING);
    attachInterrupt(encoder2PinA, updateEncoder2A, RISING);
    attachInterrupt(encoder2PinB, updateEncoder2B, RISING);

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Setup MQTT
    client.setServer(mqtt_broker, mqtt_port); //Sets the server details
    reconnect();
}

void loop() {  
  //checks the MQTT connection and publishes the motor speeds to the "robot/speeds" topic based on the encoder readings
      if (!client.connected()) {
        reconnect();
    }
    client.loop();

    // Handle incoming messages
    client.setCallback(callback);

    // Check if 30 ms has passed
    unsigned long currentTime = millis();
    if (currentTime - lastPublishTime >= 30) {
        lastPublishTime = currentTime; // Update the last publish time
        publishEncoderStates(topic); // Call your publish function
    }

}