# Turn Voice Notes from a Trip into a Searchable Travel Journal

- **Tool:** whisper.cpp (local speech-to-text, MIT-licensed)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ggml-org/whisper.cpp
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/whisper-cpp-travel-voice-journal.html

## Steps

1. **Record with dated filenames.** Use your phone's voice recorder and keep the default timestamp in the filename.
2. **Batch the files at home.** Copy the audio to one folder and convert each file to 16 kHz WAV, as in the other whisper.cpp guides.
3. **Transcribe the folder.** Run whisper.cpp once per file. Save each transcript next to its audio, with the same name.
4. **Compile a day summary.** Use the prompt below in a local model, one day at a time, to make a readable diary entry.
5. **Add the place names.** Keep a short list of places and check spellings from receipts or maps.

## Prompt

```text
Turn these voice-note transcripts from one day into a short travel diary entry in the first person. Keep the order of events, include place names exactly as spoken, and keep it under 300 words. Do not add events or feelings that are not in the notes.

NOTES:
<paste>
```

## Check your result

- [ ] Place names match your receipts or maps
- [ ] No events were added that you did not record
- [ ] Each entry is dated

## Pitfalls

- Recording people without consent can be illegal in some places; ask first.
- Save the original audio too; the transcript is only a search index.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
