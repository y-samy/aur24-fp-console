import React from 'react';
import '../Styles/BoxesDisplay.css';
const BoxesDisplay = ({ boxesPosition }) => {
  return (
    <>
      {boxesPosition.map((box, index) => (
        <div 
          key={index}
          className="box"
          style={{
            left: `${(box.x / 3.2) * 100}%`,
            bottom: `${(box.y / 3.2) * 100}%`
          }}
        ></div>
      ))}
    </>
  );
};

export default BoxesDisplay;
