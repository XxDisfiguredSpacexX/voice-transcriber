import re
import whisper
from pathlib import Path

# Unambiguous spoken fillers — not content words like "like", "so", "actually"
FILLER_PATTERNS = [
    r"\bum+\b",
    r"\buh+\b",
    r"\buhh+\b",
    r"\bumm+\b",
    r"\bhmm+\b",
    r"\byou know,?\b",
    r"\bI mean,?\b",
]

_model_cache: dict = {}


def remove_fillers(text: str) -> str:
    for pattern in FILLER_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" ([,\.!?])", r"\1", text)
    return text.strip()


def transcribe_file(path: Path, model_name: str = "base") -> str:
    if model_name not in _model_cache:
        _model_cache[model_name] = whisper.load_model(model_name)
    model = _model_cache[model_name]
    result = model.transcribe(str(path))
    return remove_fillers(result["text"].strip())
