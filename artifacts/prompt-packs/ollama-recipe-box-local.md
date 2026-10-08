# Build a Searchable Local Recipe Box from Your Notes

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-recipe-box-local.html

## Steps

1. **Collect the notes.** Put each recipe in its own text block, separated by a line of three dashes. Rough notes are fine.
2. **Standardise the format.** Use the prompt below to get title, servings, ingredients with quantities, steps, and tags for each recipe.
3. **Check quantities.** Compare the ingredient list against your original note. Models sometimes change a '1 tsp' into '1 tbsp'.
4. **Save as Markdown.** Paste the output into recipes.md. Markdown opens in any editor and stays searchable forever.
5. **Search with your file manager.** Search by ingredient with Ctrl+F or Cmd+F, or ask the model to filter tags for you.

## Prompt

```text
Convert each recipe below into this Markdown format: '## Title', then 'Serves:', 'Time:', 'Ingredients' as a bullet list keeping the original quantities, 'Method' as numbered steps, and 'Tags' (e.g. vegetarian, quick, freezer-friendly). Do not add ingredients that are not in the original. Mark anything unclear with [check].

RECIPES:
<paste>
```

## Check your result

- [ ] Every ingredient quantity matches the original note
- [ ] Unclear items are marked [check] and resolved
- [ ] The Markdown file is saved on your own device

## Pitfalls

- Always taste-test a converted recipe before you trust a changed quantity.
- Food-safety guidance (cooking temperatures, storage) should come from a food-safety authority, not a model.

_Checked on 8 Oct 2026._
