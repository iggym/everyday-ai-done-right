# Turn Lecture Recordings into Captioned Study Notes Offline

- **Tool:** whisper.cpp (local speech-to-text, MIT-licensed)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ggml-org/whisper.cpp
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/whisper-cpp-lecture-notes-offline.html

## Steps

1. **Set up whisper.cpp.** Build whisper.cpp from the repository (follow its README for CMake steps), then download a model with the bundled script, for example ./models/download-ggml-model.sh base.en. Models download once; transcription runs offline.
2. **Convert and transcribe.** Convert your recording to 16 kHz mono WAV: ffmpeg -i input.m4a -ar 16000 -ac 1 -c:pcm_s16le audio.wav. Then run the transcription binary and keep the timestamps in the output.
3. **Generate notes from the transcript.** Use the prompt below in a local model, one lecture at a time.
4. **Link notes back to timestamps.** Keep the [00:12:31] markers so you can jump to the exact point in the audio when you revise.
5. **Review with your own words.** Rewrite three key ideas per lecture without looking at the notes. That is the step that builds memory.

## Prompt

```text
Turn this lecture transcript into study notes: a title, five key ideas as bullets with the timestamp they start at, three terms with plain-English definitions taken from the lecture, and two questions a student should be able to answer afterwards. Do not add facts that are not in the transcript.

TRANSCRIPT:
<paste>
```

## Check your result

- [ ] Timestamps match the audio
- [ ] Definitions come from the lecture, not from memory of the subject
- [ ] You can explain each key idea without the notes

## Pitfalls

- Check recording rules with your instructor or institution before recording a class.
- Technical terms are often misheard; correct them against the slides.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
