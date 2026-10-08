# Translate School Letters for Multilingual Families, Self-Hosted

- **Tool:** LibreTranslate (self-hosted, AGPL-3.0)
- **Cost:** $0 to self-host — open-source under AGPL-3.0
- **Limits:** Your own server's capacity; no quota
- **Source:** https://github.com/LibreTranslate/LibreTranslate
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/libretranslate-school-letters-selfhosted.html

## Steps

1. **Set up the translator.** Install LibreTranslate on a home computer or small server, as described in the project README.
2. **Translate paragraph by paragraph.** Long letters translate better in short chunks. Keep the original next to the translation.
3. **Mark dates and amounts.** Circle every date, time, and amount on the original, then confirm them in the translation.
4. **Ask the school for the official version.** For forms or consent slips, request the translated version from the school.
5. **Share carefully.** Share the translation only with the family it concerns.

## Prompt

```text
(Use the LibreTranslate interface or API.) Translate this school letter from {source} to {target}. Keep all dates, times, sums of money, names, and form numbers unchanged. Mark any sentence where the meaning is unclear.
```

## Check your result

- [ ] Every date, time, and amount matches the original
- [ ] Consent or payment forms were confirmed with the school
- [ ] Translations are shared only with the relevant family

## Pitfalls

- Do not rely on machine translation for consent, safeguarding, or medical letters.
- Children's details are sensitive; keep copies on the device you control.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
