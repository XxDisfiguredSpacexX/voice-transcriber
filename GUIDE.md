# How to Set Up Voice Transcriber on Your Mac

This tool watches a folder on your Mac. When you drop an audio file in, it automatically transcribes it and saves a note into your Obsidian vault.

---

## What You Need Before Starting

- A Mac running macOS
- An Obsidian vault already set up
- An internet connection for the one-time setup

---

## Step 1 — Install Homebrew

Homebrew is a tool that lets you install software on a Mac easily.

Open the **Terminal** app (search for it in Spotlight with Cmd+Space) and paste this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Press Enter and follow the prompts. This may take a few minutes.

---

## Step 2 — Install ffmpeg

ffmpeg is required to read audio files. In Terminal, run:

```bash
brew install ffmpeg
```

---

## Step 3 — Install Python

Check if you already have Python by running:

```bash
python3 --version
```

If it shows a version number, skip to Step 4.

If not, download and install Python from: **https://www.python.org/downloads/**

---

## Step 4 — Install pipx

pipx is what installs the voice transcriber tool. Run:

```bash
pip3 install pipx && pipx ensurepath
```

Then **close your Terminal and reopen it** before continuing.

---

## Step 5 — Install Voice Transcriber

```bash
pipx install git+https://github.com/XxDisfiguredSpacexX/voice-transcriber
```

This downloads and installs the tool. The first time you run a transcription it will also download the AI model (~145 MB), so make sure you're on Wi-Fi.

---

## Step 6 — Create Your Watched Folder

This is the folder you'll drop audio files into. You can put it anywhere — your Desktop is easy:

```bash
mkdir ~/Desktop/Voice\ Transcripts
```

---

## Step 7 — Start the Watcher

Run this command, replacing the `--output` path with the path to your Obsidian vault's voice notes folder:

```bash
voice-transcriber watch --input ~/Desktop/Voice\ Transcripts --output "/path/to/your/obsidian/Voice Notes"
```

For example:
```bash
voice-transcriber watch --input ~/Desktop/Voice\ Transcripts --output "/Users/yourname/Documents/MyVault/Voice Notes"
```

You'll see:
```
Watching /Users/yourname/Desktop/Voice Transcripts
Press Ctrl+C to stop.
```

---

## Step 8 — Transcribe Your First File

Drop any `.mp3`, `.m4a`, `.aac`, or `.wav` file into your **Voice Transcripts** folder.

Within a few seconds you'll see:
```
Transcribing: my-recording.mp3
Saved: 2026-07-14 12-36 - my-recording.md
```

Open your Obsidian vault and the note will be there.

---

## What the Note Looks Like

```markdown
---
created: 2026-07-14 12:36
tags:
  - voice-note
source: my-recording.mp3
---

# 2026-07-14 12:36 - my-recording

Your transcribed text here, broken into
paragraphs based on natural pauses...
```

---

## Stopping the Watcher

Press **Ctrl+C** in the Terminal window to stop it.

---

## Tips

- The watcher must be running for transcription to happen. You can leave the Terminal window open in the background.
- Larger audio files take longer — a 10 minute recording takes roughly 2-3 minutes to transcribe.
- To use a more accurate (but slower) model, add `--model small` or `--model medium` to the watch command.
- Supported formats: `.mp3`, `.m4a`, `.aac`, `.wav`
