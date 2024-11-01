from . import socketio, mqttc
import numpy as np

publish = mqttc.publish


@socketio.on("gamepad buttons")
def map_and_send_buttons(command):
    print(command)
    #(2,2)
    # mqttc.publish("Motion Commands", command, qos=1) # to localhost:1883
    index = int(command[0])
    value = float(command[2:])
    if index == 0:  # Control the arm (up/down)
        if value == 1:
            # Arm up
            arm_up = "0," + str(+1)
            publish("Motion Commands", arm_up)
        elif value == 0:
            # Arm down
            arm_down = "0," + str(0)
            publish("Motion Commands", arm_down)
    elif index == 1:  # Control the gripper (open/close)
        if value == 1:
            # Gripper open
            gripper_open = "1," + str(+1)
            publish("Motion Commands", gripper_open)
        elif value == 0:
            # Gripper close
            gripper_close = "1," + str(0)
            publish("Motion Commands", gripper_close)
    elif index == 2:  # Forward or backward movement
        if value > 0:
            # Forward movement
            forward = (
                "2,"
                + str(int(np.interp(value, [0, 1], [0, 255])))
                + ","
                + str(int(np.interp(value, [0, 1], [0, 255])))
            )
            publish("Motion Commands", forward)
        elif value < 0:
            # Backward movement
            backward = (
                "2,"
                + str(int(np.interp(value, [-1, 0], [-255, 0])))
                + ","
                + str(int(np.interp(value, [-1, 0], [-255, 0])))
            )
            publish("Motion Commands", backward)
    elif index == 3:  # Rotate left or right
        if value > 0:
            # Rotate right
            right = (
                "2,"
                + str(int(np.interp(value, [0, 1], [0, 255])))
                + ","
                + str(int(np.interp(value, [0, 1], [0, -255])))
            )
            publish("Motion Commands", right)
        elif value < 0:
            # Rotate left
            left = (
                "2,"
                + str(int(np.interp(value, [0, 1], [0, -255])))
                + ","
                + str(int(np.interp(value, [0, 1], [0, 255])))
            )
            publish("Motion Commands", left)
    else:
        print("Unknown index received")
