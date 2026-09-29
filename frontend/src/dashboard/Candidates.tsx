import { useEffect, useState } from "react";
import { api } from "../api";
import SessionDetail from "./SessionDetail";

interface Item {
  session_id: number; candidate: string; email: string; interview: string;
  status: string; score: number | null; recommendation: string;
}

export default function Candidates() {
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState("recent");
  const [data, setData] = useState<{ total: number; page_size: number; items: Item[] } | null>(null);
  const [selected, setSelected] = useState<number | null>(null);

  useEffect(() => {
    api.sessions(page, sort).then(setData).catch(() => alert("Failed to load candidates"));
  }, [page, sort]);

  if (selected !== null) return <SessionDetail id={selected} onBack={() => setSelected(null)} />;
  if (!data) return <p>Loading...</p>;
  const pages = Math.max(1, Math.ceil(data.total / data.page_size));

  return (
    <div>
      <label>
        Sort:{" "}
        <select value={sort} onChange={(e) => { setSort(e.target.value); setPage(1); }}>
          <option value="recent">Most recent</option>
          <option value="score">Highest score</option>
        </select>
      </label>
      <table>
        <thead>
          <tr><th>Candidate</th><th>Interview</th><th>Score</th><th>Recommendation</th><th>Status</th><th></th></tr>
        </thead>
        <tbody>
          {data.items.map((s) => (
            <tr key={s.session_id}>
              <td>{s.candidate}<br /><small>{s.email}</small></td>
              <td>{s.interview}</td>
              <td>
                {s.score ?? "-"}
                {s.score !== null && <div className="bar"><div style={{ width: `${s.score}%` }} /></div>}
              </td>
              <td><span className={`badge ${s.recommendation.toLowerCase()}`}>{s.recommendation}</span></td>
              <td>{s.status}</td>
              <td><button onClick={() => setSelected(s.session_id)}>View</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pager">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Prev</button>
        <span>Page {page} of {pages}</span>
        <button disabled={page >= pages} onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </div>
  );
}