import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import paho.mqtt.client as mqtt  # For MQTT communication


class Motion(Node):
    def __init__(self):
        super().__init__("motion")
        # self.subscriber = self.create_subscription(
        #     String, "commands", self.commandProcessing, 10
        # )

        # Initialize MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect()  # defaults: localhost, 1883, 60s
        self.mqtt_client.loop_start()

    def commandProcessing(self, msg):
        commands = msg.data.split(",")

        try:
            index = int(commands[0])  # The index indicates the type of action
            value = float(commands[1])  # The value controls the movement/control
        except (ValueError, IndexError):
            self.get_logger().error("Invalid command format")
            return

        if index == 0:  # Control the arm (up/down)
            if value == 1:
                # Arm up
                arm_up = "0," + str(+1)
                self.mqtt_client.publish("robot/commands", arm_up)
            elif value == 0:
                # Arm down
                arm_down = "0," + str(0)
                self.mqtt_client.publish("robot/commands", arm_down)
        elif index == 1:  # Control the gripper (open/close)
            if value == 1:
                # Gripper open
                gripper_open = "1," + str(+1)
                self.mqtt_client.publish("robot/commands", gripper_open)
            elif value == 0:
                # Gripper close
                gripper_close = "1," + str(0)
                self.mqtt_client.publish("robot/commands", gripper_close)

        elif index == 2:  # Forward or backward movement
            if value > 0:
                # Forward movement
                forward = (
                    "2,"
                    + str(int(np.interp(value, [0, 1], [0, 255])))
                    + ","
                    + str(int(np.interp(value, [0, 1], [0, 255])))
                )
                self.mqtt_client.publish("robot/commands", forward)
            elif value < 0:
                # Backward movement
                backward = (
                    "2,"
                    + str(int(np.interp(value, [-1, 0], [-255, 0])))
                    + ","
                    + str(int(np.interp(value, [-1, 0], [-255, 0])))
                )
                self.mqtt_client.publish("robot/commands", backward)

        elif index == 3:  # Rotate left or right
            if value > 0:
                # Rotate right
                right = (
                    "2,"
                    + str(int(np.interp(value, [0, 1], [0, 255])))
                    + ","
                    + str(int(np.interp(value, [0, 1], [0, -255])))
                )
                self.mqtt_client.publish("robot/commands", right)
            elif value < 0:
                # Rotate left
                left = (
                    "2,"
                    + str(int(np.interp(value, [0, 1], [0, -255])))
                    + ","
                    + str(int(np.interp(value, [0, 1], [0, 255])))
                )
                self.mqtt_client.publish("robot/commands", left)

        else:
            self.get_logger().info("Unknown index received")


def main(args=None):
    rclpy.init(args=args)
    node = Motion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
