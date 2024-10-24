import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import time


class KalmanFilter:
    def __init__(self):
        self.state = np.zeros(3) #State vector: x, y, ,yaw
        self.F = np.eye(3) #State transition matrix
        self.Q = np.eye(3) * 0.1  #Process noise covariance
        self.H = np.eye(3)      #Measurement Matrix 
        self.R = np.eye(3) * 0.1    #Measurement noise covariance
        self.P = np.eye(3)  #State covariance matrix

    def predict(self,dt,vx,omega):
        self.F = np.array([
            [1, 0, -vx * np.sin(self.state[2]) * dt],
            [0, 1,  vx * np.cos(self.state[2]) * dt],
            [0, 0,  1]
        ])

        
        self.state[0] += vx * np.cos(self.state[2]) * dt
        self.state[1] += vx * np.sin(self.state[2]) * dt
        self.state[2] += omega * dt  # Update yaw with angular velocity

        # Update covariance matrix
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, measurement):
        y = measurement - (self.H @ self.state)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.state = self.state + (K @ y)
        self.P = (np.eye(len(self.P)) - K @ self.H) @ self.P

    def get_state(self):
        return self.state


class RobotPosition(Node):
    def __init__(self):
        super().__init__("localization")
        # Initialize robot's position and orientation
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.vx = 0.0  # Velocity from IMU
        self.omega = 0.0  # Yaw rate from IMU 
        self.publisher = self.create_publisher(String, "coordinates", 10)
        self.subscriber = self.create_subscription(
            String, "IMU", self.sensor_fusion, 10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.kf = KalmanFilter()
        self.last_time = time.time()
        self.WIDTH = 0.5  # Define the width of the robot for encoder updates

    def publish_coordinates(self):
        #Publish Fused Coordinates
        msg = f"Fused Position: ({self.x:.2f}, {self.y:.2f}) | Orientation: {self.theta:.2f}"
        self.publisher.publish(String(data=msg))
        self.get_logger().info(msg)

    def sensor_fusion(self, msg):
        #replace with actual IMU data
        imu_data = msg.data.split(",")
        self.vx = float(imu_data[0])  # Linear velocity mn IMU
        self.omega = float(imu_data[1])  # Angular velocity mn IMU


        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        
        self.kf.predict(dt, self.vx, self.omega) #Prediction IMU based

        encoder_left = 100  # Replace with actual encoder data
        encoder_right = 110  
        self.update_pose(encoder_left, encoder_right)

        fused_measurement = np.array([self.x, self.y, self.theta])
        self.kf.update(fused_measurement)
        
        fused_x = self.kf.state[0]
        fused_y = self.kf.state[1]
        fused_theta = self.kf.state[2]

        #update the robot’s position and orientation with the fused estimates
        self.x = fused_x
        self.y = fused_y
        self.theta = fused_theta
        
        self.publish_coordinates()

    def update_pose(self, encoder_left, encoder_right):
        dR = self.calc_distance(encoder_right)
        dL = self.calc_distance(encoder_left)
        distance = (dR + dL) / 2
        delta_theta = (dR - dL) / self.WIDTH
        self.theta += delta_theta
        self.x += distance * np.cos(self.theta)
        self.y += distance * np.sin(self.theta)

    def calc_distance(self, encoder_count):
        radius = 0.03
        counts_per_rev = 240
        return (encoder_count / counts_per_rev) * (2 * np.pi * radius)


def main(args=None):
    rclpy.init(args=args)
    node = RobotPosition()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()