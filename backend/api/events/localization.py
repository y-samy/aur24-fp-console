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
WIDTH = 0.5  # Distance between 2 encoders
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
    dL = eL - lastEL
    dR = eR - lastER
    lastEL = eL
    lastER = eR
    distance = (dL + dR) / 2
    deltaTheta = (dR - dL) / WIDTH

    # Debugging output
    print(
        f"Encoder changes: dL={dL}, dR={dR}, distance={distance}, deltaTheta={deltaTheta}"
    )
    print(f"Yaw before update: {state[2]}")

    # Update the state with encoder-derived position and orientation changes
    state[0] += distance * np.cos(state[2])
    state[1] += distance * np.sin(state[2])
    state[2] += deltaTheta

    # Debugging output
    print(f"Updated state: x={state[0]}, y={state[1]}, yaw={state[2]}")


def update(measurement):
    global state, P
    y = measurement - (H @ state)
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    state += K @ y
    P = (np.eye(len(P)) - K @ H) @ P


def sensorFusion(aX, gZ, eL, eR):
    global lastTime, state
    currentTime = time.time()
    dt = currentTime - lastTime
    lastTime = currentTime

    predict(dt, aX, gZ)
    updatePose(eL, eR)

    # Ensure the measurement array is numeric
    fusedMeasurement = np.array([float(state[0]), float(state[1]), float(state[2])])
    update(fusedMeasurement)

    fusedX = state[0]
    fusedY = state[1]

    return f"{fusedX},{fusedY}"


if __name__ == "__main__":
    try:
        # Example testing with both accelerations and encoder readings
        print(sensorFusion(0.02, 0.03, 5, 5))  # Change encoder values
        print(sensorFusion(0.11, 0.13, 7, 6))  # Change encoder values
        print(sensorFusion(0.12, 0.14, 8, 11))  # Change encoder values
        print(sensorFusion(0.2, 0.1, 10, 13))  # Change encoder values

    except Exception as e:
        print(f"An error occurred: {e}")


# def handleSensorData(encoderData):
#     imu_data = jsonify(
#         (requests.get("http://192.168.172.75:8080/get?linX&gyrZ")).content
#     )["buffer"]
#     aX = imu_data["linX"]["buffer"][0]
#     gZ = imu_data["gyrZ"]["buffer"][0]
#     eL = encoderData[0]
#     eR = encoderData[1]
# print(sensorFusion(2, 3, 1, 2))
# import requests
# from json import loads as jsonify
# import numpy as np
# import time

# # Initialize Kalman filter parameters
# state = np.zeros(3)  # state[0]: x, state[1]: y, state[2]: yaw
# F = np.eye(3)
# Q = np.eye(3) * 0.1
# H = np.eye(3)
# R = np.eye(3) * 0.1
# P = np.eye(3)
# WIDTH = 0.5  # Distance between 2 encoders
# lastTime = time.time()
# lastEL = 0.0
# lastER = 0.0


# def predict(dt, aX, aY, gZ):
#     global state, F, P
#     # Calculate forward velocity from linear acceleration
#     # Using average acceleration over the time interval
#     velocityX = aX * dt
#     velocityY = aY * dt

#     # Update the state based on linear accelerations
#     state[0] += velocityX * np.cos(state[2]) * dt  # Update x based on yaw
#     state[1] += velocityY * np.sin(state[2]) * dt  # Update y based on yaw
#     state[2] += gZ * dt  # Update yaw

#     # Update the state transition matrix F
#     F = np.array(
#         [
#             [1, 0, -velocityY * dt],
#             [0, 1, velocityX * dt],
#             [0, 0, 1],
#         ]
#     )

#     # Update the error covariance
#     P = F @ P @ F.T + Q


# def updatePose(eL, eR):
#     global state, lastEL, lastER, WIDTH
#     # Calculate changes in encoder readings
#     dL = eL - lastEL
#     dR = eR - lastER
#     # Update last encoder positions
#     lastEL = eL
#     lastER = eR

#     # Calculate movement distance and change in orientation
#     distance = (dL + dR) / 2
#     deltaTheta = (dR - dL) / WIDTH

#     # Update the state using encoder-derived position and orientation changes
#     # Use the current yaw to update both x and y
#     state[0] += distance * np.cos(state[2])  # Update x
#     state[1] += distance * np.sin(state[2])  # Update y
#     state[2] += deltaTheta  # Update yaw

#     # Print for debugging
#     print(
#         f"UpdatePose: dL={dL}, dR={dR}, distance={distance:.3f}, deltaTheta={deltaTheta:.3f}"
#     )
#     print(f"Pose Updated: x={state[0]:.3f}, y={state[1]:.3f}, yaw={state[2]:.3f}")


# def update(measurement):
#     global state, P
#     y = measurement - (H @ state)
#     S = H @ P @ H.T + R
#     K = P @ H.T @ np.linalg.inv(S)

#     # Update state with the measurement
#     state += K @ y
#     # Update the error covariance
#     P = (np.eye(len(P)) - K @ H) @ P


# # Sensor fusion function combining IMU and encoder data
# def sensorFusion(aX, aY, gZ, eL, eR):
#     global lastTime, state

#     # Calculate time difference
#     currentTime = time.time()
#     dt = currentTime - lastTime
#     lastTime = currentTime

#     # Prediction step using IMU data
#     predict(dt, aX, aY, gZ)

#     # Update pose using encoder position data
#     updatePose(eL, eR)

#     # Fusion measurement update
#     fusedMeasurement = np.array([state[0], state[1], state[2]])
#     update(fusedMeasurement)

#     fusedX = state[0]
#     fusedY = state[1]

#     return f"{fusedX},{fusedY}"  # Return coordinates as a string


# if __name__ == "__main__":
#     try:
#         # Example testing with both accelerations and encoder readings
#         print(sensorFusion(0.02, 0.03, 0.5, 5, 5))  # Change encoder values
#         print(sensorFusion(0.11, 0.13, 0.4, 7, 6))  # Change encoder values
#         print(sensorFusion(0.12, 0.14, 0.50, 8, 11))  # Change encoder values
#         print(sensorFusion(0.2, 0.1, 0.1, 10, 13))  # Change encoder values

#     except Exception as e:
#         print(f"An error occurred: {e}")
