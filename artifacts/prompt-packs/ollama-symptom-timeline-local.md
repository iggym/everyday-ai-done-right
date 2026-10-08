# Turn a Symptom Diary into a Doctor-Ready Timeline, Locally

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-symptom-timeline-local.html

## Steps

1. **Gather the raw notes.** Put each entry in a text file, one per line, starting with the date: 2026-09-14 headache after lunch, 6/10, ibuprofen helped.
2. **Run the model locally.** Use ollama run llama3.2. Keep the chat on your device; do not paste diary text into a cloud chatbot.
3. **Ask for a neutral timeline.** Use the prompt below. You want dates, symptoms, severity, triggers you recorded, and what you tried.
4. **Mark gaps.** Let the model list missing dates or missing severity scores so you can fill them in from memory before the visit.
5. **Bring it to the appointment.** Print the timeline and add the questions you want answered. Keep your own original diary as the source of truth.

## Prompt

```text
Turn the diary entries below into a chronological timeline. For each entry output: date, symptom(s), severity if recorded, possible triggers the writer noted, and treatments tried with the result. Do not interpret or diagnose. At the end, list dates with missing information and any questions a clinician might want answered, phrased neutrally.

DIARY:
<paste>
```

## Check your result

- [ ] Every line matches an original diary entry
- [ ] No diagnosis or medication advice has been added
- [ ] Gaps are listed so you can fill them in

## Pitfalls

- Do not use a summary in place of medical advice. Call your clinician or local emergency number for urgent symptoms.
- Small models can mislabel severity. Keep the numbers you wrote.

_Checked on 8 Oct 2026._
