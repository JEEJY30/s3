import React, { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: "center", fontFamily: "sans-serif", marginTop: "80px" }}>
      <h1>S3 Static Hosting Demo</h1>
      <p>This React app is hosted on Amazon S3.</p>
      <button
        onClick={() => setCount(count + 1)}
        style={{ fontSize: "1.2rem", padding: "10px 24px", cursor: "pointer" }}
      >
        Clicked {count} times
      </button>
    </div>
  );
}

export default App;
