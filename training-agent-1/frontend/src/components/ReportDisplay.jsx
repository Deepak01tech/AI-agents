import React from "react";

function ReportDisplay({ result }) {

  if (!result) return null;

  return (
    <div>

      <h2>Tasks</h2>
      <p>{result.tasks}</p>

      <h2>Project</h2>
      <p>{result.project}</p>

      <h2>Evaluation</h2>
      <p>{result.evaluation}</p>

      <h2>Improvement Plan</h2>
      <p>{result.plan}</p>

    </div>
  );
}

export default ReportDisplay;