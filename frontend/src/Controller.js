import { useEffect } from "react";
import { io } from 'socket.io-client';
const socketIo = io('http://localhost:5000');
function GamepadController() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      const gamepads = navigator.getGamepads();
      let command = -1; // 0 arm, 1 grip, 2 move, 3 rotate
      let commandValue = 0; // arm up/down, grip open/close, move forward/backward (-1->1), rotate left/right (-1->1)
      if (gamepads[0]) { // Ensure a gamepad is connected
        command = -1;
        const gamepad = gamepads[0];
        // Create a state object to capture gamepad status
        if (gamepad.buttons[0].pressed){
          command = 0; // Arm down X 
          commandValue = 0;
        }
        else if (gamepad.buttons[3].pressed){
          command = 0; // Arm up triangle
          commandValue = 1;
        }
        else if (gamepad.buttons[1].pressed){
          command = 1; // Grip close O
          commandValue = 0;
        }
        else if (gamepad.buttons[2].pressed){
          command = 1; // Grip open square
          commandValue = 1;
        }
        else if (gamepad.buttons[7].pressed || gamepad.buttons[6].pressed){
          command = 2;
          commandValue = gamepad.buttons[7].value - gamepad.buttons[6].value
        }
        else if (gamepad.axes[2] > 0.1 || gamepad.axes[2] < -0.1){
          command = 3;
          commandValue = gamepad.axes[2];
        }
        };
      if (command !== -1){
      socketIo.emit("gamepad buttons", command, commandValue); 
      }
        // if(gp_state.r2 > gp_state.l2){
        //   gp_state.r2 = gp_state.r2 - gp_state.l2
        //   gp_state.l2 = 0
        // }
        // else{
        //   gp_state.l2 = gp_state.l2 - gp_state.r2
        //   gp.state.r2 = 0 
        // }
    }, 15); // Update every 15 milliseconds
    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  return null; // This component does not render anything
}

export default GamepadController;
