# Summarise Public Council Minutes into Plain English

- **Tool:** Cloudflare Workers AI (free daily allocation)
- **Cost:** Free daily allocation of 10,000 Neurons; paid use only after upgrading to Workers Paid
- **Limits:** 10,000 Neurons per day, reset at 00:00 UTC; requests fail once the day's allocation is used up
- **Source:** https://developers.cloudflare.com/workers-ai/platform/pricing/
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/cloudflare-workers-ai-council-minutes-summary.html

## Steps

1. **Get the minutes.** Download the official minutes as text or copy them from the council's website.
2. **Chunk by agenda item.** Split long minutes by agenda item so each request stays small and within the daily budget.
3. **Summarise each item.** Use the prompt below one item at a time.
4. **Check against the source.** Verify every amount, date, and vote count against the minutes.
5. **Publish with the link.** Always include the official source link beside the summary.

## Prompt

```text
Summarise this agenda item from council minutes in plain English for a general reader. Give: what was proposed, what was decided, any cost or budget figures (quoted), the vote if recorded, and any next date for public comment. Under 120 words. Do not add opinions.

MINUTES:
<paste item>
```

## Check your result

- [ ] Every figure matches the official minutes
- [ ] The vote and decision are quoted correctly
- [ ] The official link is on the summary

## Pitfalls

- Minutes are not always the final word; check the approved version.
- A summary can omit important caveats. Recommend readers check the source.

_The free allocation was read from Cloudflare's Workers AI pricing page (last updated 1 Oct 2026) on 8 Oct 2026. Cloudflare can change it; check the page before you build on it._
