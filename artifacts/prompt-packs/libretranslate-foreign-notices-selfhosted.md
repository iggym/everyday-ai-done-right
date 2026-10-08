# Translate Foreign-Language Notices with Self-Hosted LibreTranslate

- **Tool:** LibreTranslate (self-hosted, AGPL-3.0)
- **Cost:** $0 to self-host — open-source under AGPL-3.0
- **Limits:** Your own server's capacity; no quota
- **Source:** https://github.com/LibreTranslate/LibreTranslate
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/libretranslate-foreign-notices-selfhosted.html

## Steps

1. **Install LibreTranslate.** Follow the installation options in the project's README (Python package or Docker). Choose only the languages you need.
2. **Start the service.** Run it on your laptop and open the local web interface in your browser.
3. **Translate short passages.** Paste one sentence or notice at a time and read the result against the original.
4. **Confirm critical wording.** For anything with a deadline or a legal effect, ask a qualified translator or the issuing office.
5. **Keep a phrase list.** Save useful translations as a list for your trip.

## Prompt

```text
(Use the LibreTranslate interface or API.) Translate the notice below from {source} to {target}. Keep numbers, dates, and proper names unchanged, and flag any word that has more than one likely meaning.
```

## Check your result

- [ ] Dates and numbers match the original
- [ ] Deadlines and legal wording were checked with a person
- [ ] Only the languages you need were installed

## Pitfalls

- Machine translation can produce confident mistakes on medical or legal text.
- Check the AGPL-3.0 licence terms if you run a public service for other users.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
