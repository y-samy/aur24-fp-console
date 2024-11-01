import numpy as np


class KalmanFilter:
    def __init__(self):
        self.x = np.zeros((6, 1))  # State vector
        self.P = np.eye(6)  # Error covariance
        self.F = np.eye(6)  # State transition matrix
        self.Q = np.eye(6) * 0.01  # Adjusted process noise covariance
        self.H = np.zeros((3, 6))  # Measurement matrix
        self.R_imu = np.eye(3) * 0.05  # Adjusted measurement noise covariance for IMU
        self.R_wheel = (
            np.eye(3) * 0.05
        )  # Adjusted measurement noise covariance for wheel encoders

    def predict(self):
        # print(f"Predicting... Current state: {self.x.flatten()}")
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        # print(f"Predicted state: {self.x.flatten()}")

    def update(self, z, R):
        # print(f"Updating... Measurement: {z.flatten()}")
        y = z - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        self.x += K @ y
        self.P = (np.eye(len(self.P)) - K @ self.H) @ self.P
        # print(f"Updated state: {self.x.flatten()}")

    def update_imu(self, z):
        self.H = np.eye(3, 6)  # Update H for IMU measurements
        self.update(z, self.R_imu)

    def update_wheel_encoder(self, z):
        self.H = np.array(
            [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0]]
        )  # Update H for wheel encoder measurements
        self.update(z, self.R_wheel)
