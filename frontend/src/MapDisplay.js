// MapDisplay.js
import React from 'react';
import './MapDisplay.css';

const MapDisplay = ({ robotPosition }) => {
  const xPosition = (robotPosition.x / 3.2) * 100; 
  const yPosition = (robotPosition.y / 3.2) * 100;

  return (
    <div className="map-container">
      <div className="map">
        <div className="robot" style={{ left: `${xPosition}%`, bottom: `${yPosition}%` }}></div>
      </div>
    </div>
  );
};

export default MapDisplay;
