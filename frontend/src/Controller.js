import { useEffect } from "react";

function GamepadController() {
  // B6 back
  // B7 fwd
  // B0, B1 : x, o
  // B2, B3: sqr, tri
  // Axes: +ve right, down
  // 0, 1: lStick, h, v
  // 2, 3: rStick, h, v
  // navigator.getGamepads()[0].buttons[btnID].pressed -> bool
  // navigator.getGamepads()[0].buttons[btnID].value -> 0-1f
  // navigator.getGamepads()[0].axes -> array

  useEffect(() => {
    const intervalId = setInterval(() => {
      const gamepads = navigator.getGamepads();
      if (gamepads.length === 1) {
        const gamepad = gamepads[0];
        const gp_state = {
          x: gamepad.buttons[0].pressed,
          o: gamepad.buttons[1].pressed,
          s: gamepad.buttons[2].pressed,
          t: gamepad.buttons[3].pressed,
          rt: gamepad.buttons[7].value,
          lt: gamepad.buttons[6].value,
          rsh: gamepad.axes[2],
          rsv: gamepad.axes[3],
          lsh: gamepad.axes[0],
          lsv: gamepad.axes[1]
        };
        fetch("/gamepad_states", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(gp_state),
        });
      }
    }, 15);

    return () => clearInterval(intervalId);
  }, []);
}

export default GamepadController;
