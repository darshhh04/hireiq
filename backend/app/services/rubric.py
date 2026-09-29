from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]     
RUBRIC_DIR = BASE_DIR / "rubrics"
PROMPT_FILE = BASE_DIR / "prompts" / "evaluation.txt"

def load_rubric(question_type: str) -> dict:
    path = RUBRIC_DIR / f"{question_type}.yaml"
    if not path.exists():
        path = RUBRIC_DIR / "technical.yaml"
    with open(path) as f:
        return yaml.safe_load(f)

def rubric_to_text(rubric: dict) -> str:
    lines = []
    for c in rubric["criteria"]:
        lines.append(
            f"- {c['name']} (weight {c['weight']}): {c['description']} "
            f"Strong: {c['strong']} Weak: {c['weak']}"
        )
    return "\n".join(lines)