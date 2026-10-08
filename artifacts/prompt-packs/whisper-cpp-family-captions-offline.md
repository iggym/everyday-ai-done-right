# Caption Family Videos and Voice Messages Locally

- **Tool:** whisper.cpp (local speech-to-text, MIT-licensed)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ggml-org/whisper.cpp
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/whisper-cpp-family-captions-offline.html

## Steps

1. **Extract the audio.** Use ffmpeg to pull the audio track: ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:pcm_s16le audio.wav.
2. **Transcribe.** Run whisper.cpp with the model you downloaded. Ask for timestamped output so each line has a start time.
3. **Turn the transcript into captions.** Convert the timed text to an SRT subtitle file using a plain-text editor or a small script, then check the timings.
4. **Burn in or attach.** Load the SRT as a sidecar file in most video players, or add it to the video with ffmpeg if you want it always visible.
5. **Correct names.** Family names and place names are the most common errors. Fix them before you share.

## Prompt

```text
Clean up this timed transcript for subtitles: keep each caption under two lines and 42 characters per line, correct obvious mishearings only when the context is clear, mark unclear words as [unclear], and keep the timestamps unchanged.

TRANSCRIPT:
<paste>
```

## Check your result

- [ ] Captions are readable at the video's speed
- [ ] Family and place names are correct
- [ ] Unclear speech is marked rather than guessed

## Pitfalls

- Speech models struggle with overlapping voices and music; expect to edit.
- Share private family recordings only with people you choose.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
