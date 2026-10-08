# Practise Interview Answers and Get a Transcript Without Uploading

- **Tool:** whisper.cpp (local speech-to-text, MIT-licensed)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ggml-org/whisper.cpp
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/whisper-cpp-interview-practice-offline.html

## Steps

1. **Pick five likely questions.** Use the questions for your role and write them on cards.
2. **Record each answer.** Answer aloud for about two minutes per question, with your phone on a table, and save each file.
3. **Transcribe locally.** Convert your recording to 16 kHz mono WAV: ffmpeg -i input.m4a -ar 16000 -ac 1 -c:pcm_s16le audio.wav. Then run whisper.cpp on each file. Build whisper.cpp from the repository (follow its README for CMake steps), then download a model with the bundled script, for example ./models/download-ggml-model.sh base.en. Models download once; transcription runs offline.
4. **Score the transcript.** Count filler words (um, like, you know), note the number of seconds before your first point, and check that each answer has a result.
5. **Re-record the weakest answer.** Improve one answer per session rather than rewriting all five.

## Prompt

```text
Review this practice interview answer. Report: word count, filler words with counts, whether there is a clear situation, action, and result (quote where each is), and one suggestion to shorten it. Do not rewrite the answer for me.

ANSWER TRANSCRIPT:
<paste>
```

## Check your result

- [ ] Each answer includes an outcome you can verify
- [ ] Filler-word counts were checked by ear on one recording
- [ ] Your examples are true and can be discussed in depth

## Pitfalls

- Do not memorise scripted answers word for word; aim for structure and confidence.
- A transcript cannot judge tone or body language. Also record a short video once in a while.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
