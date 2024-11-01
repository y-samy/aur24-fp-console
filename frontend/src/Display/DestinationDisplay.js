import React from 'react';

const DestinationDisplay = ({destinationPosition}) =>{
  console.log("destination"+destinationPosition);
  
  return (
    <>
      {destinationPosition.map((box, index) => (
        <div 
          key={index}
          className="box-destination"
          style={{
            left: `${(box.x / 3.2) * 100}%`,
            bottom: `${(box.y / 3.2) * 100}%`
          }}
        ></div>
      ))}
    </>
  );
}
export default DestinationDisplay;