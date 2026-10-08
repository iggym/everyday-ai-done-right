# Turn a Textbook Chapter into Flashcards with Local Ollama

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-textbook-flashcards-local.html

## Steps

1. **Export the chapter text.** Copy the text into chapter.txt, or OCR the pages first with the Tesseract guide in this directory.
2. **Ask for question-answer pairs.** Use the prompt below. Keep chunks to one or two sections so the model stays accurate.
3. **Check each card against the book.** Verify every answer on the page. Delete cards that test trivia rather than understanding.
4. **Import into your flashcard app.** Export as a CSV with two columns, front and back, and import it into any spaced-repetition tool that accepts CSV.
5. **Review daily for ten minutes.** Short, frequent sessions beat long cramming sessions.

## Prompt

```text
From the chapter text below, write 15 flashcards that test understanding, not trivia. Format each as: FRONT ; BACK, one per line, with the back under 25 words. Use only information in the text. Skip any section that is only examples or exercises.

TEXT:
<paste>
```

## Check your result

- [ ] Each answer can be found in the source text
- [ ] Cards test explanations and relationships, not isolated dates
- [ ] The CSV imports cleanly

## Pitfalls

- Models sometimes write confident wrong answers. Treat the draft as a first pass.
- Copyright: keep flashcards for your own study, not for publication.

_Checked on 8 Oct 2026._
