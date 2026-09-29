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

const H = { "Content-Type": "application/json" };

async function j(r: Response) {
  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    throw new Error(body.detail || "Request failed");
  }
  return r.json();
}

export const api = {
  sessions: (page: number, sort: string) =>
    fetch(`${API}/dashboard/sessions?page=${page}&page_size=10&sort=${sort}`).then(j),
  sessionDetail: (id: number) => fetch(`${API}/dashboard/sessions/${id}`).then(j),
  reportUrl: (id: number) => `${API}/dashboard/sessions/${id}/report`,
  interviews: () => fetch(`${API}/admin/interviews`).then(j),
  createInterview: (title: string, time_limit_sec: number) =>
    fetch(`${API}/admin/interviews`, { method: "POST", headers: H, body: JSON.stringify({ title, time_limit_sec }) }).then(j),
  addQuestion: (interviewId: number, text: string, question_type: string) =>
    fetch(`${API}/admin/interviews/${interviewId}/questions`, { method: "POST", headers: H, body: JSON.stringify({ text, question_type }) }).then(j),
  deleteQuestion: (id: number) => fetch(`${API}/admin/questions/${id}`, { method: "DELETE" }).then(j),
  rubrics: () => fetch(`${API}/admin/rubrics`).then(j),
  rubric: (name: string) => fetch(`${API}/admin/rubrics/${name}`).then(j),
  saveRubric: (name: string, yaml_text: string) =>
    fetch(`${API}/admin/rubrics/${name}`, { method: "PUT", headers: H, body: JSON.stringify({ yaml_text }) }).then(j),
};