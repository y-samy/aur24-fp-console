// MapDisplay.js
import React, { useState } from 'react';
import '../Styles/MapDisplay.css';
import BoxesDisplay from './BoxesDisplay';
import DestinationDisplay from './DestinationDisplay';
const MapDisplay = ({robotPosition1 , boxPosition}) => {
  console.log(boxPosition);
  const [robotPosition, setRobotPosition] = useState({});
  const xPosition = (robotPosition1.x / 3.2) * 100;
  const yPosition = (robotPosition1.y / 3.2) * 100;
  const [boxesPosition, setBoxesPosition] = useState([{ x: 0, y:0 }]);
  const [destinationPosition, setDestinationPosition] = useState([]);
  console.log("destination"+destinationPosition);
  const handleSubmit = () =>{
    setDestinationPosition(prevData => [...prevData, boxPosition]);
  }
  return (<>
    <button onClick={handleSubmit}>
    destination
  </button>
    <div className="map-container">
      <div className="map">
        <div className="robot" style={{ left: `${xPosition}%`, bottom: `${yPosition}%` }}></div>
        {/* <BoxesDisplay boxesPosition={boxesPosition} /> */}
        {/* <DestinationDisplay destinationPosition ={destinationPosition}/> */}

      </div>
    </div>
    </>
  );
};

export default MapDisplay;
