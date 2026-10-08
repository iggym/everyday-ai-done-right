# Budget Your Free Daily Neurons on Cloudflare Workers AI

- **Tool:** Cloudflare Workers AI (free daily allocation)
- **Cost:** Free daily allocation of 10,000 Neurons; paid use only after upgrading to Workers Paid
- **Limits:** 10,000 Neurons per day, reset at 00:00 UTC; requests fail once the day's allocation is used up
- **Source:** https://developers.cloudflare.com/workers-ai/platform/pricing/
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/cloudflare-workers-ai-daily-budget.html

## Steps

1. **Read the model's price in Neurons.** On the pricing page, each model lists Neurons per million input and output tokens. For example, the small @cf/meta/llama-3.2-1b-instruct lists 2,457 Neurons per million input tokens and 18,252 per million output tokens.
2. **Do the sum for your workload.** Estimate tokens per request and requests per day. Roughly: 10,000 Neurons covers about 4 million input tokens on that small model, but only about half a million output tokens, because output costs more Neurons.
3. **Pick the cheapest model that works.** Test two or three models on your real prompts and compare answer quality against the Neuron cost, not the headline price alone.
4. **Cap your usage.** Add a counter in your Worker that stops calling the model at a daily threshold you set, and falls back to a message to the user.
5. **Watch the dashboard.** Check the Workers AI usage view after the first week, then once a month.

## Prompt

```text
For a Cloudflare Worker that calls a Workers AI model, outline: (1) the daily request budget from my 10,000-Neuron allocation given the model's Neuron price in my table, (2) a daily counter that stops calls at 90% of budget, (3) the message users see when the budget is reached. Show the calculation.

MODEL PRICE TABLE:
<paste>
AVERAGE TOKENS PER REQUEST:
<number>
```

## Check your result

- [ ] The calculation uses the table for your exact model
- [ ] A daily stop is in place before you publish
- [ ] You know when the UTC day resets

## Pitfalls

- Output tokens are the expensive part; ask for short answers.
- Some models are priced differently; read the entry for your model, not a neighbouring one.

_The free allocation was read from Cloudflare's Workers AI pricing page (last updated 1 Oct 2026) on 8 Oct 2026. Cloudflare can change it; check the page before you build on it._
