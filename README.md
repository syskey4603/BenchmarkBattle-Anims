# Project Euler x AI — Manim Animation Source

Source code for a YouTube channel that pits Claude, ChatGPT, Gemini, and Grok against Project Euler problems and builds visual mathematical explainers around the results. It started as a way to keep problem-solving and algorithm knowledge sharp and turned into a genuine interest in where these models actually differ — not in benchmark scores but in the reasoning approaches they take and where those approaches break down.

---

## Structure

videos/ — Full-length episode animations, one Manim file per Project Euler problem. Eight scenes per episode covering the problem, each model's approach, and a verdict. Timing is pinned to real voiceover using silence-onset analysis so each visual fires at the exact second the matching sentence starts.

shorts/ — Standalone educational animations under 40 seconds each, covering broader AI and maths topics using the same TimedScene base and portrait config as the main videos.

---

## Stack

Manim Community Edition 0.18+, ffmpeg for mux and concat, ElevenLabs for voiceover. Speech-onset timestamps extracted via ffmpeg silencedetect for frame-accurate audio sync. No external Manim plugins, no ManimGL.
