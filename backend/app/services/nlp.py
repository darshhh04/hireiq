import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_nlp = None
_vader = SentimentIntensityAnalyzer()

FILLERS = ["um", "uh", "like", "basically", "actually", "you know"]
HEDGES = ["i guess", "maybe", "sort of", "kind of", "i think", "not sure"]

def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def confidence_score(transcript: str, duration_sec: float) -> float:
    words = transcript.lower().split()
    n = len(words)
    if n == 0:
        return 0.0
    text = f" {transcript.lower()} "
    hits = sum(text.count(f" {f} ") for f in FILLERS) + sum(text.count(h) for h in HEDGES)
    score = 100 - min(60, (hits / n) * 300)
    if duration_sec:
        wpm = n / duration_sec * 60
        if wpm < 90 or wpm > 190:
            score -= 15
    if n < 20:
        score -= 15
    return max(0.0, round(score, 1))

def analyze_text(transcript: str, duration_sec: float) -> dict:
    doc = _get_nlp()(transcript or "")
    keywords = list(dict.fromkeys(
        t.lemma_.lower() for t in doc
        if t.pos_ in ("NOUN", "PROPN") and not t.is_stop and len(t.text) > 2
    ))[:10]
    entities = [{"text": e.text, "label": e.label_} for e in doc.ents]
    return {
        "sentiment": _vader.polarity_scores(transcript or "")["compound"],
        "confidence": confidence_score(transcript or "", duration_sec or 0),
        "keywords": {"keywords": keywords, "entities": entities},
    }