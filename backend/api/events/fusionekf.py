from .kalmanfilter import KalmanFilter
import numpy as np


class FusionEKF:
    def __init__(self):
        self.ekf_ = KalmanFilter()
        self.is_initialized = False
        self.previous_timestamp = 0
        self.L = 0.2  # Distance between wheels in meters, adjust as needed

    def process_measurement(self, timestamp, sensor_type, measurement):
        if not self.is_initialized:
            self.ekf_.x = np.zeros((6, 1))  # [px, py, vx, vy, yaw, yaw_rate]
            self.previous_timestamp = timestamp
            self.is_initialized = True
            return

        dt = (
            timestamp - self.previous_timestamp
        ) / 1000000.0  # Convert micros to seconds
        self.previous_timestamp = timestamp

        # Predict the state based on the time difference
        self.ekf_.F = np.eye(6)
        self.ekf_.F[0, 2] = dt  # Velocity effect on position x
        self.ekf_.F[1, 3] = dt  # Velocity effect on position y

        self.ekf_.predict()

        if sensor_type == "IMU":
            self.ekf_.update_imu(measurement)
        elif sensor_type == "WHEEL_ENCODER":
            # measurement: [eL, eR, 0] where eL and eR are the distances from the left and right encoders
            dL = measurement[0, 0]  # Distance from left encoder
            dR = measurement[1, 0]  # Distance from right encoder

            # Calculate delta values
            delta_d = (dL + dR) / 2.0  # Average distance
            delta_yaw = (dR - dL) / self.L  # Change in yaw

            # Update the state
            px = self.ekf_.x[0, 0] + delta_d * np.cos(
                self.ekf_.x[4, 0]
            )  # Update x position
            py = self.ekf_.x[1, 0] + delta_d * np.sin(
                self.ekf_.x[4, 0]
            )  # Update y position
            yaw = (self.ekf_.x[4, 0] + delta_yaw + np.pi) % (2 * np.pi) - np.pi

            # Set the new position and yaw in the state vector
            self.ekf_.x[0, 0] = px
            self.ekf_.x[1, 0] = py
            self.ekf_.x[4, 0] = yaw

            # Update the measurement model for wheel encoder
            self.ekf_.update_wheel_encoder(measurement)
