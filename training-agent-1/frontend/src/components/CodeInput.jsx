import React from "react";

function CodeInput({ code, setCode }) {

  return (
    <div>

      <h3>Submit Python Code</h3>

      <textarea
        rows="10"
        cols="60"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your Python code"
      />

    </div>
  );
}

export default CodeInput;