from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.results import recommend, session_rows, summarize
from app.services.report import generate_pdf

router = APIRouter(prefix="/dashboard")

@router.get("/sessions")
def list_sessions(page: int = 1, page_size: int = 10, sort: str = "recent",
                  db: Session = Depends(get_db)):
    page = max(page, 1)
    page_size = min(max(page_size, 1), 50)   # always paginated, never unbounded
    avg = (
        db.query(models.Response.session_id.label("sid"),
                 func.avg(models.Evaluation.overall_score).label("score"))
        .join(models.Evaluation, models.Evaluation.response_id == models.Response.id)
        .group_by(models.Response.session_id)
        .subquery()
    )
    q = (
        db.query(models.InterviewSession, models.Candidate, models.Interview, avg.c.score)
        .join(models.Candidate, models.InterviewSession.candidate_id == models.Candidate.id)
        .join(models.Interview, models.InterviewSession.interview_id == models.Interview.id)
        .outerjoin(avg, avg.c.sid == models.InterviewSession.id)
    )
    total = q.count()
    order = avg.c.score.desc().nullslast() if sort == "score" else models.InterviewSession.id.desc()
    rows = q.order_by(order).offset((page - 1) * page_size).limit(page_size).all()
    items = [
        {
            "session_id": s.id,
            "candidate": c.name,
            "email": c.email,
            "interview": i.title,
            "status": s.status,
            "score": round(score, 1) if score is not None else None,
            "recommendation": recommend(score),
        }
        for s, c, i, score in rows
    ]
    return {"total": total, "page": page, "page_size": page_size, "items": items}

@router.get("/sessions/{session_id}")
def session_detail(session_id: int, db: Session = Depends(get_db)):
    s = db.get(models.InterviewSession, session_id)
    if not s:
        raise HTTPException(404, "Session not found")
    c = db.get(models.Candidate, s.candidate_id)
    i = db.get(models.Interview, s.interview_id)
    rows = session_rows(db, session_id)
    overall, radar = summarize(rows)
    return {
        "candidate": c.name, "email": c.email, "interview": i.title, "status": s.status,
        "overall_score": overall, "recommendation": recommend(overall),
        "radar": radar, "responses": rows,
    }

@router.get("/sessions/{session_id}/report")
def download_report(session_id: int, db: Session = Depends(get_db)):
    if not db.get(models.InterviewSession, session_id):
        raise HTTPException(404, "Session not found")
    pdf = generate_pdf(db, session_id)
    return Response(
        content=pdf, media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="hireiq_report_{session_id}.pdf"'},
    )