# voice-transcriber

Watches a local folder for audio files and transcribes them into your Obsidian vault using [OpenAI Whisper](https://github.com/openai/whisper) — fully local, no API key, no cloud.

Filler words (`um`, `uh`, `you know`, `I mean`) are removed. Everything else is untouched.

---

## Prerequisites

**1. Python 3.9 or later**
Check with: `python3 --version`
Download from: https://www.python.org/downloads/

**2. ffmpeg** (required by Whisper to decode audio)

macOS:
```bash
brew install ffmpeg
```

Windows:
Download from https://ffmpeg.org/download.html and add to PATH.

Linux:
```bash
sudo apt install ffmpeg
```

**3. pipx**
```bash
pip install pipx
pipx ensurepath
```

---

## Install

```bash
pipx install git+https://github.com/YOUR_USERNAME/voice-transcriber
```

Or from a local copy:
```bash
pipx install /path/to/voice-transcriber
```

---

## Usage

### Watch a folder (recommended)

Keeps running in the background. Every time an audio file appears in `--input`, it gets transcribed and saved to `--output`.

```bash
voice-transcriber watch --input ~/Desktop/recordings --output ~/Documents/MyVault/Voice\ Notes
```

Supported formats: `.mp3`, `.aac`, `.wav`, `.m4a`

### Transcribe a single file

```bash
voice-transcriber transcribe ~/Desktop/meeting.mp3 --output ~/Documents/MyVault/Voice\ Notes
```

### Model sizes

The `--model` flag controls accuracy vs speed. Default is `base`.

| Model  | Size  | Speed  | Accuracy |
|--------|-------|--------|----------|
| tiny   | 75 MB | Fastest | Lower   |
| base   | 145 MB | Fast  | Good    |
| small  | 466 MB | Medium | Better  |
| medium | 1.5 GB | Slow  | Great   |
| large  | 2.9 GB | Slowest | Best  |

The model is downloaded automatically on first use.

---

## Output format

Each transcript is saved as a Markdown file:

```
2026-07-14 14-32 - my-recording.md
```

```markdown
---
created: 2026-07-14 14:32
tags:
  - voice-note
source: my-recording.mp3
---

# 2026-07-14 14:32 - my-recording

Transcript text here...
```

---

## Update

```bash
pipx upgrade voice-transcriber
```

## Uninstall

```bash
pipx uninstall voice-transcriber
```
