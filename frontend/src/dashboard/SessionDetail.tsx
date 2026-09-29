import { useEffect, useState } from "react";
import { api } from "../api";

interface Seg { start: number; end: number; text: string }
interface Resp {
  response_id: number; question: string; status: string; transcript: string | null;
  segments: Seg[] | null; score: number | null; feedback: string | null;
  sentiment: number | null; confidence: number | null;
  keywords: { keywords: string[] } | null;
}
interface Detail {
  candidate: string; email: string; interview: string; overall_score: number | null;
  recommendation: string; radar: Record<string, number>; responses: Resp[];
}

const fmt = (t: number) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}`;

export default function SessionDetail({ id, onBack }: { id: number; onBack: () => void }) {
  const [d, setD] = useState<Detail | null>(null);

  useEffect(() => {
    api.sessionDetail(id).then(setD).catch(() => alert("Failed to load session"));
  }, [id]);

  if (!d) return <p>Loading...</p>;

  return (
    <div>
      <button onClick={onBack}>Back</button>
      <h2>{d.candidate} <small>({d.email})</small></h2>
      <p>{d.interview}</p>
      <p>
        Overall: <b>{d.overall_score ?? "-"}</b> / 100{" "}
        <span className={`badge ${d.recommendation.toLowerCase()}`}>{d.recommendation}</span>
      </p>
      <a className="btn" href={api.reportUrl(id)}>Download PDF report</a>

      <h3>Skill dimensions (0-10)</h3>
      {Object.entries(d.radar).map(([k, v]) => (
        <div key={k} className="dim">
          <span>{k.replace(/_/g, " ")}</span>
          <div className="bar"><div style={{ width: `${v * 10}%` }} /></div>
          <b>{v}</b>
        </div>
      ))}

      <h3>Responses</h3>
      {d.responses.map((r) => (
        <div key={r.response_id} className="resp">
          <h4>{r.question}</h4>
          <p>Status: {r.status} · Score: {r.score ?? "-"} · Confidence: {r.confidence ?? "-"} · Sentiment: {r.sentiment ?? "-"}</p>
          {r.feedback && <p><i>{r.feedback}</i></p>}
          {r.keywords && <p>Keywords: {r.keywords.keywords.join(", ")}</p>}
          <div className="transcript">
            {r.segments?.length
              ? r.segments.map((s, i) => <p key={i}><code>{fmt(s.start)}</code> {s.text}</p>)
              : <p>{r.transcript ?? "(no transcript yet)"}</p>}
          </div>
        </div>
      ))}
    </div>
  );
}