# Voice Transcriber — Setup Guide

This tool watches a folder on your Mac. When you drop an audio file into it, the tool automatically transcribes it and saves a note directly into your Obsidian vault.

Supported audio formats: `.mp3` `.m4a` `.aac` `.wav`

---

## Before You Start

You will need:
- A Mac
- Obsidian already installed with a vault set up
- A Wi-Fi connection (for the one-time setup)

All of the steps below are done in the **Terminal** app.

> **How to open Terminal:** Press **Cmd + Space**, type `Terminal`, press Enter.

---

## Step 1 — Install Homebrew

Homebrew is a tool that lets you install software on a Mac from the Terminal.

Paste this into Terminal and press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

It will ask for your Mac password. Type it and press Enter (you won't see the characters — that's normal). This takes a few minutes.

---

## Step 2 — Install ffmpeg

ffmpeg is a tool that lets the transcriber read audio files.

```bash
brew install ffmpeg
```

---

## Step 3 — Check if Python is installed

```bash
python3 --version
```

If you see a version number (e.g. `Python 3.11.0`), move on to Step 4.

If you see an error, download and install Python from **https://www.python.org/downloads/** then come back here.

---

## Step 4 — Install pipx

pipx is what installs the voice transcriber tool cleanly on your Mac.

```bash
pip3 install pipx && pipx ensurepath
```

**After this finishes, close Terminal completely and reopen it before moving on.**

---

## Step 5 — Install Voice Transcriber

```bash
pipx install git+https://github.com/XxDisfiguredSpacexX/voice-transcriber
```

---

## Step 6 — Create a folder to drop audio files into

This is the folder you will drop recordings into whenever you want them transcribed. Run this to create it on your Desktop:

```bash
mkdir ~/Desktop/Voice\ Transcripts
```

You can also just create the folder manually in Finder if you prefer.

---

## Step 7 — Find your Obsidian vault path

This is the most important step to get right. You need to tell the tool where your Obsidian vault is so it knows where to save the transcript notes.

**How to find your vault path:**

1. Open **Finder**
2. Navigate to your Obsidian vault folder (the folder that contains all your notes)
3. Right-click the folder where you want transcripts saved (e.g. a folder called `Voice Notes`)
4. Hold the **Option key** on your keyboard — the menu item changes to **"Copy ... as Pathname"**
5. Click it — this copies the full path to your clipboard

It will look something like this:
```
/Users/yourname/Documents/MyVault/Voice Notes
```

Keep this copied — you will need it in the next step.

---

## Step 8 — Start the watcher

Paste this into Terminal, but **replace the output path with the one you copied in Step 7:**

```bash
voice-transcriber watch --input ~/Desktop/Voice\ Transcripts --output "/Users/yourname/Documents/MyVault/Voice Notes"
```

For example, if your vault path is `/Users/sarah/Documents/Notes/Voice Notes`, the command would be:

```bash
voice-transcriber watch --input ~/Desktop/Voice\ Transcripts --output "/Users/sarah/Documents/Notes/Voice Notes"
```

You will see this in Terminal when it is ready:
```
Watching /Users/yourname/Desktop/Voice Transcripts
Press Ctrl+C to stop.
```

---

## Step 9 — Test it

Drop any audio file into the **Voice Transcripts** folder on your Desktop.

Within a few seconds, Terminal will show:
```
Transcribing: my-recording.mp3
Saved: 2026-07-14 12-36 - my-recording.md
```

Open Obsidian and the note will be there, titled with the date and time it was created.

---

## What the note looks like in Obsidian

```
---
created: 2026-07-14 12:36
tags:
  - voice-note
source: my-recording.mp3
---

# 2026-07-14 12:36 - my-recording

Your transcribed text here, broken into
paragraphs based on your natural pauses...
```

---

## Step 10 — Auto-start on login (optional but recommended)

By default, you need to open Terminal and run the watcher command every time you restart your Mac. This step makes the watcher start automatically in the background whenever you log in — no Terminal needed.

Run this command, replacing both paths with your own (the same ones you used in Step 8):

```bash
cat > ~/Library/LaunchAgents/com.voice-transcriber.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.voice-transcriber</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which voice-transcriber)</string>
        <string>watch</string>
        <string>--input</string>
        <string>$(echo ~/Desktop/Voice\ Transcripts)</string>
        <string>--output</string>
        <string>/Users/yourname/Documents/MyVault/Voice Notes</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$(echo ~/Library/Logs/voice-transcriber.log)</string>
    <key>StandardErrorPath</key>
    <string>$(echo ~/Library/Logs/voice-transcriber.log)</string>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.voice-transcriber.plist
```

> **Remember:** Replace `/Users/yourname/Documents/MyVault/Voice Notes` with your actual Obsidian vault path from Step 7.

The watcher is now running in the background and will restart automatically every time you log in.

**To check if it's working:**
```bash
launchctl list | grep voice-transcriber
```
If you see a line of output, it's running.

**To view the logs:**
```bash
cat ~/Library/Logs/voice-transcriber.log
```

**To stop it permanently:**
```bash
launchctl unload ~/Library/LaunchAgents/com.voice-transcriber.plist
```

---

## Stopping and restarting manually

If you are not using auto-start, you can run the watcher manually:

- **To start:** Run the command from Step 8
- **To stop:** Press **Ctrl+C** in the Terminal window

The Terminal window needs to stay open while the watcher is running. You can minimise it and leave it in the background.

---

## Things to know

- The first time you transcribe a file, the tool downloads an AI model (~145 MB). This only happens once.
- A 10 minute recording takes roughly 2–3 minutes to transcribe.
- Filler words (`um`, `uh`, `you know`, `I mean`) are automatically removed. Everything else is left exactly as spoken.
