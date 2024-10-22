import { useEffect } from "react";

function GamepadController() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      const gamepads = navigator.getGamepads();

      if (gamepads[0]) { // Ensure a gamepad is connected
        const gamepad = gamepads[0];

        // Create a state object to capture gamepad status
        const gp_state = {
          // Button states (pressed or not)
          x: gamepad.buttons[0].pressed, // B0 ==> x
          o: gamepad.buttons[1].pressed, // B1 ==> o
          s: gamepad.buttons[2].pressed, // B2 ==> square
          t: gamepad.buttons[3].pressed, // B3 ==> triangle
          r2: gamepad.buttons[7].value, // Right Trigger (B7) ==> R2
          l2: gamepad.buttons[6].value, // Left Trigger (B6) ==> L2
          l1: gamepad.buttons[4].pressed, // L1 ==> L1
          r1: gamepad.buttons[5].pressed, // R1 ==> R1

        };
        if(gp_state.l1){
  console.log( gamepads);
        }
      }
    }, 15); // Update every 15 milliseconds

    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  return null; // This component does not render anything
}

export default GamepadController;
