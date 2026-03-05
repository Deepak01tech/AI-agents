import React from "react";

function TopicDisplay({ topic }) {

  if (!topic) return null;

  return (
    <div>
      <h2>Weekly Topic</h2>
      <p>{topic}</p>
    </div>
  );
}

export default TopicDisplay;