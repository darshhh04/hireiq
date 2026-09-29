const API = "http://localhost:8000";

export interface Question { id: number; text: string; question_type: string }
export interface InterviewData {
  title: string;
  time_limit_sec: number;
  questions: Question[];
}

export async function getQuestions(interviewId: number): Promise<InterviewData> {
  const r = await fetch(`${API}/interviews/${interviewId}/questions`);
  if (!r.ok) throw new Error("Failed to load questions");
  return r.json();
}

export async function startSession(interviewId: number, name: string, email: string): Promise<number> {
  const r = await fetch(`${API}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ interview_id: interviewId, name, email }),
  });
  if (!r.ok) throw new Error("Failed to start session");
  return (await r.json()).session_id;
}

export async function uploadResponse(sessionId: number, questionId: number, duration: number, audio: Blob) {
  const form = new FormData();
  form.append("question_id", String(questionId));
  form.append("duration_sec", String(duration));
  form.append("audio", audio, "answer.webm");
  const r = await fetch(`${API}/sessions/${sessionId}/responses`, { method: "POST", body: form });
  if (!r.ok) throw new Error("Upload failed");
}

export async function completeSession(sessionId: number) {
  await fetch(`${API}/sessions/${sessionId}/complete`, { method: "POST" });
}