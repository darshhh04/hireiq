from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rubric_file = Column(String)            # path to YAML rubric
    time_limit_sec = Column(Integer, default=120)
    created_at = Column(DateTime, default=datetime.utcnow)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(String, default="technical")  # technical / behavioral
    order_index = Column(Integer, default=0)

class InterviewSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    status = Column(String, default="in_progress")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    transcript = Column(Text)
    status = Column(String, default="pending")  # pending/transcribing/done/failed
    duration_sec = Column(Float)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    overall_score = Column(Float)
    criteria_scores = Column(JSON)
    feedback = Column(Text)
    sentiment = Column(Float)
    confidence_score = Column(Float)
    keywords = Column(JSON)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    overall_score = Column(Float)
    recommendation = Column(String)   # Proceed / Hold / Reject
    pdf_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)