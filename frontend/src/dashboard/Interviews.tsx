import { useEffect, useState } from "react";
import { api } from "../api";

interface Q { id: number; text: string; question_type: string }
interface Interview { id: number; title: string; time_limit_sec: number; questions: Q[] }

export default function Interviews() {
  const [list, setList] = useState<Interview[]>([]);
  const [rubrics, setRubrics] = useState<string[]>([]);
  const [title, setTitle] = useState("");
  const [timer, setTimer] = useState(120);
  const [qText, setQText] = useState<Record<number, string>>({});
  const [qType, setQType] = useState<Record<number, string>>({});

  const load = () => {
    api.interviews().then(setList);
    api.rubrics().then(setRubrics);
  };
  useEffect(load, []);

  async function create() {
    await api.createInterview(title, timer);
    setTitle("");
    load();
  }

  async function add(id: number) {
    if (!qText[id]) return;
    try {
      await api.addQuestion(id, qText[id], qType[id] || rubrics[0]);
      setQText({ ...qText, [id]: "" });
      load();
    } catch (e) {
      alert((e as Error).message);
    }
  }

  async function remove(id: number) {
    try {
      await api.deleteQuestion(id);
      load();
    } catch (e) {
      alert((e as Error).message);
    }
  }

  return (
    <div>
      <h3>New interview</h3>
      <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />{" "}
      <input type="number" value={timer} onChange={(e) => setTimer(Number(e.target.value))} /> sec per question{" "}
      <button disabled={!title} onClick={create}>Create</button>

      {list.map((i) => (
        <div key={i.id} className="resp">
          <h4>#{i.id} {i.title} <small>({i.time_limit_sec}s per question)</small></h4>
          <p>Candidate link: <code>{`${window.location.origin}/?interview=${i.id}`}</code></p>
          <ol>
            {i.questions.map((q) => (
              <li key={q.id}>
                {q.text} <small>[{q.question_type}]</small>{" "}
                <button onClick={() => remove(q.id)}>Delete</button>
              </li>
            ))}
          </ol>
          <input placeholder="New question" value={qText[i.id] ?? ""}
                 onChange={(e) => setQText({ ...qText, [i.id]: e.target.value })} />{" "}
          <select value={qType[i.id] ?? rubrics[0] ?? ""}
                  onChange={(e) => setQType({ ...qType, [i.id]: e.target.value })}>
            {rubrics.map((r) => <option key={r} value={r}>{r}</option>)}
          </select>{" "}
          <button onClick={() => add(i.id)}>Add</button>
        </div>
      ))}
    </div>
  );
}