import React, { useState } from "react";

const App = () => {
function handleClick() {
  alert('You clicked me!');
}

return (
  <>
  <div class="centered">
   <img
    src="http://localhost:5000/video_feed"
    alt="Video"
   />
  </div>
  <button onClick={handleClick}>
  Click me
  </button>
  </>
 );
};



export default App;