# Transcribe Meetings Offline with whisper.cpp

- **Tool:** whisper.cpp (local speech-to-text, MIT-licensed)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ggml-org/whisper.cpp
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/whisper-cpp-meeting-transcripts-offline.html

## Steps

1. **Set up whisper.cpp.** Build whisper.cpp from the repository (follow its README for CMake steps), then download a model with the bundled script, for example ./models/download-ggml-model.sh base.en. Models download once; transcription runs offline.
2. **Convert the recording.** Convert your recording to 16 kHz mono WAV: ffmpeg -i input.m4a -ar 16000 -ac 1 -c:pcm_s16le audio.wav.
3. **Transcribe.** Run the bundled command-line binary on the WAV file with the model you downloaded, and save the output as text. Check the README for the current binary name and flags.
4. **Add speaker labels by hand.** Whisper does not reliably separate speakers. Use a two-minute pass to label the people who spoke, then keep the file.
5. **Extract action items.** Paste the transcript into a local model (see the Ollama guides in this directory) and ask for owners and deadlines, then check each one against the audio.

## Prompt

```text
From this meeting transcript, list: decisions made, action items with owner and due date (write 'unassigned' if unclear), open questions, and figures mentioned with the exact sentence they came from. Do not infer anything not said.

TRANSCRIPT:
<paste>
```

## Check your result

- [ ] The transcript was produced without uploading audio
- [ ] Action items match a timestamp you have listened to
- [ ] Names and figures were checked against the recording

## Pitfalls

- Background noise and crosstalk lower accuracy; use a clip-on microphone when you can.
- Recording a meeting may require consent under local law. Tell participants first.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
