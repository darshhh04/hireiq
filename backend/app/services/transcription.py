_model = None

def _get_model():
    global _model
    if _model is None:
        import whisper 
        _model = whisper.load_model("base")
    return _model

def transcribe_chunks(chunk_paths: list[str], chunk_sec: int = 60):
    model = _get_model()
    texts, segments = [], []
    for i, path in enumerate(chunk_paths):
        result = model.transcribe(path, fp16=False)
        texts.append(result["text"].strip())
        for s in result["segments"]:
            segments.append({
                "start": round(s["start"] + i * chunk_sec, 2),
                "end": round(s["end"] + i * chunk_sec, 2),
                "text": s["text"].strip(),
            })
    return " ".join(texts).strip(), segments