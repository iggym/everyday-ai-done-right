#!/usr/bin/env python3
"""Site build step for Everyday AI, Done Right.

Reads ``metadata.json`` and:

1. Injects a standard, self-contained "chrome" into every article page
   (idempotent - re-running replaces the previous injection):
     * <head>: meta description (when missing), canonical URL, Open Graph +
       Twitter Card tags, favicon links, RSS autodiscovery, JSON-LD
       (Article + BreadcrumbList), ``noindex`` for drafts.
     * top of <body>: skip-to-content link, breadcrumb nav
       (Home › Category › Title), reading time + verified date, and a
       staleness notice when the guide was verified > 12 months ago.
     * end of article: "Related guides" (3 nearest by category / tags /
       tool) plus "Next steps" links and a report-a-problem link.
2. Adds ``aria-label`` to icon-only buttons (share / copy / theme / step
   buttons whose only visible content is a glyph or a number).
3. Generates ``sitemap.xml`` and ``feed.xml`` (RSS 2.0).

Usage:
    python3 scripts/build.py            # build everything
    python3 scripts/build.py --check    # exit 1 if any file would change

Standard library only.  Line endings of each article (LF or CRLF) are
preserved.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "metadata.json"
ARTICLES = ROOT / "articles"

STALE_AFTER_DAYS = 365
RELATED_COUNT = 3
FEED_ITEMS = 50
GITHUB_REPO = "https://github.com/iggym/everyday-ai-done-right"

# Staleness is computed as of the build date. The date is recorded in each page
# (data-built) so that --check can re-render "as of" the committed build date and
# stay deterministic; the tiny inline script keeps the warning correct at view time.
TODAY = dt.date.today()

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def fmt_date(iso: str) -> str:
    try:
        return dt.date.fromisoformat(iso).strftime("%b %-d, %Y")
    except ValueError:
        return iso


def truncate(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:—-") + "…"


def is_stale(verified: str, today: dt.date) -> bool:
    try:
        return (today - dt.date.fromisoformat(verified)).days > STALE_AFTER_DAYS
    except ValueError:
        return False


def age_phrase(verified: str, today: dt.date) -> str:
    days = (today - dt.date.fromisoformat(verified)).days
    years = days // 365
    months = days // 30
    if years >= 2:
        return f"over {years} years ago"
    if years == 1:
        return "over a year ago"
    return f"{months} months ago"


def has_tag(doc: str, pattern: str) -> bool:
    return re.search(pattern, doc, re.I) is not None


def strip_block(doc: str, name: str) -> str:
    """Remove a previously injected block. Blocks are always inserted at the start
    of a line and end with a newline, so removing exactly the block is lossless."""
    return re.sub(rf"<!-- eadr:{name}:start -->.*?<!-- eadr:{name}:end -->\n", "", doc, flags=re.S)


def line_start(doc: str, pos: int) -> int:
    return doc.rfind("\n", 0, pos) + 1


# --------------------------------------------------------------------------- #
# CSS for the injected chrome - namespaced, theme-agnostic (inherits the page's
# own text colour so it works with every template's light/dark toggle).
# Every element type we use is reset first because many templates style bare
# ``a``, ``p``, ``h2``, ``ul``, ``li`` and ``section`` selectors.
# --------------------------------------------------------------------------- #
NAV_CSS = """
.eadr-nav,.eadr-nav *,.eadr-stale,.eadr-stale *{box-sizing:border-box}
.eadr-nav,.eadr-nav div,.eadr-nav ol,.eadr-nav li,.eadr-nav a,.eadr-nav span,.eadr-stale,.eadr-stale a{margin:0;padding:0;border:0;background:none;list-style:none;position:static;text-align:left;max-width:none;color:inherit;font-size:inherit;text-transform:none;letter-spacing:normal;text-shadow:none;box-shadow:none;text-decoration:none;border-radius:0;transform:none;counter-increment:none;float:none;width:auto;min-height:0;height:auto}
.eadr-nav li::before,.eadr-nav li::after{content:none;display:none}
.eadr-skip{position:absolute;left:-10000px;top:12px;z-index:10000;padding:10px 16px;border-radius:8px;background:#0F8A5F;color:#fff;font:600 14px/1 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;text-decoration:none}
.eadr-skip:focus{left:12px;outline:3px solid #FF6B4A;outline-offset:2px}
.eadr-nav{display:block;font:500 13px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;border-bottom:1px solid rgba(127,127,127,.28)}
.eadr-nav-inner{display:flex;align-items:center;justify-content:space-between;gap:8px 18px;flex-wrap:wrap;max-width:880px;margin:0 auto;padding:10px 20px}
.eadr-crumbs{display:flex;align-items:center;flex-wrap:wrap;gap:6px;min-width:0}
.eadr-crumbs li{display:inline-flex;align-items:center;gap:6px;min-width:0}
.eadr-crumbs li+li::before{content:"\\203A";display:inline;opacity:.45}
.eadr-crumbs a{display:inline;opacity:.78;border-bottom:1px solid transparent;white-space:nowrap}
.eadr-crumbs a:hover,.eadr-crumbs a:focus-visible{opacity:1;border-bottom-color:currentColor}
.eadr-crumbs [aria-current]{display:inline-block;opacity:.62;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:min(44ch,62vw)}
.eadr-meta{display:inline-flex;align-items:center;gap:12px;font:500 11.5px/1 "JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;opacity:.72;white-space:nowrap}
.eadr-stale{display:none;max-width:840px;margin:14px auto 0;padding:12px 16px;border:1px solid rgba(255,107,74,.45);border-left:5px solid #FF6B4A;border-radius:12px;background:rgba(255,107,74,.10);font:500 13.5px/1.55 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
.eadr-stale.eadr-show{display:block}
.eadr-stale a{text-decoration:underline;font-weight:600}
@media (max-width:640px){.eadr-nav-inner{padding:10px 16px}.eadr-meta{opacity:.65}}
@media print{.eadr-nav,.eadr-stale,.eadr-related,.eadr-skip,.theme-toggle,button,header nav,footer{display:none!important}a[href^="http"]::after{content:" (" attr(href) ")";font-size:.85em;opacity:.8;word-break:break-all}}
""".strip()

RELATED_CSS = """
.eadr-related,.eadr-related *{box-sizing:border-box}
.eadr-related,.eadr-related div,.eadr-related ul,.eadr-related li,.eadr-related a,.eadr-related p,.eadr-related h2,.eadr-related span,.eadr-related strong{margin:0;padding:0;border:0;background:none;list-style:none;position:static;text-align:left;max-width:none;color:inherit;font-size:inherit;text-transform:none;letter-spacing:normal;text-shadow:none;box-shadow:none;text-decoration:none;border-radius:0;transform:none;counter-increment:none;float:none;width:auto;min-height:0;height:auto;line-height:1.5}
.eadr-related li::before,.eadr-related li::after,.eadr-related h2::before,.eadr-related h2::after{content:none;display:none}
.eadr-related{display:block;font:400 15px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;border-top:1px solid rgba(127,127,127,.28);margin-top:56px;padding:40px 20px 28px}
.eadr-related-inner{max-width:880px;margin:0 auto}
.eadr-kicker{display:block;font:600 11px/1 "JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin:0 0 8px}
.eadr-related h2{display:block;font:800 1.35rem/1.25 Manrope,Inter,system-ui,sans-serif;letter-spacing:-.01em;margin:0 0 18px}
.eadr-related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.eadr-related-grid li{display:block}
.eadr-related-grid a{display:flex;flex-direction:column;gap:8px;height:100%;padding:16px 18px;border:1px solid rgba(127,127,127,.3);border-radius:14px;transition:border-color .2s ease,transform .2s ease}
.eadr-related-grid a:hover,.eadr-related-grid a:focus-visible{border-color:#0F8A5F;transform:translateY(-2px)}
.eadr-rel-cat{display:block;font:600 10.5px/1.3 "JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;opacity:.65}
.eadr-related-grid strong{display:block;font:700 15px/1.35 Manrope,Inter,system-ui,sans-serif}
.eadr-rel-hook{display:block;font-size:13px;line-height:1.5;opacity:.75}
.eadr-next{display:flex;flex-wrap:wrap;gap:10px 22px;margin:26px 0 0;font-size:14px}
.eadr-next a{display:inline;font-weight:600;border-bottom:1px solid rgba(127,127,127,.45)}
.eadr-next a:hover,.eadr-next a:focus-visible{border-bottom-color:currentColor}
.eadr-foot-meta{display:block;margin:26px 0 0;font:500 12px/1.6 "JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;opacity:.62}
.eadr-foot-meta a{display:inline;text-decoration:underline}
@media (prefers-reduced-motion:reduce){.eadr-related-grid a{transition:none}.eadr-related-grid a:hover{transform:none}}
""".strip()

STALE_JS = (
    "(function(){var n=document.querySelector('.eadr-nav[data-verified]');if(!n)return;"
    "var v=new Date(n.getAttribute('data-verified')+'T00:00:00');if(isNaN(v))return;"
    "if((Date.now()-v)/864e5>%d){var s=document.querySelector('.eadr-stale');if(s)s.classList.add('eadr-show');}})();"
    % STALE_AFTER_DAYS
)


# --------------------------------------------------------------------------- #
# per-article fragments
# --------------------------------------------------------------------------- #
class Site:
    def __init__(self, data: dict):
        s = data["site"]
        self.title = s["title"]
        self.base = s["base_url"].rstrip("/") + "/"
        self.description = s["description"]
        self.categories = s.get("categories", {})
        self.articles = data["articles"]
        self.published = [a for a in self.articles if a["status"] == "published"]

    def cat_label(self, cat: str) -> str:
        meta = self.categories.get(cat)
        return meta["label"] if meta else cat.replace("-", " ").title()

    def cat_emoji(self, cat: str) -> str:
        meta = self.categories.get(cat)
        return meta["emoji"] if meta else "💡"

    def url(self, a: dict) -> str:
        return self.base + a["path"]

    def image(self, a: dict) -> str:
        """Per-guide social card (og/<slug>.png, see make_social_cards.py) or the site default."""
        if (ROOT / "og" / f"{a['slug']}.png").is_file():
            return f"{self.base}og/{a['slug']}.png"
        return self.base + "og-image.png"


def related_for(site: Site, a: dict) -> list[dict]:
    """Nearest guides: same category (+5), shared tags (+2 each), same tool family (+1), same tool (+1).
    Ties go to the newer guide; the pinned catalog is excluded (it is linked separately)."""
    tags = set(a.get("tags", []))

    def score(b: dict) -> int:
        s = 5 if b["category"] == a["category"] else 0
        s += 2 * len(tags & set(b.get("tags", [])))
        s += 1 if b["tool_family"] == a["tool_family"] else 0
        s += 1 if b["tool"] == a["tool"] else 0
        return s

    pool = [b for b in site.published if b["slug"] != a["slug"] and not b.get("pinned")]
    pool.sort(key=lambda b: (-score(b), -int(b["date"].replace("-", "")), b["slug"]))
    return pool[:RELATED_COUNT]


def head_block(site: Site, a: dict, doc: str) -> str:
    url = site.url(a)
    existing_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', doc, re.I)
    desc = html.unescape(existing_desc.group(1)) if existing_desc else truncate(a["hook"], 155)
    og_desc = truncate(desc, 200)
    cat_label = site.cat_label(a["category"])
    img = site.image(a)
    lines = [f"<!-- eadr:head:start -->"]
    if not existing_desc:
        lines.append(f'<meta name="description" content="{esc(desc)}">')
    if a["status"] != "published":
        lines.append('<meta name="robots" content="noindex, nofollow">')
    if not has_tag(doc, r'rel=["\']canonical["\']'):
        lines.append(f'<link rel="canonical" href="{esc(url)}">')
    if not has_tag(doc, r'property=["\']og:title["\']'):
        lines += [
            '<meta property="og:type" content="article">',
            f'<meta property="og:site_name" content="{esc(site.title)}">',
            f'<meta property="og:title" content="{esc(a["title"])}">',
            f'<meta property="og:description" content="{esc(og_desc)}">',
            f'<meta property="og:url" content="{esc(url)}">',
        ]
    if not has_tag(doc, r'rel=["\']manifest["\']'):
        lines += ['<link rel="manifest" href="../manifest.webmanifest">', '<meta name="theme-color" content="#0F8A5F">']
    if not has_tag(doc, r'property=["\']og:image["\']'):
        lines += [
            f'<meta property="og:image" content="{esc(img)}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{esc(site.title)} — Real AI leverage. Actually free.">',
        ]
    if not has_tag(doc, r'property=["\']article:published_time["\']'):
        lines += [
            f'<meta property="article:published_time" content="{a["date"]}">',
            f'<meta property="article:modified_time" content="{a["verified"]}">',
            f'<meta property="article:section" content="{esc(cat_label)}">',
        ] + [f'<meta property="article:tag" content="{esc(t)}">' for t in a.get("tags", [])]
    if not has_tag(doc, r'name=["\']twitter:card["\']'):
        lines += [
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{esc(a["title"])}">',
            f'<meta name="twitter:description" content="{esc(og_desc)}">',
            f'<meta name="twitter:image" content="{esc(img)}">',
        ]
    if not has_tag(doc, r'rel=["\'](?:shortcut )?icon["\']'):
        lines += [
            '<link rel="icon" href="../favicon.ico" sizes="32x32">',
            '<link rel="icon" href="../favicon.svg" type="image/svg+xml">',
            '<link rel="apple-touch-icon" href="../apple-touch-icon.png">',
        ]
    if not has_tag(doc, r'type=["\']application/rss\+xml["\']'):
        lines.append(f'<link rel="alternate" type="application/rss+xml" title="{esc(site.title)}" href="../feed.xml">')
    if "application/ld+json" not in doc:
        ld = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "@id": url + "#article",
                    "headline": a["title"],
                    "description": desc,
                    "url": url,
                    "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                    "datePublished": a["date"],
                    "dateModified": a["verified"],
                    "author": {"@type": "Organization", "name": site.title, "url": site.base},
                    "publisher": {
                        "@type": "Organization",
                        "name": site.title,
                        "url": site.base,
                        "logo": {"@type": "ImageObject", "url": site.base + "apple-touch-icon.png", "width": 180, "height": 180},
                    },
                    "image": img,
                    "articleSection": cat_label,
                    "keywords": ", ".join(a.get("tags", [])),
                    "timeRequired": f"PT{int(a.get('reading_time_minutes') or 3)}M",
                    "isAccessibleForFree": True,
                    "about": {"@type": "SoftwareApplication", "name": a["tool"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": site.base},
                        {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"{site.base}?category={a['category']}"},
                        {"@type": "ListItem", "position": 3, "name": a["title"], "item": url},
                    ],
                },
            ],
        }
        ld_json = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        lines.append(f'<script type="application/ld+json">{ld_json}</script>')
    lines.append("<!-- eadr:head:end -->")
    return "\n".join(lines) + "\n"


def nav_block(site: Site, a: dict, skip_target: str, today: dt.date, add_anchor: bool = False) -> str:
    cat = a["category"]
    cat_label = site.cat_label(cat)
    stale = is_stale(a["verified"], today)
    verified_txt = f'{"⚠" if stale else "✓"} verified {fmt_date(a["verified"])}'
    mins = a.get("reading_time_minutes")
    issue_url = esc(
        f"{GITHUB_REPO}/issues/new?title={quote_plus('Outdated limit: ' + a['slug'])}"
        f"&body={quote_plus('Which limit changed? Please link the provider page showing the current free tier.')}"
    )
    stale_box = (
        f'<div class="eadr-stale{" eadr-show" if stale else ""}" role="note">'
        f'<strong>Heads up:</strong> this guide was last verified on {fmt_date(a["verified"])}'
        f'{" — " + age_phrase(a["verified"], today) if stale else ""}. Free-tier limits change often — re-check the '
        f'provider\'s current pricing page before relying on it. '
        f'<a href="{issue_url}" rel="noopener">Report an outdated limit</a>.'
        f"</div>"
    )
    return (
        "<!-- eadr:nav:start -->\n"
        f"<style>{NAV_CSS}</style>\n"
        f'<a class="eadr-skip" href="#{skip_target}">Skip to content</a>\n'
        f'<nav class="eadr-nav" aria-label="Breadcrumb" data-verified="{a["verified"]}" data-built="{today.isoformat()}">\n'
        '  <div class="eadr-nav-inner">\n'
        '    <ol class="eadr-crumbs">\n'
        '      <li><a href="../index.html">Home</a></li>\n'
        f'      <li><a href="../index.html?category={esc(cat)}">{site.cat_emoji(cat)} {esc(cat_label)}</a></li>\n'
        f'      <li><span aria-current="page" title="{esc(a["title"])}">{esc(a["title"])}</span></li>\n'
        "    </ol>\n"
        f'    <div class="eadr-meta">{f"<span>{mins} min read</span>" if mins else ""}<span>{verified_txt}</span></div>\n'
        "  </div>\n"
        "</nav>\n"
        f"{stale_box}\n"
        f"<script>{STALE_JS}</script>\n"
        + ('<span id="eadr-content" tabindex="-1"></span>\n' if add_anchor else "")
        + "<!-- eadr:nav:end -->\n"
    )


def related_block(site: Site, a: dict) -> str:
    cat = a["category"]
    cat_label = site.cat_label(cat)
    items = []
    for b in related_for(site, a):
        items.append(
            "      <li><a href=\"./{slug}.html\">"
            '<span class="eadr-rel-cat">{emoji} {cat} · {mins} min</span>'
            "<strong>{title}</strong>"
            '<span class="eadr-rel-hook">{hook}</span>'
            "</a></li>".format(
                slug=esc(b["slug"]),
                emoji=site.cat_emoji(b["category"]),
                cat=esc(site.cat_label(b["category"])),
                mins=b.get("reading_time_minutes") or "—",
                title=esc(b["title"]),
                hook=esc(truncate(b["hook"], 110)),
            )
        )
    pinned = next((p for p in site.published if p.get("pinned")), None)
    pinned_link = (
        f'      <a href="./{esc(pinned["slug"])}.html">📌 Master catalog of free AI tools</a>\n' if pinned and pinned["slug"] != a["slug"] else ""
    )
    return (
        "<!-- eadr:footer:start -->\n"
        f"<style>{RELATED_CSS}</style>\n"
        '<section class="eadr-related" aria-labelledby="eadr-related-title">\n'
        '  <div class="eadr-related-inner">\n'
        '    <p class="eadr-kicker">Keep going</p>\n'
        '    <h2 id="eadr-related-title">Related guides</h2>\n'
        '    <ul class="eadr-related-grid">\n' + "\n".join(items) + "\n"
        "    </ul>\n"
        '    <p class="eadr-next">\n'
        f'      <a href="../index.html?category={esc(cat)}">More {esc(cat_label)} guides →</a>\n'
        '      <a href="../index.html">All guides</a>\n'
        '      <a href="../privacy.html">Privacy</a>\n'
        f"{pinned_link}"
        f'      <a href="{GITHUB_REPO}/issues/new" rel="noopener">Report a problem</a>\n'
        "    </p>\n"
        f'    <p class="eadr-foot-meta">{esc(site.title)} · {esc(a["tool"])} · free-tier terms verified {fmt_date(a["verified"])} · '
        f'<a href="{esc(a["source_url"])}" rel="noopener">provider source</a></p>\n'
        "  </div>\n"
        "</section>\n"
        "<!-- eadr:footer:end -->\n"
    )


# --------------------------------------------------------------------------- #
# aria-labels for icon-only buttons
# --------------------------------------------------------------------------- #
def _button_text(inner: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner))).strip()


def label_for_button(attrs: str, text: str) -> str | None:
    """Return an aria-label for a button with no readable text, or None."""
    if re.search(r"[A-Za-z]{2,}", text):
        return None  # already has a readable visible label
    attrs_l = attrs.lower()
    text_l = text.lower()
    m = re.search(r'data-step=["\'](\d+)', attrs)
    if m:
        return f"Go to step {m.group(1)}"
    m = re.search(r'data-(?:usage|min|value|count)=["\']([^"\']+)', attrs)
    if m and re.fullmatch(r"\d+", text):
        return f"Use preset {text}"
    if re.fullmatch(r"\d+", text):
        return f"Use preset {text}"
    if "twitter" in attrs_l or re.search(r'data-platform=["\']x["\']', attrs_l) or re.fullmatch(r"[^a-z]*x[^a-z]*", text_l):
        return "Share on X"
    if "linkedin" in attrs_l:
        return "Share on LinkedIn"
    if "facebook" in attrs_l:
        return "Share on Facebook"
    if "copy" in attrs_l or "🔗" in text or "📋" in text:
        return "Copy link"
    if "theme" in attrs_l or text in ("◐", "☀️", "🌙", "🌓", "☾", "☀", "●", "○"):
        return "Toggle dark/light theme"
    if "close" in attrs_l or "xmark" in attrs_l or text in ("×", "✕", "✖"):
        return "Close"
    if "modal" in attrs_l or "info" in attrs_l or "metadata" in attrs_l:
        return "View full details"
    if "next" in attrs_l or "→" in text or "›" in text:
        return "Next"
    if "prev" in attrs_l or "←" in text or "‹" in text:
        return "Previous"
    return None


def add_button_labels(doc: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        attrs, inner = m.group(1), m.group(2)
        if "aria-label" in attrs or "aria-labelledby" in attrs:
            return m.group(0)
        label = label_for_button(attrs, _button_text(inner))
        if not label:
            return m.group(0)
        count += 1
        return f'<button{attrs} aria-label="{esc(label)}">{inner}</button>'

    return re.sub(r"<button\b([^>]*)>(.*?)</button>", repl, doc, flags=re.S | re.I), count


# --------------------------------------------------------------------------- #
# article processing
# --------------------------------------------------------------------------- #
def ensure_skip_target(doc: str) -> tuple[str, str]:
    """Pick (and if necessary create) the skip-link target. Returns (doc, id)."""
    m = re.search(r"<main\b([^>]*)>", doc, re.I)
    if m:
        attrs = m.group(1)
        idm = re.search(r'\bid=["\']([^"\']+)["\']', attrs)
        new_attrs = attrs
        if not idm:
            new_attrs += ' id="main"'
        if "tabindex" not in attrs:
            new_attrs += ' tabindex="-1"'
        if new_attrs != attrs:
            doc = doc[: m.start()] + f"<main{new_attrs}>" + doc[m.end():]
        return doc, (idm.group(1) if idm else "main")
    m = re.search(r"<h1\b([^>]*)>", doc, re.I)
    if m:
        attrs = m.group(1)
        idm = re.search(r'\bid=["\']([^"\']+)["\']', attrs)
        new_attrs = attrs
        if not idm:
            new_attrs += ' id="eadr-content"'
        if "tabindex" not in attrs:
            new_attrs += ' tabindex="-1"'
        if new_attrs != attrs:
            doc = doc[: m.start()] + f"<h1{new_attrs}>" + doc[m.end():]
        return doc, (idm.group(1) if idm else "eadr-content")
    return doc, "eadr-content"


def process_article(site: Site, a: dict, check: bool = False) -> tuple[bool, int]:
    path = ROOT / a["path"]
    raw = path.read_bytes()
    crlf = b"\r\n" in raw
    doc = raw.decode("utf-8").replace("\r\n", "\n")
    original = doc

    today = TODAY
    if check:  # re-render as of the committed build date so the check is deterministic
        m = re.search(r'<nav class="eadr-nav"[^>]*data-built="(\d{4}-\d{2}-\d{2})"', doc)
        if m:
            today = dt.date.fromisoformat(m.group(1))

    for name in ("head", "nav", "footer"):
        doc = strip_block(doc, name)

    # title fix for exported artifacts that never got a real title
    if re.search(r"<title>\s*(React Artifact)?\s*</title>", doc, re.I):
        doc = re.sub(r"<title>.*?</title>", f"<title>{esc(a['title'])} | {esc(site.title)}</title>", doc, count=1, flags=re.I | re.S)

    doc, labelled = add_button_labels(doc)
    doc, skip_target = ensure_skip_target(doc)

    # <head>: block goes on its own lines just before </head>
    hm = re.search(r"</head>", doc, re.I)
    if not hm:
        raise SystemExit(f"{a['path']}: no </head>")
    at = line_start(doc, hm.start())
    doc = doc[:at] + head_block(site, a, doc) + doc[at:]

    # top of <body>: block starts on the line after the <body> tag
    bm = re.search(r"<body\b[^>]*>", doc, re.I)
    if not bm:
        raise SystemExit(f"{a['path']}: no <body>")
    need_anchor = skip_target == "eadr-content" and 'id="eadr-content"' not in doc
    nav = nav_block(site, a, skip_target, today, add_anchor=need_anchor)
    at = bm.end() + (1 if doc[bm.end():bm.end() + 1] == "\n" else 0)
    doc = doc[:at] + nav + doc[at:]

    # related guides: before the page footer when there is one, else before </body>
    no_script = re.sub(r"<script\b[^>]*>.*?</script>", lambda m: " " * len(m.group(0)), doc, flags=re.S | re.I)
    fm = list(re.finditer(r"<footer\b", no_script, re.I))
    insert_at = fm[-1].start() if fm else None
    if insert_at is None:
        em = re.search(r"</body>", doc, re.I)
        if not em:
            raise SystemExit(f"{a['path']}: no </body>")
        insert_at = em.start()
    insert_at = line_start(doc, insert_at)
    doc = doc[:insert_at] + related_block(site, a) + doc[insert_at:]

    changed = doc != original
    if changed and not check:
        out = doc.replace("\n", "\r\n") if crlf else doc
        path.write_bytes(out.encode("utf-8"))
    return changed, labelled


# --------------------------------------------------------------------------- #
# sitemap + feed
# --------------------------------------------------------------------------- #
def build_sitemap(site: Site) -> str:
    newest = max(max(a["date"], a["verified"]) for a in site.published)
    rows = [f"  <url><loc>{xml_escape(site.base)}</loc><lastmod>{newest}</lastmod></url>"]
    for page, lastmod in STATIC_PAGES:
        rows.append(f"  <url><loc>{xml_escape(site.base + page)}</loc><lastmod>{lastmod}</lastmod></url>")
    for a in sorted(site.published, key=lambda x: x["date"], reverse=True):
        rows.append(f"  <url><loc>{xml_escape(site.url(a))}</loc><lastmod>{max(a['date'], a['verified'])}</lastmod></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"


def rfc822(iso: str) -> str:
    d = dt.datetime.combine(dt.date.fromisoformat(iso), dt.time(0, 0), tzinfo=dt.timezone.utc)
    return email.utils.format_datetime(d)


def build_feed(site: Site) -> str:
    items = sorted(site.published, key=lambda x: (x["date"], x["slug"]), reverse=True)[:FEED_ITEMS]
    newest = items[0]["date"]
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "<channel>",
        f"  <title>{xml_escape(site.title)}</title>",
        f"  <link>{xml_escape(site.base)}</link>",
        f"  <description>{xml_escape(site.description)}</description>",
        "  <language>en</language>",
        f"  <lastBuildDate>{rfc822(newest)}</lastBuildDate>",
        f'  <atom:link href="{xml_escape(site.base)}feed.xml" rel="self" type="application/rss+xml"/>',
        f"  <image><url>{xml_escape(site.base)}apple-touch-icon.png</url><title>{xml_escape(site.title)}</title><link>{xml_escape(site.base)}</link></image>",
    ]
    for a in items:
        url = site.url(a)
        out += [
            "  <item>",
            f"    <title>{xml_escape(a['title'])}</title>",
            f"    <link>{xml_escape(url)}</link>",
            f'    <guid isPermaLink="true">{xml_escape(url)}</guid>',
            f"    <pubDate>{rfc822(a['date'])}</pubDate>",
            f"    <category>{xml_escape(site.cat_label(a['category']))}</category>",
            f"    <description>{xml_escape(a['hook'])} (Tool: {xml_escape(a['tool'])} · verified {a['verified']})</description>",
            "  </item>",
        ]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# README catalog (backlog 6.5) - the per-category list between the markers is
# generated, so the GitHub front page can't drift from metadata.json again.
# --------------------------------------------------------------------------- #
README = ROOT / "README.md"
CATALOG_START = "<!-- catalog:start -->"
CATALOG_END = "<!-- catalog:end -->"


def build_catalog(site: Site) -> str:
    by_cat: dict[str, list[dict]] = {}
    for a in site.published:
        by_cat.setdefault(a["category"], []).append(a)
    lines = [
        f"**{len(site.published)} verified guides** across {len(by_cat)} categories. "
        "This list is generated from `metadata.json` by `python3 scripts/build.py`, so edit the metadata, not this section.",
        "",
    ]
    for cat in sorted(by_cat, key=site.cat_label):
        items = sorted(by_cat[cat], key=lambda a: (not a.get("pinned"), a["title"].lower()))
        lines.append(f"### {site.cat_emoji(cat)} {site.cat_label(cat)} ({len(items)})")
        lines.append("")
        for a in items:
            pin = "📌 " if a.get("pinned") else ""
            lines.append(f"* {pin}**[{a['title']}]({site.url(a)})** — {truncate(a['hook'], 170)}")
            lines.append(f"  <sub>{a['tool']} · verified {fmt_date(a['verified'])}</sub>")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_readme(site: Site, current: str) -> str:
    try:
        head, rest = current.split(CATALOG_START, 1)
        _, tail = rest.split(CATALOG_END, 1)
    except ValueError:
        raise SystemExit(f"README.md is missing the {CATALOG_START} / {CATALOG_END} markers")
    return head + CATALOG_START + "\n" + build_catalog(site) + CATALOG_END + tail


# Static pages that live outside metadata.json but should be in the sitemap.
STATIC_PAGES = [("privacy.html", "2026-10-08")]


def write_if_changed(path: Path, content: str, check: bool) -> bool:
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == content:
        return False
    if not check:
        path.write_text(content, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- #
def main(argv: list[str]) -> int:
    check = "--check" in argv
    site = Site(json.loads(METADATA.read_text(encoding="utf-8")))

    changed_articles = 0
    labelled = 0
    for a in site.articles:
        ch, n = process_article(site, a, check=check)
        changed_articles += ch
        labelled += n

    changed_files = []
    if write_if_changed(ROOT / "sitemap.xml", build_sitemap(site), check):
        changed_files.append("sitemap.xml")
    if write_if_changed(ROOT / "feed.xml", build_feed(site), check):
        changed_files.append("feed.xml")
    if write_if_changed(README, build_readme(site, README.read_text(encoding="utf-8")), check):
        changed_files.append("README.md")

    verb = "would change" if check else "updated"
    print(f"{verb}: {changed_articles} article(s), {', '.join(changed_files) or 'no root files'}; "
          f"{labelled} icon-only button(s) newly given aria-labels; "
          f"{sum(is_stale(a['verified'], TODAY) for a in site.published)} published guide(s) flagged stale (> {STALE_AFTER_DAYS} days as of {TODAY})")
    if check and (changed_articles or changed_files):
        print("run `python3 scripts/build.py` and commit the result")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
