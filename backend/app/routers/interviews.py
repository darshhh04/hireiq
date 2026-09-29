import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()


AUDIO_DIR = "/tmp/hireiq_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

class SessionStart(BaseModel):
    interview_id: int
    name: str
    email: str

@router.get("/interviews/{interview_id}/questions")
def get_questions(interview_id: int, db: Session = Depends(get_db)):
    interview = db.get(models.Interview, interview_id)
    if not interview:
        raise HTTPException(404, "Interview not found")
    questions = (db.query(models.Question)
                 .filter_by(interview_id=interview_id)
                 .order_by(models.Question.order_index).all())
    return {
        "title": interview.title,
        "time_limit_sec": interview.time_limit_sec,
        "questions": [
            {"id": q.id, "text": q.text, "question_type": q.question_type}
            for q in questions
        ],
    }

@router.post("/sessions")
def start_session(body: SessionStart, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter_by(email=body.email).first()
    if not candidate:
        candidate = models.Candidate(name=body.name, email=body.email)
        db.add(candidate)
        db.flush()
    session = models.InterviewSession(
        interview_id=body.interview_id, candidate_id=candidate.id
    )
    db.add(session)
    db.commit()
    return {"session_id": session.id}

@router.post("/sessions/{session_id}/responses")
def upload_response(
    session_id: int,
    question_id: int = Form(...),
    duration_sec: float = Form(0),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    response = models.Response(
        session_id=session_id, question_id=question_id,
        duration_sec=duration_sec, status="pending",
    )
    db.add(response)
    db.commit()
    with open(os.path.join(AUDIO_DIR, f"{response.id}.webm"), "wb") as f:
        f.write(audio.file.read())
    return {"response_id": response.id, "status": "pending"}

@router.post("/sessions/{session_id}/complete")
def complete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(models.InterviewSession, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    session.status = "completed"
    session.completed_at = datetime.utcnow()
    db.commit()
    return {"status": "completed"}