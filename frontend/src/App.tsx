import { useState } from "react";
import InterviewSession from "./InterviewSession";
import { getQuestions, startSession, type InterviewData } from "./api";

const INTERVIEW_ID = Number(new URLSearchParams(window.location.search).get("interview")) || 1;

export default function App() {
  const [stage, setStage] = useState<"start" | "interview" | "done">("start");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [sessionId, setSessionId] = useState(0);
  const [data, setData] = useState<InterviewData | null>(null);

  async function begin() {
    try {
      const [d, id] = await Promise.all([
        getQuestions(INTERVIEW_ID),
        startSession(INTERVIEW_ID, name, email),
      ]);
      setData(d);
      setSessionId(id);
      setStage("interview");
    } catch {
      alert("Could not start the interview. Is the backend running?");
    }
  }

  if (stage === "interview" && data) {
    return <InterviewSession sessionId={sessionId} data={data} onFinish={() => setStage("done")} />;
  }

  if (stage === "done") {
    return (
      <div className="card">
        <h2>Thank you!</h2>
        <p>Your responses have been submitted.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h1>HireIQ Interview</h1>
      <input placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button disabled={!name || !email} onClick={begin}>Begin Interview</button>
    </div>
  );
}