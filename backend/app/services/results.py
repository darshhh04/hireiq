from pathlib import Path
import yaml
from sqlalchemy.orm import Session
from app import models

REC_FILE = Path(__file__).resolve().parents[2] / "rubrics" / "recommendation.yaml"

def session_rows(db: Session, session_id: int) -> list[dict]:
    rows = (
        db.query(models.Response, models.Question, models.Evaluation)
        .join(models.Question, models.Response.question_id == models.Question.id)
        .outerjoin(models.Evaluation, models.Evaluation.response_id == models.Response.id)
        .filter(models.Response.session_id == session_id)
        .order_by(models.Question.order_index)
        .all()
    )
    return [
        {
            "response_id": r.id,
            "question": q.text,
            "status": r.status,
            "transcript": r.transcript,
            "segments": r.segments,
            "score": e.overall_score if e else None,
            "criteria_scores": e.criteria_scores if e else None,
            "feedback": e.feedback if e else None,
            "sentiment": e.sentiment if e else None,
            "confidence": e.confidence_score if e else None,
            "keywords": e.keywords if e else None,
        }
        for r, q, e in rows
    ]

def summarize(rows: list[dict]):
    scored = [r for r in rows if r["score"] is not None]
    if not scored:
        return None, {}
    overall = round(sum(r["score"] for r in scored) / len(scored), 1)
    per_criterion: dict[str, list[float]] = {}
    for r in scored:
        for name, s in (r["criteria_scores"] or {}).items():
            per_criterion.setdefault(name, []).append(s)
    radar = {n: round(sum(v) / len(v), 1) for n, v in per_criterion.items()}
    return overall, radar

def recommend(overall) -> str:
    if overall is None:
        return "Pending"
    cfg = yaml.safe_load(REC_FILE.read_text())
    if overall >= cfg["proceed_min"]:
        return "Proceed"
    if overall >= cfg["hold_min"]:
        return "Hold"
    return "Reject"