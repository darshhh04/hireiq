import { useEffect, useRef, useState } from "react";
import { uploadResponse, completeSession, type InterviewData } from "./api";
import { useRecorder } from "./useRecorder";

interface Props {
  sessionId: number;
  data: InterviewData;
  onFinish: () => void;
}

export default function InterviewSession({ sessionId, data, onFinish }: Props) {
  const [index, setIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(data.time_limit_sec);
  const [busy, setBusy] = useState(false);
  const { recording, start, stop } = useRecorder();
  const startedAt = useRef(0);
  const question = data.questions[index];
  const isLast = index + 1 === data.questions.length;

  async function begin() {
    try {
      await start();
      startedAt.current = Date.now();
    } catch {
      alert("Microphone access is required to take the interview.");
    }
  }

  async function submit() {
    if (busy) return;
    setBusy(true);
    const duration = (Date.now() - startedAt.current) / 1000;
    const blob = await stop();
    await uploadResponse(sessionId, question.id, duration, blob);
    if (isLast) {
      await completeSession(sessionId);
      onFinish();
    } else {
      setIndex(index + 1);
      setSecondsLeft(data.time_limit_sec);
      setBusy(false);
    }
  }

  useEffect(() => {
    if (!recording) return;
    if (secondsLeft <= 0) {
      submit();
      return;
    }
    const t = setTimeout(() => setSecondsLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [recording, secondsLeft]);

  const mm = Math.floor(secondsLeft / 60);
  const ss = String(secondsLeft % 60).padStart(2, "0");

  return (
    <div className="card">
      <p>Question {index + 1} of {data.questions.length}</p>
      <h2>{question.text}</h2>
      <p className="timer">{mm}:{ss}</p>
      {!recording && !busy && <button onClick={begin}>Start Answer</button>}
      {recording && <button onClick={submit}>{isLast ? "Submit and Finish" : "Submit Answer"}</button>}
      {busy && <p>Uploading...</p>}
    </div>
  );
}