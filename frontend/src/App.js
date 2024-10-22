import React, { useState, useEffect } from "react";
import GamepadController from './Controller.js';
import "./App.css";
import { io } from 'socket.io-client';
import MapDisplay from './MapDisplay'; 

const socketIo = io('http://localhost:5000');

const App = () => {
  const [scanningData, setScanningData] = useState([]);
  const [robotPosition, setRobotPosition] = useState({ x: 0, y: 0 }); 
  const [connectionMessage, setConnectionMessage] = useState(""); 

  useEffect(() => {
    socketIo.on("connect", () => {
      console.log("Connected to Socket.IO server");
    });

    socketIo.on("connected", (data) => { 
      setConnectionMessage(data.message); 
      console.log("Message from server:", data.message);
    });

    socketIo.on("scanning_toggled", (data) => {
      console.log("Message from server:", data.status);
    });

    socketIo.on("localization_data", (data) => {
      setRobotPosition({ x: data.x, y: data.y });
    });

    // Listen for new scanned data
    socketIo.on("new_scanned_data", (data) => {
      console.log("New scanned data:", data.coords);
      // Update the scanningData state with the new coordinates
      setScanningData(prevData => [...prevData, data.coords]);
    });

    // Cleanup on unmount
    return () => {
      socketIo.off("connect");
      socketIo.off("connected");
      socketIo.off("scanning_toggled");
      socketIo.off("localization_data");
      socketIo.off("new_scanned_data");
      socketIo.disconnect();
    };
  }, []);

  const handleScan = () => {
    socketIo.emit("toggle_scanning");
    console.log("Scanning toggled");
  };

  const requestLocalizationData = () => {
    socketIo.emit("request_localization_data");
  };

  return (
    <>
      <div className="app-container">
        <div className="sidebar">
          <h3>Scanned Data:</h3>
          <ul>
            {scanningData.map((item, index) => (
              <li key={index}>{`X: ${item.X}, Y: ${item.Y}`}</li> // Display formatted data
            ))}
          </ul>
        </div>
        <div className="content">
          <h1 className="centered-h1">Live Cam</h1>
          <div className="frame centered">
            <img
              src="/video/feed"
              alt="Video"
            />
          </div>
          <div className="controls">
            <button onClick={requestLocalizationData}>
              Get Localization Data
            </button>
            <button onClick={handleScan}>
              Fast scan
            </button>
            <button>
              Tilt scan
            </button>
            <button>
              Deep Scan
            </button>
          </div>
          <h1>Robot Position</h1>
          <MapDisplay robotPosition={robotPosition} />
          <div className="connection-message">
            {connectionMessage} {/* Display connection message */}
          </div>
        </div>
      </div>
      <GamepadController />
    </>
  );
};

export default App;
