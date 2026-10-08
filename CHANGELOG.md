# Changelog

Dated entries for guide additions, verification refreshes, and site changes (backlog 12.5 — started).
Per-guide verification dates live in `metadata.json` (`verified`).

## 2026-10-08

### Added — 36 new guides (136 published in total)
Local-first and open-source guides, plus free-tier guides for Cloudflare Workers AI, OpenRouter `:free` models, and Mistral's Le Chat free plan.

- **Ollama (local, MIT):** lease summaries, resume tailoring, symptom timelines, recipe box, family chores, client email drafts, weekly meal prep, textbook flashcards.
- **whisper.cpp (MIT):** meeting transcripts, lecture notes, interview practice, family captions, travel voice journal.
- **Tesseract (Apache-2.0) and OCRmyPDF (MPL-2.0):** receipts to CSV, searchable forms, lab printouts, screen-reader-ready scans.
- **Aider and Continue (Apache-2.0):** small-site fixes, learning a codebase, local PR review, unit tests.
- **OpenRouter `:free` variants:** model comparison, newsletter drafts, language practice, follow-up notes, naming brainstorm.
- **Cloudflare Workers AI:** daily-allocation budgeting, council minutes summaries, bill sorter.
- **Mistral Le Chat (Free plan):** packing lists, job-offer comparison, party planner, zine outline.
- **LibreTranslate (AGPL-3.0, self-hosted):** foreign notices, school letters, product copy.

Each new guide has a verification note naming what was checked and when, a copy-paste prompt, a checklist, and pitfalls. Every guide also has a prompt pack in `artifacts/prompt-packs/` and a social card in `og/`.

### Changed
- **Duplicate draft retired:** `plan-week-trip-gemini-flash` (draft, overlapped `travel-itinerary-gemini-flash`) removed; old URL redirects to the itinerary guide.
- **Categories merged:** `ai-tools` (1 guide) → `learning`; `software-engineering` (1 guide) → `business`.
- **Homepage:** sort control (newest, recently verified, quickest read), tool-family filter, and a per-card error boundary so one malformed entry can't blank the feed.
- **Article chrome:** print stylesheet (URLs shown after links; navigation hidden); per-guide `og:image` / `twitter:image`; web manifest link.
- **README:** the catalog is generated from `metadata.json` between `<!-- catalog:start -->` markers, so it can't drift. `metadata.json` is documented as a read-only data source.
- `.gitignore`: the unused Node.js template block was removed.

### Added — site pages and tooling
- `privacy.html`: what the site stores, the anonymous Cloudflare page-view counter, Google Fonts requests, third-party tools, and issue reports. Linked from the homepage, article footers and sitemap.
- `manifest.webmanifest` (installable-app metadata; icons already existed).
- `.github/ISSUE_TEMPLATE/outdated-limit.yml`: structured "Outdated limit" report form. Every guide's report link points at it.
- `scripts/make_social_cards.py`: per-guide 1200×630 social cards (Pillow).
- `scripts/batches/`: the 2026-10 batch source and renderer.

## Earlier

- 2026-10-08 (remediation PR #2): metadata integrity, SEO and accessibility chrome, 404 and sitemap, feed, homepage clarity.
