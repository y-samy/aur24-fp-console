#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h> 
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
//Connects to WiFi and sets up the MQTT client, subscribing to the topic for receiving movement commands



// WiFi credentials
const char* ssid = "TeamB";
const char* password ="balobalo";
// MQTT Broker
const char *mqtt_broker = "192.168.251.97";
const char *topic = "Encoders";
const int mqtt_port = 1883; //constant port

WiFiClient espClient;
PubSubClient client(espClient);
String jsonBuffer;

// void callback(char *topic, byte *payload, unsigned int length);

// Motor pins
const int motor1Pin1 = 15; // Motor 1 direction pin 1
const int motor1Pin2 = 16; // Motor 1 direction pin 2
const int motorSpeed1 = 19; // Motor 1 speed pin (PWM) left
const int motor2Pin1 = 17; // Motor 2 direction pin 1
const int motor2Pin2 = 18; // Motor 2 direction pin 2
const int motorSpeed2 = 20; // Motor 2 speed pin (PWM) right

enum MotorDirection { FORWARD, REVERSE, STOP };


// Encoder pins
const int encoder1PinA = 34; // Encoder 1 A pin
const int encoder1PinB = 35; // Encoder 1 B pin
const int encoder2PinA = 32; // Encoder 2 A pin
const int encoder2PinB = 33; // Encoder 2 B pin 

// Servo pins & variables
Servo arm;
Servo gripper; 

const int max_angle = 180;
const int min_angle = 0;

int current_angle_arm = 0;
int current_angle_grip = 0;

int armPin = 17;
int gripperPin = 18;


// Variables for motor speed and encoder counts
volatile int encoder1Count = 0;
volatile int encoder2Count = 0; 
const int maxSpeed = 255; 

unsigned long lastPublishTime = 0; // To track the last publish time
const unsigned long publishInterval = 30; // 30 milliseconds  

TaskHandle_t task1Handle = NULL; // create task handle 
TaskHandle_t task2Handle = NULL; 


// function to handle the input 
void callback(char* topic, byte* payload, unsigned int length) {
    payload[length] = '\0'; // Null-terminate the string
    String message = String((char*)payload);
    int command[3] = {0}; //message 
          Serial.println(message);  

    // Assuming the message format is "cmd,param1,param2,param3"
     int numParams = sscanf(message.c_str(), "%d,%d,%d", &command[0], &command[1], &command[2]);
    
    Serial.println(command[0]);
    Serial.println(command[1]);
    Serial.println(command[2]);
            
        if (command[0] == 0) { // Input value is for arm
            armMotion(command[1]);
        } else if (command[0] == 1) { // Input value is for grip
            gripMotion(command[1]);
        } else if (command[0] == 2) { // Input values are for motors
            motorMotion(command[1], command[2]); // left_motor, right_motor
            
        }
    
}

// movements functions
void motorMotion(int leftPwm, int rightPwm) {
    leftPwm = constrain(leftPwm, -maxSpeed, maxSpeed);
    rightPwm = constrain(rightPwm, -maxSpeed, maxSpeed);
    
    // Set motor directions
    MotorDirection leftDir = (leftPwm > 0) ? FORWARD : (leftPwm < 0) ? REVERSE : STOP;
    MotorDirection rightDir = (rightPwm > 0) ? FORWARD : (rightPwm < 0) ? REVERSE : STOP;

    // Control left motor
    switch (leftDir) {
        case FORWARD:
            digitalWrite(motor1Pin1, HIGH);
            digitalWrite(motor1Pin2, LOW);
            ledcWrite(motorSpeed1, leftPwm);
            break;
        case REVERSE:
            digitalWrite(motor1Pin1, LOW);
            digitalWrite(motor1Pin2, HIGH);
            ledcWrite(motorSpeed1, -leftPwm); // Use absolute value
            break;
        case STOP:
            digitalWrite(motor1Pin1, LOW);
            digitalWrite(motor1Pin2, LOW);
            ledcWrite(motorSpeed1, 0);
            break;
    }
    
    // Control right motor
    switch (rightDir) {
        case FORWARD:
            digitalWrite(motor2Pin1, HIGH);
            digitalWrite(motor2Pin2, LOW);
            ledcWrite(motorSpeed2, rightPwm);
            break;
        case REVERSE:
            digitalWrite(motor2Pin1, LOW);
            digitalWrite(motor2Pin2, HIGH);
            ledcWrite(motorSpeed2, -rightPwm); // Use absolute value
            break;
        case STOP:
            digitalWrite(motor2Pin1, LOW);
            digitalWrite(motor2Pin2, LOW);
            ledcWrite(motorSpeed2, 0);
            break;
    }
}
void armMotion(int direction) { 
    int current_angle_arm = arm.read(); // Get the current angle
  Serial.println(current_angle_arm);
    if (direction == 1) {
        for (int i = current_angle_arm; i <= max_angle; i += 1) {
            arm.write(i);
            delay(15); // Small delay to allow the servo to move
        }
    } else if (direction == 0) {
        for (int i = current_angle_arm; i >= min_angle; i -= 1) {
            arm.write(i);
            delay(15); // Small delay to allow the servo to move
        }
    }
   current_angle_arm = arm.read(); 
}

void gripMotion(int dir){
     int current_angle_grip = gripper.read(); // Get the current angle
   // Serial.println(current_angle_grip);

    if (dir == 1) {
        for (int i = current_angle_grip; i <= max_angle; i += 5) {
            gripper.write(i);
            delay(15); // Small delay to allow the servo to move
        }
    } else if (dir == 0) {
        for (int i = current_angle_grip; i >= min_angle; i -= 5) {
            gripper.write(i);
            delay(15); // Small delay to allow the servo to move
        }
    }
   current_angle_grip = gripper.read(); 
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

// Publish encoder input
void publishEncoderStates(const char* topic) {

   String message = String(encoder1Count) + "," + String(encoder2Count); // Prepare the message
    const int maxRetries = 5; // Maximum number of retries
    int attempts = 0; // Attempt counter

    while (attempts < maxRetries) {
      
        if (client.publish(topic, message.c_str())) {
            Serial.println("Message sent successfully");
            return; // Exit the function if successful
        } else {
            Serial.println("Message failed to send. Retrying...");
            attempts++;
            delay(20); // Delay before retrying (1 second)
        }
    }

    Serial.println("Failed to send message after multiple attempts.");
}

  void task1connection(void *parameters){ 

      
    while(1){
        if (!client.connected()) {         
        reconnect();
    }
    client.loop();

    vTaskDelay(1);
    }
} 

void updatePublishEncoders(void *p){


  while(1){

    updateEncoder1A();
    updateEncoder1B();
    updateEncoder2A();
    updateEncoder1B();

    // Check if 30 milliseconds have passed since the last publish
          unsigned long currentTime = millis();
    if (currentTime - lastPublishTime >= publishInterval) {
        publishEncoderStates("Encoders"); // Publish the encoder states
        lastPublishTime = currentTime; // Update the last publish time

    }
    vTaskDelay(1);
  }
}

// Setup
void setup() {
    Serial.begin(115200);
  
    ESP32PWM::allocateTimer(0);
	  ESP32PWM::allocateTimer(1);
	  ESP32PWM::allocateTimer(2);
	  ESP32PWM::allocateTimer(3);
	  arm.setPeriodHertz(50);    // standard 50 hz servo
    gripper.setPeriodHertz(50);    // standard 50 hz servo
	  arm.attach(armPin, 500, 2500); // Attach arm
    gripper.attach(gripperPin, 1000, 2000); // Attach gripper

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

            // Handle incoming messages
    client.setCallback(callback);

    xTaskCreate(
        task1connection,      // Function name of the task
        "wifi_mqtt_callback",   // Name of the task (e.g. for debugging)
        10000,        // Stack size (bytes)
        NULL,        // Parameter to pass
        1,           // Task priority
        &task1Handle   // Assign task handle
      ); 

    xTaskCreate(
        updatePublishEncoders,
        "encoder_read_publish",
        10000,
        NULL,
        1,
        &task2Handle
    );
}

void loop() {  
}
  


