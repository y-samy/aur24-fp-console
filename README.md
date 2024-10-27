# aur-fp24-software

AU Robotics 2024 Final Project

## Setup

### The backend

Set up the virtual environment

```sh
python -m venv flask-venv
```

Activate the environment


Windows
```sh
./flask-venv/Scripts/activate
```
Linux
```sh
chmod +x ./flask-venv/bin/activate
./flask-venv/bin/activate
```

Install the dependencies

```sh
pip install ./backend/requirements.txt
```

Running the flask server

```sh
python ./backend/main.py
```
### The MQTT Broker
https://mosquitto.org/download/

To run the broker:
```sh
mosquitto -c ./mqtt/mosquitto.conf
```

### The frontend

Dependencies
```sh
cd ./frontend
npm install
```
Run
```sh
cd ./frontend
npm start
```

## Gamepad controls
**Controller Commands**
* L2 = B6 -> back
* R2 = B7 -> fwd
* B0, B1 : x, o
* B2, B3: sqr, tri
* Axes: +ve right, down
* 0, 1: lStick, h, v
* 2, 3: rStick, h, v
