import { useState } from "react";
import Candidates from "./dashboard/Candidates";
import Interviews from "./dashboard/Interviews";
import Rubrics from "./dashboard/Rubrics";

const tabs = ["Candidates", "Interviews", "Rubrics"] as const;

export default function Admin() {
  const [tab, setTab] = useState<(typeof tabs)[number]>("Candidates");
  return (
    <div className="wide">
      <h1>HireIQ Dashboard</h1>
      <div className="tabs">
        {tabs.map((t) => (
          <button key={t} className={t === tab ? "active" : ""} onClick={() => setTab(t)}>{t}</button>
        ))}
      </div>
      {tab === "Candidates" && <Candidates />}
      {tab === "Interviews" && <Interviews />}
      {tab === "Rubrics" && <Rubrics />}
    </div>
  );
}