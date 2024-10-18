import React, { useState } from "react";

const App = () => {
function handleClick() {
  fetch("/video/toggle_scanning")
}

return (
  <>
  <div class="centered">
   <img
    src="/video/feed"
    alt="Video"
   />
  </div>
  <button onClick={handleClick}>
  Turn on scanning
  </button>
  </>
 );
};



export default App;