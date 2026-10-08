# Write Client Emails from Bullet Notes, Fully Offline

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-client-email-drafts-offline.html

## Steps

1. **Write bullets straight after the call.** Three to six lines: what was agreed, who does what, and the next date.
2. **Generate a draft.** Use the prompt below with your house style: greeting, short paragraphs, one clear ask.
3. **Strip anything you would not send.** Delete internal notes, prices you did not agree, and names of other clients.
4. **Edit the tone yourself.** Read it aloud once. Small models can sound stiff or overly apologetic.
5. **Keep a template library.** Save the best outputs as templates in a local folder for next time.

## Prompt

```text
Write a short follow-up email to a client. Use a warm, direct tone, no more than 150 words, and a single clear call to action. Include only the facts below; do not add prices, dates, or commitments that are not listed.

BULLET NOTES:
<paste>
```

## Check your result

- [ ] Every commitment and date matches your notes
- [ ] No internal or other-client information appears
- [ ] The email has one clear next step

## Pitfalls

- Read contracts before promising timelines; the model cannot know your obligations.
- Local speed depends on your hardware. A smaller model is quicker for short emails.

_Checked on 8 Oct 2026._
