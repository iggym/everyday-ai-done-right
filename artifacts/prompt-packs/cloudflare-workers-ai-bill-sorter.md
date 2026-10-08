# Sort Your Household Bills into a Monthly Budget Sheet

- **Tool:** Cloudflare Workers AI (free daily allocation)
- **Cost:** Free daily allocation of 10,000 Neurons; paid use only after upgrading to Workers Paid
- **Limits:** 10,000 Neurons per day, reset at 00:00 UTC; requests fail once the day's allocation is used up
- **Source:** https://developers.cloudflare.com/workers-ai/platform/pricing/
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/cloudflare-workers-ai-bill-sorter.html

## Steps

1. **Collect the bill text.** Copy the amount, due date, and provider from each notice, one per paragraph. Remove account numbers first.
2. **Run the sorter.** Use the prompt below in a small Worker or the Workers AI playground.
3. **Verify the totals.** Add the amounts by hand and compare them with the total you expect.
4. **Import to a spreadsheet.** Paste the CSV output into any spreadsheet app.
5. **Compare month to month.** Keep one file per month and look for unexplained increases.

## Prompt

```text
From the bill notices below, output CSV with the columns: provider, category (utilities, phone, internet, insurance, subscriptions, other), amount (number only), currency, due date (YYYY-MM-DD). Do not include account numbers. Output the header once, then one row per bill.

NOTICES:
<paste>
```

## Check your result

- [ ] Totals match your manual sum
- [ ] No account numbers were sent to the model
- [ ] Due dates are correct

## Pitfalls

- Remove account and card numbers before you paste anything.
- Subscriptions can hide in bank statements; the sorter only sees what you paste.

_The free allocation was read from Cloudflare's Workers AI pricing page (last updated 1 Oct 2026) on 8 Oct 2026. Cloudflare can change it; check the page before you build on it._
