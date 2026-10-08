# Plan Weekly Meal Prep with a Local Model and a Shopping List

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-weekly-meal-prep-local.html

## Steps

1. **Inventory the cupboard.** List what you already have, with rough quantities, in a text file.
2. **Set your constraints.** Note servings, budget, allergies, and foods you will not eat.
3. **Generate a plan.** Use the prompt below for five dinners and two lunches, reusing ingredients across meals.
4. **Build the shopping list.** Ask for a list grouped by store section, subtracting what you already own.
5. **Check the food-safety basics.** Confirm storage times and reheating guidance with a food-safety authority before batch-cooking.

## Prompt

```text
Plan seven dinners and seven lunches for batch cooking. Reuse ingredients across meals to reduce waste. Respect these constraints: servings, allergies, and foods to avoid below. Output: the plan by day, a shopping list grouped by store section with only items I do not already have, and the cooking order for one prep session.

INVENTORY:
<paste>

CONSTRAINTS:
<paste>
```

## Check your result

- [ ] No listed allergen or excluded food appears
- [ ] The shopping list subtracts your inventory
- [ ] Storage and reheating times were checked against a food-safety source

## Pitfalls

- Nutrition numbers from a model are estimates. For medical diets, ask a dietitian or your clinician.
- Cooked food has safe storage limits; do not rely on a model for them.

_Checked on 8 Oct 2026._
