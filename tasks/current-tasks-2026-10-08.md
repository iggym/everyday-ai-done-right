# Project Audit: Everyday AI, Done Right

**Date:** 2026-10-08  
**Scope:** Full site audit across 13 quality dimensions  
**Files reviewed:** `index.html`, `metadata.json` (100 articles), 104 article HTML files, `README.md`, `.gitignore`, `LICENSE`  
**Repository:** `iggym/everyday-ai-done-right` (GitHub Pages static site)

---

## Executive Summary

Everyday AI, Done Right is a curated directory of 99 published zero-cost AI workflows delivered as a static site on GitHub Pages. The core value proposition is strong — verified, genuinely-free AI guides for real people. The site performs well functionally, but has significant gaps in metadata consistency, SEO infrastructure, accessibility compliance, and architectural coherence that limit discoverability, trust signals, and maintainability.

### Current Stats
| Metric | Value |
|---|---|
| Total articles in metadata | 100 |
| Published | 99 |
| Drafts | 1 |
| HTML files on disk | 104 (4 orphaned) |
| Categories | 14 (with casing inconsistencies) |
| Articles needing re-verification (pre-2026) | 24 |
| Duplicate IDs in metadata | 20 groups |

---

## 1. HIGH UTILITY — Solves a pressing problem effectively

**Rating: ✅ Strong**

### What works
- Covers genuinely high-value use cases: resume building, medical bill audits, debt collection defense, meal planning, legal self-help, accessibility tools
- Every guide targets a real, costly problem people pay $12–$79/month for
- Clear hooks in metadata ("Stop doing manual data entry…", "FDCPA violations…")

### Issues & Tasks
- [ ] **1.1** — 4 orphaned HTML files exist but are not in metadata, meaning users cannot discover them:
  - `articles/build-custom-web-tools-without-coding-for-free.html`
  - `articles/build-the-tool-that-doesnt-exist-yet.html`
  - `articles/read-foreign-signs-instantly-for-free.html`
  - `articles/source-grounded-ai-study-engine.html`
- [ ] **1.2** — 1 article is in `draft` status (`plan-week-trip-gemini-flash`) — evaluate whether to publish or remove
- [ ] **1.3** — No feedback mechanism (issue template, rating, or contact link) for users to report broken workflows or out-of-date pricing
- [ ] **1.4** — Some categories have only 1 article (`ai-tools`, `software-engineering`) — consider merging or expanding

---

## 2. HIGH LEVERAGE — Multiplies user effort with scalable results

**Rating: ✅ Strong**

### What works
- Clear "What this replaces" cost widget on homepage
- Each article is a standalone workflow users can follow immediately
- Categories cover career, health, legal, learning, household — high-leverage life domains

### Issues & Tasks
- [ ] **2.1** — No internal cross-linking between related articles (e.g., resume articles linking to each other, meal planning linking to nutrition tracking)
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
- [ ] **4.1** — **24 articles have verification dates from 2023–2025** — free-tier pricing changes frequently; these need re-verification or a prominent staleness warning
- [ ] **4.2** — Cloudflare Web Analytics is injected in `index.html` but not disclosed in a privacy policy — add a brief analytics disclosure
- [ ] **4.3** — No `robots.txt` or `sitemap.xml` — adding them improves transparency with crawlers

---

## 5. HIGH TRUST — Consistently delivers on promises

**Rating: ⚠️ Needs Work**

### What works
- Strong "Verified" badges on cards
- Honest language about limitations

### Issues & Tasks
- [ ] **5.1** — No `404.html` error page — broken links give the default GitHub Pages 404, which looks unprofessional and erodes trust
- [ ] **5.2** — No favicon — browsers show a generic tab icon, reducing brand recognition and trust
- [ ] **5.3** — No Open Graph image (`og:image`) — social shares show no preview image
- [ ] **5.4** — No privacy policy or terms page — especially needed since Cloudflare analytics is used
- [ ] **5.5** — 76 of 99 articles lack `<meta name="description">` — search engines may show poor snippets
- [ ] **5.6** — 97 of 99 articles lack Open Graph tags (`og:title`, `og:description`) — poor social sharing previews
- [ ] **5.7** — 99 of 99 articles lack canonical URLs — risk of duplicate content penalties

---

## 6. HIGH COHERENCE — Logical consistency across UI/UX/state

**Rating: ❌ Significant Issues**

### What works
- Homepage (`index.html`) has a clean, consistent design system
- Category filters and search work correctly
- Dark mode respects `prefers-color-scheme`

### Issues & Tasks
- [ ] **6.1** — **3 different template architectures** across articles:
  - `inline-custom` (majority — hand-rolled CSS)
  - `custom-css-vars` (CSS variable system)
  - `tailwind` (2 articles use Tailwind CDN)
  This creates visual inconsistency and makes maintenance extremely difficult.
- [ ] **6.2** — **Category casing inconsistency**: `'Creative'` vs `'creative'`, `'Family'` vs `'family'` — this breaks filter chips on the homepage (the EMOJI_MAP is case-sensitive)
- [ ] **6.3** — **20 groups of duplicate article IDs** in metadata.json — IDs should be unique identifiers
- [ ] **6.4** — Article template structure is inconsistent across articles:
  - Some have back-to-home navigation, many don't
  - Some have footers, none consistently
  - Some show reading time, many don't
  - No standardized article layout pattern
- [ ] **6.5** — The README references articles/links that don't always match the current metadata (e.g., some README sections point to tools that aren't in the live directory)

---

## 7. HIGH QUALITY — Exceptional craftsmanship, no bugs

**Rating: ⚠️ Needs Work**

### What works
- Core index.html is well-crafted with smooth animations, responsive layout
- Good use of `prefers-reduced-motion` for accessibility
- Clean CSS custom properties design system

### Issues & Tasks
- [ ] **7.1** — `consistent-character-bible-nano-banana.html` is 201KB — excessively large for a single article page, likely contains inlined images or heavy markup
- [ ] **7.2** — 2 articles load `cdn.tailwindcss.com` externally — adds a runtime dependency and CSP concern
- [ ] **7.3** — Article IDs are not truly unique — the `id` field is reused across multiple articles (e.g., `"0054"` appears 8 times) — this could break any ID-based lookup or deduplication
- [ ] **7.4** — No automated testing, linting, or CI/CD pipeline for content quality
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
- [ ] **9.1** — No offline fallback — if `metadata.json` fails to load, the feed shows "No guides published yet" which is misleading (should show a retry/message)
- [ ] **9.2** — No error boundary for individual article cards — if one card has bad data, it could break rendering of all subsequent cards
- [ ] **9.3** — No `404.html` — GitHub Pages shows an ugly default for missing routes
- [ ] **9.4** — External CDN dependency (Tailwind, FontAwesome, Google Fonts) — if any CDN is down, those 2 articles break or look unstyled
- [ ] **9.5** — No content security policy (CSP) headers — vulnerable to XSS via CDN injection

---

## 10. HIGH COMPOSABILITY — Integrates via open standards

**Rating: ❌ Missing**

### Issues & Tasks
- [ ] **10.1** — No RSS/Atom feed — users and aggregators cannot subscribe to new articles
- [ ] **10.2** — No `sitemap.xml` — search engines cannot efficiently discover all 100+ pages
- [ ] **10.3** — No `robots.txt` — no crawl directives for search engines
- [ ] **10.4** — No structured data (JSON-LD / Schema.org) — search engines miss rich snippet opportunities (HowTo, Article, FAQPage schemas)
- [ ] **10.5** — No API or JSON endpoint for the article catalog — third-party tools cannot programmatically consume the directory
- [ ] **10.6** — No Open Graph / Twitter Card meta tags on 97% of articles — poor social media integration
- [ ] **10.7** — No `.well-known` directory or web manifest for PWA support
- [ ] **10.8** — The `metadata.json` is a flat array with no pagination or filtering API — works for 100 articles but won't scale

---

## 11. HIGH ACCESSIBILITY — Frictionless for all users

**Rating: ❌ Significant Gaps**

### What works
- Homepage has proper `<html lang="en">`, landmark roles (`<main>`, `<header>`, `<footer>`)
- Search input has `aria-label`
- `prefers-reduced-motion` support
- Focus visible styles

### Issues & Tasks
- [ ] **11.1** — No skip-to-content link on homepage or articles
- [ ] **11.2** — 99 of 99 articles lack `aria-label` on buttons (theme toggle, share buttons)
- [ ] **11.3** — No `<nav>` landmark on homepage — screen readers cannot identify navigation
- [ ] **11.4** — Category filter chips use `<span>` with click handlers — should be `<button>` elements for keyboard/screen-reader accessibility
- [ ] **11.5** — No visible focus indicator override on some article templates (keyboard-only users can't see where focus is)
- [ ] **11.6** — Cost widget is marked `aria-hidden="true"` — screen readers miss the key value proposition
- [ ] **11.7** — Color contrast in light mode: `--muted` (#8A8A8F) on `--paper` (#FAFAF9) may fail WCAG AA for normal text
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
- [ ] **12.4** — No CI/CD automation — no GitHub Actions for link checking, HTML validation, accessibility auditing, or deployment
- [ ] **12.5** — No versioning or changelog for article updates — impossible to track when free-tier limits change
- [ ] **12.6** — `.gitignore` is a generic Node.js template but the project has no `package.json` — should be cleaned up to match the actual project

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
- [ ] **13.1** — No onboarding or "getting started" guidance for first-time visitors — the site assumes users understand what "verified zero-cost AI workflows" means
- [ ] **13.2** — Category emojis use generic mappings (`💼` for both career AND business) — confusing
- [ ] **13.3** — No breadcrumb navigation on article pages — users can't easily see where they are in the site hierarchy
- [ ] **13.4** — Article pages lack "Related guides" or "Next steps" — dead-end navigation after reading
- [ ] **13.5** — The pinned article (`zero-cost-ai-catalog-and-schema`) spans full width (`grid-column: 1/-1`) but has no visual explanation of why it's special

---

## Priority Matrix

### 🔴 Critical (fix first)
| # | Task | Dimension(s) |
|---|---|---|
| 6.2 | Fix category casing inconsistency (`Creative` → `creative`, `Family` → `family`) | Coherence, Quality |
| 6.3 | Deduplicate article IDs in metadata.json | Coherence, Quality |
| 5.5 | Add `<meta name="description">` to all articles | Trust, Composability |
| 5.6 | Add Open Graph tags to all articles | Trust, Composability |
| 11.1 | Add skip-to-content link | Accessibility |
| 11.4 | Convert filter chips to `<button>` elements | Accessibility |
| 9.3 | Create a `404.html` error page | Resilience, Trust |
| 5.2 | Add a favicon | Trust |
| 10.2 | Add `sitemap.xml` | Composability |
| 10.3 | Add `robots.txt` | Composability |

### 🟡 High Impact (next)
| # | Task | Dimension(s) |
|---|---|---|
| 1.1 | Publish or remove 4 orphaned HTML files | Utility |
| 4.1 | Re-verify 24 articles with pre-2026 verification dates | Integrity, Trust |
| 6.4 | Standardize article template (back link, footer, reading time) | Coherence |
| 10.1 | Add RSS/Atom feed | Composability |
| 10.4 | Add JSON-LD structured data (Schema.org Article) | Composability |
| 11.2 | Add `aria-label` to all interactive buttons | Accessibility |
| 11.6 | Remove `aria-hidden` from cost widget (or add accessible alternative) | Accessibility |
| 12.1 | Adopt a static site generator (11ty, Astro, or Hugo) | Adaptability |

### 🟢 Nice to Have
| # | Task | Dimension(s) |
|---|---|---|
| 2.1 | Add internal cross-linking between related articles | Leverage |
| 2.2 | Create "workflow bundle" collections | Leverage |
| 3.1 | Add local bookmark/favorites feature | Agency |
| 3.2 | Add print-friendly styles | Agency |
| 8.1 | Bundle and minify shared CSS/JS | Performance |
| 8.4 | Add service worker for offline support | Performance, Resilience |
| 13.1 | Add a brief "What is this?" intro for first-time visitors | Clarity |
| 13.4 | Add "Related guides" section to article pages | Clarity, Leverage |
| 4.2 | Add analytics disclosure / privacy policy | Integrity |

---

## Appendix: Data Quality Issues

### Duplicate IDs in `metadata.json`
These IDs are shared by multiple articles and should be made unique:
```
"0001" → 6 articles
"0002" → 5 articles
"0003" → 5 articles
"0054" → 8 articles
"0014" → 4 articles
"0004" → 3 articles
"0055" → 3 articles
(and 13 more groups with 2 each)
```

### Category Casing Mismatches
| Current | Should Be |
|---|---|
| `Creative` | `creative` |
| `Family` | `family` |

### Articles Needing Re-verification (pre-2026)
24 articles last verified before January 2026 — free-tier limits change frequently and these may no longer be accurate:
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

### Missing Infrastructure
| Asset | Status |
|---|---|
| `sitemap.xml` | ❌ Missing |
| `robots.txt` | ❌ Missing |
| `404.html` | ❌ Missing |
| `favicon.ico` | ❌ Missing |
| `manifest.json` | ❌ Missing |
| `feed.xml` / `atom.xml` | ❌ Missing |
| `og-image.png` | ❌ Missing |
| `privacy.html` | ❌ Missing |
| `package.json` | ❌ Missing (`.gitignore` assumes Node.js) |
| CI/CD (GitHub Actions) | ❌ Missing |

---

*Audit generated automatically on 2026-10-08. This is a living document — update as tasks are completed.*