# Maintain a Small Business Website with Aider and a Local Model

- **Tool:** Aider (open-source coding agent, Apache-2.0)
- **Cost:** $0 — open-source licence (Apache-2.0)
- **Limits:** Your hardware is the limit when run with a local model
- **Source:** https://github.com/Aider-AI/aider
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/aider-small-site-fixes-ollama.html

## Steps

1. **Put the site in git.** Make sure the website folder is a git repository, with a clean commit before you start.
2. **Install Aider.** Follow the install instructions in the Aider repository. It is an open-source Python tool under Apache-2.0.
3. **Point Aider at a local model.** Install Ollama and pull a coder model, then start Aider with an Ollama model string as shown in Aider's documentation for your version.
4. **Ask for one small change.** Example: 'Change the opening hours in contact.html to Mon–Fri 9–5.' Ask for one change per run.
5. **Review the diff before you push.** Run git diff, check the change, and only then publish the site.

## Prompt

```text
Make only the change described below. Do not reformat other content, do not add new sections, and keep the existing HTML structure. After the change, list the files you touched.

CHANGE:
<describe one change>
```

## Check your result

- [ ] The diff touches only the files you expected
- [ ] Prices, hours, and contact details match your source
- [ ] The site still loads locally before you publish

## Pitfalls

- Local coder models are less capable than frontier models; keep changes small.
- Never let an agent run on a live server with no review step.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
