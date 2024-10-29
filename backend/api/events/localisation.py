import time
import numpy as np
import requests
from .fusionekf import FusionEKF
from flask import jsonify

# Set numpy print options to avoid scientific notation
np.set_printoptions(suppress=True, precision=8)

# Initialize the EKF once outside the function to maintain state across calls
ekf = FusionEKF()
counts = 16  # counts per revolution
radius = 0.325  # radius of wheel


def sensorFusion(aX, gZ, eL, eR):
    currentTime = time.time()
    timestamp = int(currentTime * 1000000)  # Convert seconds to microseconds

    # Process IMU measurement
    imu_measurement = np.array([[aX], [0], [gZ]])
    ekf.process_measurement(timestamp, "IMU", imu_measurement)

    # Process wheel encoder measurement
    wheel_measurement = np.array([[eL], [eR], [0]])
    ekf.process_measurement(timestamp, "WHEEL_ENCODER", wheel_measurement)

    # Return the position (px, py) and yaw
    return ekf.ekf_.x[:3]  # [px, py, yaw]


def calcDistance(x):
    return (x / counts) * 2 * 3.14156 * radius


def handleReadings(encoderData):
    print(encoderData)
    try:
        imu_data = jsonify(
            (requests.get("http://192.168.159.194:8080/get?linX&gyrZ")).content
        )["buffer"]
    except requests.ConnectionError:
        return
    aX = imu_data["linX"]["buffer"][0]
    gZ = imu_data["gyrZ"]["buffer"][0]
    eLC = encoderData[0]
    eRC = encoderData[1]
    print(encoderData)
    eL = calcDistance(eLC)
    eR = calcDistance(eRC)

    sensorFusion(aX, gZ, eL, eR)


# if __name__ == "__main__":
#     try:
#         print("Test 1 Result:", sensorFusion(0.0, 0.0, 0.0, 0.0))  # Initial state
#         print("Test 2 Result:", sensorFusion(0.064, 0, 6.4, 6.4))  # Change values for testing
#         print("Test 3 Result:", sensorFusion(0.1, 0, 3.2, 3.2))    # Moderate movement with acceleration
#         print("Test 4 Result:", sensorFusion(0.05, 0.1, 2.0, 2.5)) # Curved path movement
#         print("Test 5 Result:", sensorFusion(-0.05, 0, 1.6, 1.6))  # Deceleration to stop
#         print("Test 6 Result:", sensorFusion(0.02, 0.5, 1.0, 1.5)) # Sharp turn
#     except Exception as e:
#         print(f"An error occurred: {e}")
# Expected Values
# (0,0,0)
# (4,5,0)
# (3.2,0,0)
# (2.25,0.225,0.1)
# (1.6,0,0)
# (1.096,0.599,0.5)
