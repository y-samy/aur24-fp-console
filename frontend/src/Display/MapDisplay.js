// MapDisplay.js
import React, { useState } from 'react';
import '../Styles/MapDisplay.css';
import BoxesDisplay from './BoxesDisplay';
import DestinationDisplay from './DestinationDisplay';
const MapDisplay = () => {

  const [robotPosition, setRobotPosition] = useState({ x: 0, y: 0 });

  const xPosition = (robotPosition.x / 3.2) * 100;
  const yPosition = (robotPosition.y / 3.2) * 100;
  const [boxesPosition, setBoxesPosition] = useState([{ x: 0, y:0 }]);
  const [destinationPosition, setDestinationPosition] = useState([{x: 2 , y : 2}]);
  return (
    <div className="map-container">
      <div className="map">
        <div className="robot" style={{ left: `${xPosition}%`, bottom: `${yPosition}%` }}></div>
        <BoxesDisplay boxesPosition={boxesPosition} />
        <DestinationDisplay destinationPosition ={destinationPosition}/>
      </div>
    </div>
  );
};

export default MapDisplay;
