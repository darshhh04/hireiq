import re
import yaml
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.rubric import RUBRIC_DIR

router = APIRouter(prefix="/admin")
NAME_RE = re.compile(r"^[a-z_]{1,30}$")

class RubricBody(BaseModel):
    yaml_text: str

class InterviewBody(BaseModel):
    title: str
    time_limit_sec: int = 120

class QuestionBody(BaseModel):
    text: str
    question_type: str = "technical"

def _rubric_path(name: str):
    if not NAME_RE.match(name):
        raise HTTPException(400, "Invalid rubric name")
    return RUBRIC_DIR / f"{name}.yaml"

def _validate(data: dict):
    criteria = data["criteria"]
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("no criteria")
    for c in criteria:
        if not c["name"] or float(c["weight"]) <= 0:
            raise ValueError("bad criterion")
        for key in ("description", "strong", "weak"):
            if key not in c:
                raise ValueError(f"missing {key}")

@router.get("/rubrics")
def list_rubrics():
    return sorted(p.stem for p in RUBRIC_DIR.glob("*.yaml") if p.stem != "recommendation")

@router.get("/rubrics/{name}")
def get_rubric(name: str):
    path = _rubric_path(name)
    if not path.exists():
        raise HTTPException(404, "Rubric not found")
    return {"name": name, "yaml_text": path.read_text()}

@router.put("/rubrics/{name}")
def save_rubric(name: str, body: RubricBody):
    path = _rubric_path(name)
    try:
        _validate(yaml.safe_load(body.yaml_text))
    except Exception:
        raise HTTPException(
            422, "Invalid rubric: needs a 'criteria' list; each item needs name, weight > 0, "
                 "description, strong, weak")
    path.write_text(body.yaml_text)
    return {"saved": name}

@router.get("/interviews")
def list_interviews(db: Session = Depends(get_db)):
    out = []
    for i in db.query(models.Interview).order_by(models.Interview.id).all():
        qs = (db.query(models.Question).filter_by(interview_id=i.id)
              .order_by(models.Question.order_index).all())
        out.append({
            "id": i.id, "title": i.title, "time_limit_sec": i.time_limit_sec,
            "questions": [{"id": q.id, "text": q.text, "question_type": q.question_type} for q in qs],
        })
    return out

@router.post("/interviews")
def create_interview(body: InterviewBody, db: Session = Depends(get_db)):
    interview = models.Interview(title=body.title, time_limit_sec=body.time_limit_sec)
    db.add(interview)
    db.commit()
    return {"id": interview.id}

@router.post("/interviews/{interview_id}/questions")
def add_question(interview_id: int, body: QuestionBody, db: Session = Depends(get_db)):
    if not db.get(models.Interview, interview_id):
        raise HTTPException(404, "Interview not found")
    if not _rubric_path(body.question_type).exists():
        raise HTTPException(400, "Unknown question type (no rubric with that name)")
    next_index = db.query(func.coalesce(func.max(models.Question.order_index), -1)) \
                   .filter_by(interview_id=interview_id).scalar() + 1
    q = models.Question(interview_id=interview_id, text=body.text,
                        question_type=body.question_type, order_index=next_index)
    db.add(q)
    db.commit()
    return {"id": q.id}

@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    q = db.get(models.Question, question_id)
    if not q:
        raise HTTPException(404, "Question not found")
    if db.query(models.Response).filter_by(question_id=question_id).first():
        raise HTTPException(409, "This question already has responses and cannot be deleted")
    db.delete(q)
    db.commit()
    return {"deleted": question_id}