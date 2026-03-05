import { useState } from "react";
import { submitTraining } from "../api/trainingApi";

function SubmissionForm() {
  const [level, setLevel] = useState("");
  const [submission, setSubmission] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      level: level,
      submission: submission,
    };

    try {
      const result = await submitTraining(data);
      setResponse(JSON.stringify(result));
    } catch (error) {
      console.error(error);
      setResponse("Error submitting data");
    }
  };

  return (
    <div>
      <h2>Training Submission</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Level</label>
          <input
            type="text"
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            placeholder="Enter level"
          />
        </div>

        <div>
          <label>Submission</label>
          <textarea
            value={submission}
            onChange={(e) => setSubmission(e.target.value)}
            placeholder="Enter submission"
          />
        </div>

        <button type="submit">Submit</button>
      </form>

      {response && (
        <div>
          <h3>Response</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default SubmissionForm;