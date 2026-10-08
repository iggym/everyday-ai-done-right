# Project Audit: Everyday AI, Done Right

**Date:** 2026-10-08  
**Scope:** Full site audit across 13 quality dimensions  
**Files reviewed:** `index.html`, `metadata.json` (100 articles), 104 article HTML files, `README.md`, `.gitignore`, `LICENSE`  
**Repository:** `iggym/everyday-ai-done-right` (GitHub Pages static site)  
**Last updated:** 2026-10-08 16:51 CDT — status pass after the remediation PR (see below)

---

## 📌 Status update — 2026-10-08 (remediation PR)

All 🔴 Critical items, all 🟡 High-Impact items except the SSG migration (12.1), and all five Clarity items (13.x) were implemented in one PR. Legend used below: `[x]` done · `[~]` partially done (remainder tracked in `current-tasks-2026-10-08-1651.md`) · `[ ]` open.

**What shipped**

- **Data integrity** — `metadata.json` now has 101 unique zero-padded ids, lowercase categories, canonical formatting, a `site.categories` map (single source of truth for labels + distinct emojis), `pinned_reason`, and `site.redirects` for removed slugs. `scripts/validate_metadata.py` enforces all of it; `.github/workflows/validate.yml` runs it on every push/PR.
- **Orphans** — `build-the-tool-that-doesnt-exist-yet` published (editorial "[re-verify]" notes removed); the three superseded files were deleted and redirect (via the 404 page) to their successors.
- **Every article (101 files) now gets a generated, idempotent chrome** from `scripts/build.py`: `<meta description>` where missing, canonical, Open Graph + Twitter Card, `article:*` tags, favicon links, RSS autodiscovery, JSON-LD `Article` + `BreadcrumbList`, skip-to-content link (targets `<main>`/`<h1>`), breadcrumb nav (Home › Category › Title) with reading time + verified date, a **staleness notice** for guides verified > 12 months ago (static at build time and re-evaluated by a 300-byte inline script at view time), and a **Related guides / Next steps** footer (3 nearest guides by category/tags/tool, category link, master-catalog link, report-a-problem link, provider source link). 70 icon-only buttons received `aria-label`s. The draft article is `noindex`.
- **New root assets** — `404.html` (search hand-off, category chips, "did you mean" suggestions, slug redirects), `favicon.svg/.ico`, `apple-touch-icon.png`, `og-image.png` (1200×630, brand fonts), `robots.txt`, `sitemap.xml` (101 URLs), `feed.xml` (RSS 2.0, 50 newest), `.nojekyll`.
- **Homepage** — "New here? How this works" onboarding strip; filter chips are real `<button aria-pressed>` elements; `<nav>` landmarks (primary + footer); cost widget exposed to assistive tech (no more `aria-hidden`); pinned card carries a "📌 Pinned · Start here" label + reason; stale cards show "⚠ verified … · re-check"; `?category=` and `?q=` deep links; proper error state with retry when `metadata.json` fails; distinct category emojis + friendly labels; AA-contrast `--muted`/`--green`/`--coral`; invalid dark-mode chip CSS rule fixed; GitHub / RSS / "report a limit" links.
- **Bugs found along the way** — `stable-diffusion-comfyui-setup-guide.html` was truncated mid-file with no closing tags and no JavaScript (theme toggle, calculator, accordion, reveal and share buttons were all dead) → repaired; `consistent-character-bible-nano-banana.html` had `<title>React Artifact</title>` → fixed; EMOJI_MAP keyed `software_engineering` while the category is `software-engineering` → fixed by `site.categories`.

**Still open from the original matrix:** 12.1 (SSG migration) and the *human* half of 4.1 — the 23 stale guides are now clearly flagged, but their limits still need to be re-checked against provider docs and their `verified` dates refreshed.

---

## Executive Summary

Everyday AI, Done Right is a curated directory of 100 published zero-cost AI workflows delivered as a static site on GitHub Pages. The core value proposition is strong — verified, genuinely-free AI guides for real people. ~~The site performs well functionally, but has significant gaps in metadata consistency, SEO infrastructure, accessibility compliance, and architectural coherence that limit discoverability, trust signals, and maintainability.~~ **Update 2026-10-08:** metadata consistency, SEO infrastructure, baseline accessibility and site-wide navigation coherence have been remediated (see status update above). The remaining structural gap is the per-article template sprawl (6.1 / 12.1).

### Current Stats
| Metric | At audit (2026-10-08 AM) | After remediation (2026-10-08 PM) |
|---|---|---|
| Total articles in metadata | 100 | **101** |
| Published | 99 | **100** |
| Drafts | 1 | 1 (`noindex`, still to decide) |
| HTML files on disk | 104 (4 orphaned) | **101 (0 orphaned)** |
| Categories | 14 (with casing inconsistencies) | **12, lowercase, defined in `site.categories`** |
| Articles flagged stale (verified > 12 months ago) | 24 (pre-2026 rule) | **23 flagged automatically**; human re-verification still open |
| Duplicate IDs in metadata | 20 groups | **0** (enforced by validator + CI) |
| Articles with meta description / OG / canonical / JSON-LD | 24 / 3 / 1 / 1 | **101 / 101 / 101 / 101** |
| Articles with skip link / breadcrumbs / related guides | 0 / 0 / 0 | **101 / 101 / 101** |
| Root infrastructure (404, favicon, sitemap, robots, feed, og-image) | none | **all present** |

---

## 1. HIGH UTILITY — Solves a pressing problem effectively

**Rating: ✅ Strong**

### What works
- Covers genuinely high-value use cases: resume building, medical bill audits, debt collection defense, meal planning, legal self-help, accessibility tools
- Every guide targets a real, costly problem people pay $12–$79/month for
- Clear hooks in metadata ("Stop doing manual data entry…", "FDCPA violations…")

### Issues & Tasks
- [x] **1.1** — ~~4 orphaned HTML files exist but are not in metadata~~ **Done.** `build-the-tool-that-doesnt-exist-yet` published (unique Claude Artifacts + GitHub Pages workflow). The other three were superseded by newer guides on the same tool and were removed; their URLs now redirect via `404.html` + `site.redirects`:
  - `build-custom-web-tools-without-coding-for-free` → `build-the-tool-that-doesnt-exist-yet`
  - `read-foreign-signs-instantly-for-free` → `offline-ai-translate-camera-travel-kit-free`
  - `source-grounded-ai-study-engine` → `turn-any-textbook-into-self-testing-study-system`
- [ ] **1.2** — 1 article is in `draft` status (`plan-week-trip-gemini-flash`) — evaluate whether to publish or remove (now `noindex`; excluded from sitemap/feed/related)
- [~] **1.3** — ~~No feedback mechanism~~ Every article footer, every staleness notice and the homepage footer now link to a pre-filled GitHub issue ("Report an outdated limit"). An issue template is still a nice-to-have.
- [ ] **1.4** — Some categories have only 1 article (`ai-tools`, `software-engineering`) — consider merging or expanding

---

## 2. HIGH LEVERAGE — Multiplies user effort with scalable results

**Rating: ✅ Strong**

### What works
- Clear "What this replaces" cost widget on homepage
- Each article is a standalone workflow users can follow immediately
- Categories cover career, health, legal, learning, household — high-leverage life domains

### Issues & Tasks
- [x] **2.1** — ~~No internal cross-linking between related articles~~ **Done.** Every article ends with "Related guides" (3 nearest by category, shared tags, tool family) plus "More {Category} guides →", "All guides" and the master catalog.
- [ ] **2.2** — No "workflow bundles" or collections that group related guides for compound value (e.g., "Job Hunt Kit": resume + ATS + interview prep)
- [ ] **2.3** — No sort options on directory (by date, category, reading time, popularity)

---

## 3. HIGH AGENCY — Empowers users with total control

**Rating: ✅ Strong**

### What works
- Theme toggle (auto/light/dark) with localStorage persistence
- Client-side search and category filtering — no server dependency
- Guides emphasize open-source, privacy-first, and self-hosted tools
- Zero data collection from users — pure static site

### Issues & Tasks
- [ ] **3.1** — No way for users to bookmark/save articles locally (e.g., localStorage favorites list)
- [ ] **3.2** — No export/print-friendly mode for guides (users printing or saving offline)
- [ ] **3.3** — Search only filters by text match — no advanced filtering by tool, difficulty, or platform

---

## 4. HIGH INTEGRITY — Transparent, no dark patterns

**Rating: ✅ Very Strong**

### What works
- Every article explicitly states pricing verification date
- Clear disclaimers ("not legal advice", "verify statutes")
- Honest about trade-offs (caps, training data toggles, non-private uploads)
- BSD 3-Clause license — open and permissive

### Issues & Tasks
- [~] **4.1** — **24 articles had verification dates from 2023–2025.** **Staleness warning shipped:** any guide verified > 365 days ago is flagged on its homepage card ("⚠ verified … · re-check") and gets a prominent notice at the top of the article with a report link; the rule is rolling (computed at build time *and* at view time), so nothing needs manual flagging. **Still open:** actually re-checking the 23 flagged guides against provider docs and refreshing their `verified` dates (requires a human with web access — not possible from the remediation sandbox).
- [ ] **4.2** — Cloudflare Web Analytics is injected in `index.html` but not disclosed in a privacy policy — add a brief analytics disclosure (the script comment now says "privacy-friendly, cookie-less"; a visible note is still missing)
- [x] **4.3** — ~~No `robots.txt` or `sitemap.xml`~~ **Done.** Both generated; `robots.txt` points at the sitemap and disallows `/tasks/` and `/scripts/`.

---

## 5. HIGH TRUST — Consistently delivers on promises

**Rating: ✅ Strong** (was ⚠️ Needs Work)

### What works
- Strong "Verified" badges on cards — now with an explicit ⚠ state when stale
- Honest language about limitations
- Branded 404, favicon, social preview image, canonical URLs and structured data on every page

### Issues & Tasks
- [x] **5.1** — ~~No `404.html` error page~~ **Done.** Branded 404 with search hand-off (`?q=`), category chips, "did you mean" suggestions from the requested slug, and automatic redirects for renamed guides.
- [x] **5.2** — ~~No favicon~~ **Done.** `favicon.svg` + `favicon.ico` (16/32/48) + `apple-touch-icon.png`, linked from every page (`scripts/make_brand_assets.py`).
- [x] **5.3** — ~~No Open Graph image~~ **Done.** Site-wide `og-image.png` (1200×630, Manrope/Inter/JetBrains Mono). Per-article images remain a nice-to-have.
- [ ] **5.4** — No privacy policy or terms page — especially needed since Cloudflare analytics is used
- [x] **5.5** — ~~76 of 99 articles lack `<meta name="description">`~~ **Done.** 101/101 (existing descriptions kept; missing ones derived from the metadata hook, ≤155 chars).
- [x] **5.6** — ~~97 of 99 articles lack Open Graph tags~~ **Done.** 101/101 have `og:*`, `article:*` and `twitter:*` tags (pre-existing tags respected, never duplicated).
- [x] **5.7** — ~~99 of 99 articles lack canonical URLs~~ **Done.** 101/101.

---

## 6. HIGH COHERENCE — Logical consistency across UI/UX/state

**Rating: ⚠️ Needs Work** (was ❌ Significant Issues — data and site-wide navigation are now coherent; per-article template sprawl remains)

### What works
- Homepage (`index.html`) has a clean, consistent design system
- Category filters and search work correctly
- Dark mode respects `prefers-color-scheme`
- Every article now shares the same breadcrumb/meta strip and "Related guides" footer, generated from one place

### Issues & Tasks
- [ ] **6.1** — **3 different template architectures** across articles:
  - `inline-custom` (majority — hand-rolled CSS)
  - `custom-css-vars` (CSS variable system)
  - `tailwind` (2 articles use Tailwind CDN)
  This creates visual inconsistency and makes maintenance extremely difficult.
- [x] **6.2** — ~~Category casing inconsistency~~ **Done.** All lowercase; the validator rejects anything else. Category labels/emojis live in `site.categories`.
- [x] **6.3** — ~~20 groups of duplicate article IDs~~ **Done.** 101 unique zero-padded ids (first occurrence kept its id, later duplicates got the lowest free id; the one integer id was normalised). Enforced by validator + CI.
- [x] **6.4** — ~~Article template structure is inconsistent~~ **Done at the site-chrome level:** every article now has a back link (Home crumb), category link, reading time, verified date, a standard footer section and a skip link, injected by `scripts/build.py`. The *inner* templates still differ (see 6.1).
- [ ] **6.5** — The README references articles/links that don't always match the current metadata (3 "guides" link to the homepage; only ~18 of 100 guides are listed) — generate the README catalog from `metadata.json`

---

## 7. HIGH QUALITY — Exceptional craftsmanship, no bugs

**Rating: ⚠️ Needs Work**

### What works
- Core index.html is well-crafted with smooth animations, responsive layout
- Good use of `prefers-reduced-motion` for accessibility
- Clean CSS custom properties design system

### Issues & Tasks
- [ ] **7.1** — `consistent-character-bible-nano-banana.html` is 201KB — it is a compiled React artifact (inlined Tailwind + `<script type="module">`), not a hand-written guide. Its `<title>` was "React Artifact" (fixed). Verify it renders without network access and rebuild as a normal article.
- [ ] **7.2** — 2 articles load `cdn.tailwindcss.com` externally — adds a runtime dependency and CSP concern
- [x] **7.3** — ~~Article IDs are not truly unique~~ **Done** (same fix as 6.3).
- [~] **7.4** — ~~No automated testing, linting, or CI/CD pipeline~~ `validate.yml` now runs `validate_metadata.py` and `build.py --check` on every push/PR. HTML validation, link checking and accessibility auditing are still open.
- [ ] **7.5** — No link checker — no way to verify external tool URLs haven't changed or died

---

## 8. HIGH PERFORMANCE — Minimal latency, optimal efficiency

**Rating: ⚠️ Needs Work**

### What works
- Static HTML with no JavaScript framework — inherently fast
- `metadata.json` is loaded once and filtered client-side
- Google Fonts use `display=swap` to avoid FOIT

### Issues & Tasks
- [ ] **8.1** — No asset bundling or minification — each article is a standalone HTML file with inline CSS/JS (duplicated across all 100+ files)
- [ ] **8.2** — Google Fonts loaded on every page (3 font families) — no font subsetting or local hosting
- [ ] **8.3** — No `<link rel="preload">` for critical resources
- [ ] **8.4** — No service worker or offline support — users lose access if network drops
- [ ] **8.5** — 2 articles load Tailwind CDN at runtime — generates CSS on-the-fly in the browser, adding ~200ms to paint
- [ ] **8.6** — No image optimization pipeline — articles with images (if any) are not compressed or served in modern formats (WebP/AVIF)
- [ ] **8.7** — 104 separate HTML files each duplicate ~5–10KB of boilerplate CSS — total redundancy is ~500KB–1MB of duplicated styles

---

## 9. HIGH RESILIENCE — Degrades gracefully

**Rating: ⚠️ Needs Work**

### What works
- `prefers-reduced-motion` respected for animations
- Search works client-side with no server dependency
- Theme defaults to system preference if no localStorage

### Issues & Tasks
- [x] **9.1** — ~~if `metadata.json` fails to load, the feed shows "No guides published yet"~~ **Done.** Distinct error state ("Couldn't load the guide list") with a retry button.
- [ ] **9.2** — No error boundary for individual article cards — if one card has bad data, it could break rendering of all subsequent cards
- [x] **9.3** — ~~No `404.html`~~ **Done** (see 5.1).
- [ ] **9.4** — External CDN dependency (Tailwind, FontAwesome, Google Fonts) — if any CDN is down, those 2 articles break or look unstyled
- [ ] **9.5** — No content security policy (CSP) headers — vulnerable to XSS via CDN injection

---

## 10. HIGH COMPOSABILITY — Integrates via open standards

**Rating: ✅ Strong** (was ❌ Missing)

### Issues & Tasks
- [x] **10.1** — ~~No RSS/Atom feed~~ **Done.** `feed.xml` (RSS 2.0, 50 newest, autodiscovery `<link>` on every page, linked in the topbar and footer).
- [x] **10.2** — ~~No `sitemap.xml`~~ **Done.** Generated from metadata (homepage + 100 published guides, `lastmod` = latest of date/verified).
- [x] **10.3** — ~~No `robots.txt`~~ **Done.**
- [x] **10.4** — ~~No structured data~~ **Done.** JSON-LD `Article` + `BreadcrumbList` on every article (`isAccessibleForFree`, `timeRequired`, tool as `SoftwareApplication` with a $0 offer); `WebSite` + `Organization` on the homepage. `HowTo`/`FAQPage` schemas remain an opportunity.
- [~] **10.5** — ~~No API or JSON endpoint~~ `metadata.json` is already a stable, documented JSON catalog (now canonically formatted, with `site.categories` and `site.redirects`). Documenting it as a public API is the remaining step.
- [x] **10.6** — ~~No Open Graph / Twitter Card meta tags on 97% of articles~~ **Done** (see 5.6).
- [ ] **10.7** — No `.well-known` directory or web manifest for PWA support
- [ ] **10.8** — The `metadata.json` is a flat array with no pagination or filtering API — works for 100 articles but won't scale

---

## 11. HIGH ACCESSIBILITY — Frictionless for all users

**Rating: ⚠️ Needs Work** (was ❌ Significant Gaps — homepage and site chrome are now solid; per-template article internals remain)

### What works
- Homepage has proper `<html lang="en">`, landmark roles (`<main>`, `<header>`, `<footer>`, and now `<nav>` ×2)
- Search input has a label; result count is an `aria-live` status region
- `prefers-reduced-motion` support
- Focus visible styles (`:focus-visible` ring on the homepage; skip links on every page)

### Issues & Tasks
- [x] **11.1** — ~~No skip-to-content link~~ **Done.** Homepage + all 101 articles (targets the article's `<main>`, else its `<h1>`, with `tabindex="-1"`).
- [x] **11.2** — ~~articles lack `aria-label` on buttons~~ **Done.** All 70 icon-only buttons (share "X"/🔗, theme ◐, step numbers, presets, close/info icons) now have labels. Buttons with visible text were deliberately left alone (visible text *is* their accessible name).
- [x] **11.3** — ~~No `<nav>` landmark on homepage~~ **Done** (`nav[aria-label="Primary"]`, `nav[aria-label="Footer"]`, filters in a labelled `role="group"`).
- [x] **11.4** — ~~Category filter chips use `<span>`~~ **Done.** `<button type="button" aria-pressed>`.
- [ ] **11.5** — No visible focus indicator override on some article templates (keyboard-only users can't see where focus is)
- [x] **11.6** — ~~Cost widget is marked `aria-hidden="true"`~~ **Done.** Exposed as a labelled group; struck-through prices read as "normally $29/mo".
- [~] **11.7** — ~~`--muted` (#8A8A8F) on `--paper` fails WCAG AA~~ Confirmed (3.29:1) and fixed on the homepage/404 (`--muted` → 4.86:1, `--green` → 4.92:1, `--coral` → 4.96:1). Per-article palettes still need a pass.
- [ ] **11.8** — No `prefers-contrast` media query support for high-contrast mode users
- [ ] **11.9** — Articles with embedded images lack alt text verification

---

## 12. HIGH ADAPTABILITY — Evolves easily without rewrite

**Rating: ❌ Significant Issues**

### What works
- Static site architecture is inherently simple to deploy
- `metadata.json` separates content data from presentation

### Issues & Tasks
- [ ] **12.1** — No build system, templating engine, or static site generator — every article is a standalone HTML file with duplicated inline CSS/JS; updating the design requires editing 100+ files
- [ ] **12.2** — No component abstraction — header, footer, theme toggle, share bar are copy-pasted across every article
- [ ] **12.3** — No content pipeline — articles appear to be hand-authored HTML; introducing a Markdown-to-HTML pipeline would dramatically improve authoring velocity
- [~] **12.4** — ~~No CI/CD automation~~ `validate.yml` (metadata validation + build freshness) added. Link checking, HTML validation and accessibility auditing still open.
- [ ] **12.5** — No versioning or changelog for article updates — impossible to track when free-tier limits change
- [ ] **12.6** — `.gitignore` is a generic Node.js template but the project has no `package.json` — should be cleaned up to match the actual project (Python ignores were appended; the Node block is still there)

---

## 13. HIGH CLARITY — Intuitive, zero onboarding needed

**Rating: ✅ Strong**

### What works
- Homepage immediately communicates value: "Real AI leverage. Actually free."
- Cost widget is an excellent clarity device — shows exactly what you save
- Category chips are intuitive and labeled
- Search is prominently placed
- Article hooks are clear and compelling

### Issues & Tasks
- [x] **13.1** — ~~No onboarding or "getting started" guidance~~ **Done.** "New here? How this works" strip (pick a task → use the free tool, with "zero-cost" defined → check the verified date) between the hero and the directory, linked from the topbar.
- [x] **13.2** — ~~Category emojis use generic mappings (`💼` for both career AND business)~~ **Done.** Business → 📈, Family → 👪, AI Tools → 🧰, Software Engineering → 💻 (the old map keyed `software_engineering` and never matched). Labels are friendly ("Civic & Legal", "AI Tools"). Uniqueness is enforced by the validator.
- [x] **13.3** — ~~No breadcrumb navigation on article pages~~ **Done.** Home › {emoji} Category › Title on all 101 articles, with matching `BreadcrumbList` JSON-LD; category crumbs deep-link to a pre-filtered homepage (`?category=`).
- [x] **13.4** — ~~Article pages lack "Related guides" or "Next steps"~~ **Done** (see 2.1).
- [x] **13.5** — ~~The pinned article … has no visual explanation of why it's special~~ **Done.** "📌 Pinned · Start here — the master catalog of every free model, chatbot and API the other guides build on" (text from `pinned_reason` in metadata).

---

## Priority Matrix

> **The live, prioritised backlog now lives in [`current-tasks-2026-10-08-1651.md`](./current-tasks-2026-10-08-1651.md).** The matrix below is kept as the audit's original plan with status.

### 🔴 Critical (fix first)
| # | Task | Dimension(s) | Status |
|---|---|---|---|
| 6.2 | Fix category casing inconsistency (`Creative` → `creative`, `Family` → `family`) | Coherence, Quality | ✅ Done |
| 6.3 | Deduplicate article IDs in metadata.json | Coherence, Quality | ✅ Done |
| 5.5 | Add `<meta name="description">` to all articles | Trust, Composability | ✅ Done |
| 5.6 | Add Open Graph tags to all articles | Trust, Composability | ✅ Done |
| 11.1 | Add skip-to-content link | Accessibility | ✅ Done |
| 11.4 | Convert filter chips to `<button>` elements | Accessibility | ✅ Done |
| 9.3 | Create a `404.html` error page | Resilience, Trust | ✅ Done |
| 5.2 | Add a favicon | Trust | ✅ Done |
| 10.2 | Add `sitemap.xml` | Composability | ✅ Done |
| 10.3 | Add `robots.txt` | Composability | ✅ Done |

### 🟡 High Impact (next)
| # | Task | Dimension(s) | Status |
|---|---|---|---|
| 1.1 | Publish or remove 4 orphaned HTML files | Utility | ✅ Done (1 published, 3 removed + redirected) |
| 4.1 | Re-verify 24 articles with pre-2026 verification dates | Integrity, Trust | 🟡 Automatic staleness warnings shipped; human re-verification open |
| 6.4 | Standardize article template (back link, footer, reading time) | Coherence | ✅ Done (shared chrome on all 101 articles) |
| 10.1 | Add RSS/Atom feed | Composability | ✅ Done |
| 10.4 | Add JSON-LD structured data (Schema.org Article) | Composability | ✅ Done |
| 11.2 | Add `aria-label` to all interactive buttons | Accessibility | ✅ Done (all icon-only buttons) |
| 11.6 | Remove `aria-hidden` from cost widget (or add accessible alternative) | Accessibility | ✅ Done |
| 12.1 | Adopt a static site generator (11ty, Astro, or Hugo) | Adaptability | ⬜ Open (not in this PR's scope) |

### 🟢 Nice to Have
| # | Task | Dimension(s) | Status |
|---|---|---|---|
| 2.1 | Add internal cross-linking between related articles | Leverage | ✅ Done |
| 2.2 | Create "workflow bundle" collections | Leverage | ⬜ Open |
| 3.1 | Add local bookmark/favorites feature | Agency | ⬜ Open |
| 3.2 | Add print-friendly styles | Agency | ⬜ Open |
| 8.1 | Bundle and minify shared CSS/JS | Performance | ⬜ Open |
| 8.4 | Add service worker for offline support | Performance, Resilience | ⬜ Open |
| 13.1 | Add a brief "What is this?" intro for first-time visitors | Clarity | ✅ Done |
| 13.4 | Add "Related guides" section to article pages | Clarity, Leverage | ✅ Done |
| 4.2 | Add analytics disclosure / privacy policy | Integrity | ⬜ Open |

---

## Appendix: Data Quality Issues

### Duplicate IDs in `metadata.json` — ✅ resolved
~~These IDs are shared by multiple articles and should be made unique~~ (was 20 groups; "0054" alone was shared by 8 articles). All 101 ids are now unique; `python3 scripts/validate_metadata.py` fails CI if a duplicate is ever reintroduced.

### Category Casing Mismatches — ✅ resolved
`Creative` → `creative`, `Family` → `family`. Categories are now defined once in `metadata.json` → `site.categories` (label + distinct emoji) and validated.

### Articles Needing Re-verification — 🟡 flagged automatically, re-check still open
Guides verified more than 12 months before the build date are flagged on their card and page. As of 2026-10-08 that is **23** guides (the audit's 24th, `turn-textbook-into-socratic-tutor`, was verified 2025-12-11 and is still inside the 12-month window). Re-checking the provider docs and refreshing `verified` in `metadata.json` + the in-article text is the remaining human task. Original list (pre-2026 rule):
- `turn-receipts-into-spreadsheet-data-for-free` (verified 2023-10-15)
- `decode-legal-jargon-for-free` (verified 2023-11-28)
- `practice-interview-answers-out-loud-for-free` (verified 2024-01-20)
- `turn-40-page-pdf-into-plain-language-answers` (verified 2024-02-14)
- `transcribe-audio-files-for-free` (verified 2024-02-12)
- `turn-any-textbook-into-a-practice-quiz` (verified 2024-05-19)
- `turn-dense-pdfs-into-study-notes` (verified 2024-05-19)
- `generate-art-reference-photos-for-free` (verified 2024-04-05)
- `turn-business-idea-into-landing-page` (verified 2025-01-28)
- `turn-food-photo-into-nutrition-label` (verified 2025-03-17)
- `turn-health-screenshots-into-pattern-reports` (verified 2025-03-18)
- `stop-describing-start-showing-free-consistent-characters` (verified 2025-06-12)
- `never-ask-if-its-fine-free-contract-triage-with-claude` (verified 2025-06-19)
- `free-flight-delay-compensation-claims-with-gemini` (verified 2025-06-17)
- `free-debt-collection-dispute-letters-with-claude` (verified 2025-06-17)
- `free-ai-accessibility-accommodation-requests` (verified 2025-06-17)
- `free-family-meal-planning-with-claude` (verified 2025-06-17)
- `free-business-document-analysis-with-google-gemini` (verified 2025-06-17)
- `the-eleven-second-window-free-doctor-visit-prep-with-gemini` (verified 2025-07-03)
- `free-ai-travel-planning-google-maps` (verified 2025-07-18)
- `translate-foreign-menus-flag-allergens-photos-travel` (verified 2025-07-18)
- `decode-graded-exams-find-recurring-mistake-patterns` (verified 2025-07-19)
- `ask-what-they-witnessed-free-family-oral-history-with-chatgpt` (verified 2025-06-26)
- `turn-textbook-into-socratic-tutor` (verified 2025-12-11)

### Infrastructure
| Asset | At audit | Now |
|---|---|---|
| `sitemap.xml` | ❌ Missing | ✅ Generated by `scripts/build.py` |
| `robots.txt` | ❌ Missing | ✅ Present |
| `404.html` | ❌ Missing | ✅ Present (search, suggestions, redirects) |
| `favicon.ico` / `favicon.svg` / `apple-touch-icon.png` | ❌ Missing | ✅ Present |
| `manifest.json` | ❌ Missing | ❌ Still missing (icons now exist, so this is cheap) |
| `feed.xml` | ❌ Missing | ✅ Generated (RSS 2.0) |
| `og-image.png` | ❌ Missing | ✅ Present |
| `privacy.html` | ❌ Missing | ❌ Still missing |
| `package.json` | ❌ Missing (`.gitignore` assumes Node.js) | — Not needed: tooling is stdlib Python (`scripts/`); `.gitignore` still carries the Node template |
| CI/CD (GitHub Actions) | ❌ Missing | ✅ `validate.yml` (metadata + build freshness); link/HTML/a11y checks still open |
| `.nojekyll` | — | ✅ Added (plain static deploy) |

---

*Audit generated automatically on 2026-10-08; status updated 2026-10-08 16:51 CDT after the remediation PR. This is a living document — update as tasks are completed. The prioritised backlog is maintained in `current-tasks-2026-10-08-1651.md`.*