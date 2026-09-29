from app.database import SessionLocal
from app import models

db = SessionLocal()
if not db.query(models.Interview).first():
    interview = models.Interview(
        title="Python Backend Developer Interview",
        rubric_file="rubrics/technical.yaml",
        time_limit_sec=120,
    )
    db.add(interview)
    db.flush()
    questions = [
        ("Explain the difference between a list and a tuple in Python.", "technical"),
        ("What is a REST API and how does FastAPI help build one?", "technical"),
        ("Tell me about a time you resolved a conflict in a team.", "behavioral"),
    ]
    for i, (text, qtype) in enumerate(questions):
        db.add(models.Question(
            interview_id=interview.id, text=text,
            question_type=qtype, order_index=i,
        ))
    db.commit()
db.close()