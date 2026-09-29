from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routers import interviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HireIQ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interviews.router)

@app.get("/health")
def health():
    return {"status": "ok"}