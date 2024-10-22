import React, { useState, useEffect } from "react";
import "./App.css";
import { io } from 'socket.io-client';
import MapDisplay from './MapDisplay'; 
const socketIo = io('http://localhost:5000');

const App = () => {
  const [scanningData, setScanningData] = useState([]);
  const [robotPosition, setRobotPosition] = useState({ x: 0, y: 0 }); 
  useEffect(() => {
    socketIo.on("connect", () => {
      console.log("Connected to Socket.IO server");
    });

    socketIo.on("scanning_toggled", (data) => {
      console.log("Message from server:", data.status);
    });

    // Listening for localization data
    socketIo.on("localization_data", (data) => {
      // Assuming data contains x and y properties
      setRobotPosition({ x: data.x, y: data.y });
    });

    return () => {
      socketIo.disconnect();
    };
  }, []);

  const handleScan = () => {
    socketIo.emit("toggle_scanning");
  };

  return (
    <>
      <div className="app-container">
        <div className="sidebar">
          <h3>Scanned Data:</h3>
          <ul>
            {scanningData.map((item, index) => (
              <li key={index}>{item}</li>
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
            <button>
              Turn off
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
        </div>
      </div>
    </>
  );
};

export default App;
