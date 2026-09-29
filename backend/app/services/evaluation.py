from google import genai
from pydantic import BaseModel, ValidationError, field_validator
from app.config import settings
from app.services.rubric import load_rubric, rubric_to_text, PROMPT_FILE

class CriterionScore(BaseModel):
    name: str
    score: float
    justification: str

    @field_validator("score")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(0.0, min(10.0, v))  

class EvaluationResult(BaseModel):
    criteria: list[CriterionScore]
    feedback: str

def evaluate_answer(question: str, question_type: str, transcript: str) -> dict:
    rubric = load_rubric(question_type)
    weights = {c["name"]: c["weight"] for c in rubric["criteria"]}

    if not transcript or not transcript.strip():
        return {"overall_score": 0.0,
                "criteria_scores": {n: 0.0 for n in weights},
                "feedback": "No answer was detected."}

    prompt = PROMPT_FILE.read_text().format(
        question_type=question_type,
        question=question,
        rubric=rubric_to_text(rubric),
        transcript=transcript,
    )
    client = genai.Client(api_key=settings.gemini_api_key)
    resp = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": EvaluationResult,
            "temperature": 0,
        },
    )

    try:  
        result = EvaluationResult.model_validate_json(resp.text)
    except ValidationError:
        raise ValueError("LLM response failed schema validation") from None

    scores = {c.name: c.score for c in result.criteria if c.name in weights}
    missing = set(weights) - set(scores)
    if missing:
        raise ValueError(f"LLM omitted criteria: {missing}")

    overall = sum(scores[n] * w for n, w in weights.items()) / sum(weights.values()) * 10
    return {
        "overall_score": round(overall, 1),          
        "criteria_scores": {n: scores[n] for n in weights},
        "feedback": result.feedback,
    }