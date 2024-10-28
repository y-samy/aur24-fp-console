import requests
from json import loads as jsonify
import numpy as np
import time

state = np.zeros(3)
F = np.eye(3)
Q = np.eye(3) * 0.1
H = np.eye(3)
R = np.eye(3) * 0.1
P = np.eye(3)
WIDTH = 0.5  # dist between 2 encoders
lastTime = time.time()
lastEL = 0.0
lastER = 0.0


def predict(dt, aX, gZ):
    global state, F, P
    velocity = aX * dt  # Calculate forward velocity from linear acceleration
    F = np.array(
        [
            [1, 0, -velocity * np.sin(state[2]) * dt],
            [0, 1, velocity * np.cos(state[2]) * dt],
            [0, 0, 1],
        ]
    )
    state[0] += velocity * np.cos(state[2]) * dt
    state[1] += velocity * np.sin(state[2]) * dt
    state[2] += gZ * dt
    P = F @ P @ F.T + Q


def updatePose(eL, eR):
    global state, lastEL, lastER, WIDTH
    # Calculate changes in encoder readings
    dL = eL - lastEL
    dR = eR - lastER
    # Update last encoder positions
    lastEL = eL
    lastER = eR
    # Calculate movement distance and change in orientation
    distance = (dL + dR) / 2
    deltaTheta = (dR - dL) / WIDTH
    # Update the state with encoder-derived position and orientation changes
    state[0] += distance * np.cos(state[2])
    state[1] += distance * np.sin(state[2])
    state[2] += deltaTheta


def update(measurement):
    global state, P
    y = measurement - (H @ state)
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    state = state + (K @ y)
    P = (np.eye(len(P)) - K @ H) @ P


# Sensor fusion function combining IMU and encoder data
def sensorFusion(aX, gZ, eL, eR):
    global lastTime, state

    # Calculate time difference
    currentTime = time.time()
    dt = currentTime - lastTime
    lastTime = currentTime

    # Prediction step using IMU data
    predict(dt, aX, gZ)

    # Update pose using encoder position data
    updatePose(eL, eR)

    # Fusion measurement update
    fusedMeasurment = np.array([state[0], state[1], state[2]])
    update(fusedMeasurment)

    fusedX = state[0]
    fusedY = state[1]
    fusedTheta = state[2]

    return fusedX + "," + fusedY


def handleSensorData(encoderData):
    imu_data = jsonify(
        (requests.get("http://192.168.172.75:8080/get?linX&gyrZ")).content
    )["buffer"]
    aX = imu_data["linX"]["buffer"][0]
    gZ = imu_data["gyrZ"]["buffer"][0]
    eL = encoderData[0]
    eR = encoderData[1]
    print(sensorFusion(aX, gZ, eL, eR))
