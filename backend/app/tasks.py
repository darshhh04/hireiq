import os
import tempfile
from app.celery_app import celery
from app.database import SessionLocal
from app import models
from app.services.audio import normalize_and_chunk
from app.services.transcription import transcribe_chunks

AUDIO_DIR = "/tmp/hireiq_audio"

def _delete(path: str):
    if os.path.exists(path):
        os.remove(path)

@celery.task(bind=True, max_retries=3)
def transcribe_response(self, response_id: int):
    db = SessionLocal()
    path = os.path.join(AUDIO_DIR, f"{response_id}.webm")
    try:
        response = db.get(models.Response, response_id)
        response.status = "transcribing"
        db.commit()

        with tempfile.TemporaryDirectory() as tmp:
            chunks = normalize_and_chunk(path, tmp)
            text, segments = transcribe_chunks(chunks)

        response.transcript = text
        response.segments = segments
        response.status = "done"
        db.commit()
        _delete(path)
    except Exception as exc:
        db.rollback()
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=5 * (2 ** self.request.retries))
        response = db.get(models.Response, response_id)
        response.status = "failed"
        db.commit()
        _delete(path)
    finally:
        db.close()