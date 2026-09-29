import { useEffect, useState } from "react";
import { api } from "../api";

export default function Rubrics() {
  const [names, setNames] = useState<string[]>([]);
  const [current, setCurrent] = useState("");
  const [text, setText] = useState("");

  async function openRubric(name: string) {
    setCurrent(name);
    const r = await api.rubric(name);
    setText(r.yaml_text);
  }

  useEffect(() => {
    api.rubrics().then((n: string[]) => {
      setNames(n);
      if (n.length) openRubric(n[0]);
    });
  }, []);

  async function save() {
    try {
      await api.saveRubric(current, text);
      alert("Rubric saved");
    } catch (e) {
      alert((e as Error).message);
    }
  }

  return (
    <div>
      <p>Rubrics are applied by question type. Changes affect new evaluations only.</p>
      <select value={current} onChange={(e) => openRubric(e.target.value)}>
        {names.map((n) => <option key={n} value={n}>{n}</option>)}
      </select>
      <textarea rows={22} value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={save}>Save rubric</button>
    </div>
  );
}