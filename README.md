# aur-fp24-console

AU Robotics 2024 Final Project Console - a React + Flask console for monitoring and controlling the robot

# Contributing

### The backend

Set up the virtual environment

```sh
python -m venv flask-venv
```

Activate the environment

```sh
./flask-venv/Scripts/activate
```

Install the dependencies

```sh
pip install ./requirements.txt
```

Running the flask server

```sh
python ./backend/main.py
```
**Controller Commands**
* B6 ==> back
* B7  ==> fwd
* B0, B1 : x, o
* B2, B3: sqr, tri
* Axes: +ve right, down
* 0, 1: lStick, h, v
* 2, 3: rStick, h, v
* navigator.getGamepads()[0].buttons[btnID].pressed -> bool
* navigator.getGamepads()[0].buttons[btnID].value -> 0-1f
* navigator.getGamepads()[0].axes -> array
