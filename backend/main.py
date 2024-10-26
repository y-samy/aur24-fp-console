from api import socketio, app, mqtt_client
from mqtt_client import stop_mqtt

if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0", port=5000, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        stop_mqtt(mqtt_client)