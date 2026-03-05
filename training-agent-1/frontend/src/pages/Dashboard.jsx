// import React, { useState } from "react";
// import { runTraining } from "../api/api";
// import CodeInput from "../components/CodeInput";
// import TopicDisplay from "../components/TopicDisplay";
// import ReportDisplay from "../components/ReportDisplay";

// function Dashboard() {

//   const [code, setCode] = useState("");
//   const [result, setResult] = useState(null);

//   const submitCode = async () => {

//     const response = await runTraining({
//       level: "beginner",
//       submission: code
//     });

//     setResult(response.data);
//   };

//   return (

//     <div style={{ padding: "30px" }}>

//       <h1>AI Python Training Agent</h1>

//       <CodeInput code={code} setCode={setCode} />

//       <br />

//       <button onClick={submitCode}>
//         Submit Code
//       </button>

//       <TopicDisplay topic={result?.topic} />

//       <ReportDisplay result={result} />

//     </div>
//   );
// }

// export default Dashboard;