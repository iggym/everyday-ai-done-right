# Plan Family Chores and Weekly Routines Offline

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-family-chore-planner-offline.html

## Steps

1. **List every recurring job.** Write each task with a rough time estimate: bins 5 min, dishes 15 min, hoovering 20 min, and so on.
2. **Add constraints.** Note who is away on which days, sports practices, and any tasks someone dislikes or cannot do.
3. **Ask for a draft rota.** Use the prompt below. Ask for two options, each with a weekly table, so the family can compare.
4. **Review as a family.** Read both drafts at dinner. Swap tasks by hand; do not regenerate until you have agreed on the shape.
5. **Save and reuse.** Keep the chosen rota as chores.md and update it monthly.

## Prompt

```text
Create two weekly chore rotas for a household with the members and tasks below. Keep total time per person within 20% of each other, respect the availability notes, and never give a task to someone listed as unable to do it. Output a table per option: day, task, person, minutes.

MEMBERS AND AVAILABILITY:
<paste>

TASKS WITH MINUTES:
<paste>
```

## Check your result

- [ ] Time per person is roughly balanced
- [ ] No one is assigned a task they cannot do
- [ ] Two options were compared before choosing

## Pitfalls

- Estimates are guesses. Adjust after two weeks of real use.
- Keep rewards and allowances as a family decision; a model should not set them.

_Checked on 8 Oct 2026._
