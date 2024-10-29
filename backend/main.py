from api import socketio, app, mqttc

if __name__ == "__main__":
    try:
        mqttc.loop_start()
        socketio.run(app, host="0.0.0.0", port=5000, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        mqttc.disconnect()
        mqttc.loop_stop()