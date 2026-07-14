import re
import ssl
import whisper
from pathlib import Path

# Some networks use SSL inspection proxies with self-signed certs which block
# the Whisper model download. This allows the download to proceed.
ssl._create_default_https_context = ssl._create_unverified_context

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


PARAGRAPH_GAP = 1.5  # seconds of silence before starting a new paragraph


def build_paragraphs(segments: list, gap: float = PARAGRAPH_GAP) -> str:
    paragraphs = []
    current = []
    for i, seg in enumerate(segments):
        current.append(seg["text"].strip())
        if i + 1 < len(segments):
            pause = segments[i + 1]["start"] - seg["end"]
            if pause >= gap:
                paragraphs.append(" ".join(current))
                current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def transcribe_file(path: Path, model_name: str = "base") -> str:
    if model_name not in _model_cache:
        _model_cache[model_name] = whisper.load_model(model_name)
    model = _model_cache[model_name]
    result = model.transcribe(str(path))
    text = build_paragraphs(result["segments"])
    return remove_fillers(text)
