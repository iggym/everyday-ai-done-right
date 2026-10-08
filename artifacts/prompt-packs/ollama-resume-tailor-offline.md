# Tailor Your Resume Offline with a Local Model

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-resume-tailor-offline.html

## Steps

1. **Save both documents as plain text.** Copy your resume and the job advert into resume.txt and job.txt. Plain text is easier for a small model than PDF.
2. **Start a local model.** Run ollama run llama3.2 and leave the chat open. Nothing you type is sent to a server.
3. **Ask for matches, not rewrites.** Use the prompt below. You want a list of which of your existing bullets map to the job's requirements, and which requirements have no evidence.
4. **Write the edits yourself.** Choose the bullets to keep, reword them in your own voice, and add numbers only if you can back them up.
5. **Run a final consistency check.** Ask the model to flag dates, job titles, or claims that differ between the old and new versions.

## Prompt

```text
Compare my resume and the job description below. Output three lists: (1) requirements my resume already evidences, quoting my bullet; (2) requirements with weak or no evidence; (3) my bullets that are not relevant to this role. Do not invent experience. Do not add numbers that are not in my resume.

RESUME:
<paste>

JOB DESCRIPTION:
<paste>
```

## Check your result

- [ ] No claim appears that is absent from your original resume
- [ ] Dates and employer names match your source document
- [ ] You can defend every bullet in an interview

## Pitfalls

- Local models sometimes invent metrics. If a number is not in your original, delete it.
- Pair this with the ATS and impact-statement guides in this directory for formatting.

_Checked on 8 Oct 2026._
