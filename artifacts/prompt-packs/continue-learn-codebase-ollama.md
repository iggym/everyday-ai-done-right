# Learn an Unfamiliar Codebase with Continue and a Local Model

- **Tool:** Continue (open-source IDE assistant, Apache-2.0)
- **Cost:** $0 — open-source licence (Apache-2.0)
- **Limits:** Your hardware is the limit when run with a local model
- **Source:** https://github.com/continuedev/continue
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/continue-learn-codebase-ollama.html

## Steps

1. **Install Continue.** Install the Continue extension from your editor's marketplace; its repository is open source under Apache-2.0.
2. **Connect a local model.** Pull a code model with Ollama, then add it in Continue's settings using the provider and model name shown in Continue's documentation.
3. **Ask about one file at a time.** Select a function and ask for a plain-English walkthrough. Smaller selections give more accurate answers.
4. **Trace one path.** Ask the model to follow a single request from the entry point to the database call, then verify each step yourself.
5. **Write your own notes.** Keep a short architecture note in the repository and correct it as you learn.

## Prompt

```text
Explain the selected code to someone who knows the language but not this project. Cover: what it does, its inputs and outputs, side effects, and any assumptions it makes. Point out anything that looks like a bug, but do not change the code.

CODE:
<selection>
```

## Check your result

- [ ] Each explanation matches what you see when you step through it
- [ ] Suspected bugs are verified with a test, not accepted on trust
- [ ] Your notes are in your own words

## Pitfalls

- Local models can misread complex control flow; confirm with a debugger.
- Do not paste secrets or credentials into any model, local or not.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
