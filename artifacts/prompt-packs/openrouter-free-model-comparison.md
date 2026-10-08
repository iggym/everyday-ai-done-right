# Compare Three Free Models on OpenRouter Side by Side

- **Tool:** OpenRouter :free model variants
- **Cost:** $0 on :free variants — listed by OpenRouter as free versions of models
- **Limits:** Free variants have their own rate limits and availability; check the model page
- **Source:** https://openrouter.ai/docs/guides/routing/model-variants/free
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/openrouter-free-model-comparison.html

## Steps

1. **Create a free OpenRouter account.** Sign up and create an API key, or use the web chat interface if you prefer.
2. **Find free variants.** Browse the models page and filter for models whose ID ends in :free. Note each model's context length.
3. **Use the same prompt for all.** Paste one test prompt, identical for every model. Keep a copy of each answer.
4. **Score blind.** Shuffle the answers, label them A, B, C, and rank them before you check which model is which.
5. **Record the winner for each task type.** Keep a short table: task, best model, why. Re-check it in a month, since free availability changes.

## Prompt

```text
Answer the question below in under 200 words. Be accurate, say so if you are unsure, and avoid filler.

QUESTION:
<your everyday question, e.g. 'How do I explain compound interest to a 12-year-old?'>
```

## Check your result

- [ ] Each model ID you used ends in :free
- [ ] Same prompt, same settings for every model
- [ ] Rankings were made before you saw the model names

## Pitfalls

- Free variants can be rate-limited at busy times; retry later rather than switching models.
- Do not send personal or confidential data to any cloud model without reading the provider's terms.

_The ':free' variant behaviour was read from OpenRouter's documentation on 8 Oct 2026. Free models change often; check the model's page for current limits._
