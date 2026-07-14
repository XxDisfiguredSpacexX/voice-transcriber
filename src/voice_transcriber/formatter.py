from datetime import datetime
from pathlib import Path


def write_note(text: str, audio_path: Path, output_path: Path) -> Path:
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M")
    stem = audio_path.stem

    # Colons are invalid in macOS filenames when the file is synced
    safe_datetime = datetime_str.replace(":", "-")
    filename = f"{safe_datetime} - {stem}.md"

    content = f"""---
created: {datetime_str}
tags:
  - voice-note
source: {audio_path.name}
---

# {datetime_str} - {stem}

{text}
"""

    note_path = output_path / filename
    note_path.write_text(content, encoding="utf-8")
    return note_path
