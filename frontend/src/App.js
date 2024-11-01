import React, { useState, useEffect } from "react";
import GamepadController from './Controller.js';
import "./App.css";
import { socket } from './socket';
import MapDisplay from './Display/MapDisplay.js'; 


const App = () => {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [robotPosition, setRobotPosition] = useState({}); 
  const [scanningData, setScanningData] = useState([]);
  useEffect(() => {
    function onConnect() {
      setIsConnected(true);
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    function onNewBox(coords){
        setScanningData(prevData => [...prevData, coords]);
    }
    function onRobotCoords(coords) {
      setRobotPosition({ x: coords.X, y: coords.Y });
    }
    socket.on('connect', onConnect);
    socket.on('new box', onNewBox);
    socket.on('robot coords', onRobotCoords)
    socket.on('disconnect', onDisconnect);

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('new box', onNewBox);
      socket.off('robot coords', onRobotCoords);
    };
  }, []);

 const ScanOff = () =>{
  fetch("/video/configure_scanning/off");
 }
 const ScanFast = () =>{
  fetch("/video/configure_scanning/pyzbar")
 }
 const ScanTilt = () => {
  fetch("/video/configure_scanning/cv")
 }
 const ScanDeep = () => {
  fetch("/video/configure_scanning/qreader")
 }
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
            <button onClick={ScanOff}>
              ScanOff
            </button>
            <button onClick={ScanFast}>
              Fast scan
            </button>
            <button onClick={ScanTilt}>
              Tilt scan
            </button>
            <button onClick={ScanDeep}>
              Deep Scan
            </button>
          </div>
          <h1>Robot Position</h1>
          <MapDisplay robotPosition1={robotPosition} />
        </div>
      </div>
      <GamepadController />
    </>
  );
};

export default App;