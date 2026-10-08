# Build a Packing List from a Forecast and Your Trip Plan

- **Tool:** Mistral Le Chat (Free plan)
- **Cost:** Free plan — no payment needed to start
- **Limits:** Limited messages, web searches, coding sessions and document uploads; exact allowances are shown in your account
- **Source:** https://mistral.ai/pricing/
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/mistral-le-chat-packing-list.html

## Steps

1. **Write the trip facts.** Dates, destination, transport, accommodation, and the activities you have booked.
2. **Check the forecast yourself.** Look up the weather for those dates from a national weather service, and paste the summary.
3. **Generate the list.** Use the prompt below. Ask for a list grouped into clothing, toiletries, documents, and tech.
4. **Add personal items.** Medication, glasses, and dietary needs are yours to add; the model cannot know them.
5. **Tick it off a week early.** Pack from the list and move unused items into a 'probably not needed' section for next time.

## Prompt

```text
Create a packing checklist for this trip. Group items into clothing, toiletries, documents, electronics, and activity-specific gear. Base the clothing on this forecast summary. Add a note for each item that depends on the activity. Keep it under 80 items.

TRIP:
<dates, destination, transport, activities>

FORECAST SUMMARY:
<paste>
```

## Check your result

- [ ] Documents such as passports and tickets are on the list
- [ ] Medication and prescriptions were added by you
- [ ] Clothing matches the forecast

## Pitfalls

- Check entry rules, visas, and vaccination requirements with official government sources.
- Lists from a model can miss local rules; verify before you fly.

_The Free plan's features were read from Mistral's pricing page on 8 Oct 2026. Allowances are set by Mistral and shown in your account._
