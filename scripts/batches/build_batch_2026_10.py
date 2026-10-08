#!/usr/bin/env python3
"""Render the 2026-10 guide batch (36 guides) into articles/, artifacts/prompt-packs/ and metadata.json.

Run once per batch from the repository root:
    python3 scripts/batches/build_batch_2026_10.py
Then: python3 scripts/validate_metadata.py && python3 scripts/build.py && python3 scripts/make_social_cards.py

Every guide's verification note is tied to what was actually checked on the verified date:
  * GitHub-hosted tools: licence read from the repository via the GitHub API.
  * Cloudflare, OpenRouter, Mistral: free-tier wording read from the provider's own page.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from guides_2026_10_a import GUIDES as A  # noqa: E402
from guides_2026_10_b import GUIDES as B  # noqa: E402
from guides_2026_10_c import GUIDES as C  # noqa: E402
from guides_2026_10_d import GUIDES as D  # noqa: E402

VERIFIED = "2026-10-08"
METADATA = ROOT / "metadata.json"
ARTICLES = ROOT / "articles"
PACKS = ROOT / "artifacts" / "prompt-packs"

CSS = """
  :root{--paper:#FAFAF9;--paper-raised:#FFFFFF;--ink:#1C1C1E;--ink-soft:#54545A;--muted:#6E6E73;--line:rgba(28,28,30,.10);--green:#0D7D56;--green-soft:rgba(15,138,95,.10);--coral:#C2410C;--display:'Manrope',sans-serif;--body:'Inter',sans-serif;--mono:'JetBrains Mono',monospace}
  @media (prefers-color-scheme:dark){:root{--paper:#141414;--paper-raised:#1C1C1E;--ink:#F4F4F3;--ink-soft:#C7C7CB;--muted:#9A9AA0;--line:rgba(244,244,243,.10);--green:#22C58B;--green-soft:rgba(34,197,139,.14);--coral:#FF8064}}
  html[data-theme="light"]{--paper:#FAFAF9;--paper-raised:#FFFFFF;--ink:#1C1C1E;--ink-soft:#54545A;--muted:#6E6E73;--line:rgba(28,28,30,.10);--green:#0D7D56;--green-soft:rgba(15,138,95,.10)}
  html[data-theme="dark"]{--paper:#141414;--paper-raised:#1C1C1E;--ink:#F4F4F3;--ink-soft:#C7C7CB;--muted:#9A9AA0;--line:rgba(244,244,243,.10);--green:#22C58B;--green-soft:rgba(34,197,139,.14)}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.65}
  a{color:var(--green)}
  a:focus-visible,button:focus-visible{outline:3px solid var(--green);outline-offset:2px;border-radius:4px}
  .wrap{max-width:780px;margin:0 auto;padding:0 22px}
  .topbar{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:1px solid var(--line);margin-bottom:28px}
  .topbar a.mark{font-family:var(--display);font-weight:800;color:var(--ink);text-decoration:none;font-size:15px}
  .theme-toggle{font:600 12px var(--body);color:var(--ink-soft);background:var(--paper-raised);border:1px solid var(--line);border-radius:18px;padding:6px 12px;cursor:pointer}
  .kicker{display:inline-block;font:600 12px var(--mono);color:var(--green);background:var(--green-soft);padding:5px 12px;border-radius:14px;margin-bottom:14px}
  h1{font-family:var(--display);font-weight:800;font-size:clamp(28px,4.2vw,40px);line-height:1.18;letter-spacing:-.02em;margin:0 0 14px}
  .hook{font-size:18px;color:var(--ink-soft);margin:0 0 26px}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:0 0 30px}
  .stat{background:var(--paper-raised);border:1px solid var(--line);border-left:4px solid var(--green);border-radius:12px;padding:14px 16px}
  .stat b{display:block;font:600 11px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px}
  .stat span{font-size:14.5px;color:var(--ink)}
  h2{font-family:var(--display);font-weight:700;font-size:21px;margin:38px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
  p,li{color:var(--ink-soft)}
  ol.steps{list-style:none;counter-reset:s;padding:0;margin:0}
  ol.steps>li{counter-increment:s;position:relative;padding-left:44px;margin-bottom:18px}
  ol.steps>li::before{content:counter(s);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;background:var(--green);color:#fff;font:700 13px/28px var(--body);text-align:center}
  ol.steps strong{color:var(--ink);display:block}
  code{font-family:var(--mono);font-size:.88em;background:var(--paper-raised);border:1px solid var(--line);padding:1px 6px;border-radius:6px;color:var(--ink)}
  pre.prompt{white-space:pre-wrap;word-wrap:break-word;font:13.5px/1.6 var(--mono);color:var(--ink);background:var(--paper-raised);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0}
  .copy{margin-top:10px;font:600 13px var(--body);color:#fff;background:var(--green);border:0;border-radius:8px;padding:8px 14px;cursor:pointer}
  .verify{background:var(--green-soft);border-left:4px solid var(--green);border-radius:12px;padding:14px 18px;margin:26px 0}
  .verify p{margin:0;color:var(--ink)}
  ul.checks,ul.pitfalls{padding-left:20px}
  ul.pitfalls li{color:var(--ink-soft)}
  footer{border-top:1px solid var(--line);padding:30px 22px;text-align:center;color:var(--muted);font-size:13.5px}
"""

THEME_JS = """
function toggleTheme(){var r=document.documentElement;var c=r.getAttribute('data-theme');if(c==='light'){r.removeAttribute('data-theme');}else{r.setAttribute('data-theme','light');}}
function copyPrompt(btn){var t=document.getElementById(btn.getAttribute('data-target')).textContent;if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){btn.textContent='Copied';});}}
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def words(g: dict) -> int:
    parts = [g["intro"], g["prompt"]] + [t + " " + b for t, b in g["steps"]] + g["checks"] + g["pitfalls"]
    return len(re.sub(r"<[^>]+>", " ", " ".join(parts)).split())


def verification_note(g: dict) -> str:
    src = g["source"]
    if "github.com" in src:
        return ("Licence and project status were read from the project's GitHub repository on "
                "8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version.")
    if "developers.cloudflare.com" in src:
        return ("The free allocation was read from Cloudflare's Workers AI pricing page (last updated 1 Oct 2026) on 8 Oct 2026. Cloudflare can change it; check the page before you build on it.")
    if "openrouter.ai" in src:
        return ("The ':free' variant behaviour was read from OpenRouter's documentation on 8 Oct 2026. Free models change often; check the model's page for current limits.")
    if "mistral.ai" in src:
        return ("The Free plan's features were read from Mistral's pricing page on 8 Oct 2026. Allowances are set by Mistral and shown in your account.")
    return "Checked on 8 Oct 2026."


def render_article(g: dict, reading: int) -> str:
    title = esc(g["title"])
    cat_label_map = {"civic": "Civic & Legal", "ai-tools": "AI Tools"}
    steps_html = "\n".join(
        f"          <li><strong>{esc(t)}</strong>{b}</li>" for t, b in g["steps"]
    )
    checks_html = "\n".join(f"          <li>{esc(c)}</li>" for c in g["checks"])
    pit_html = "\n".join(f"          <li>{esc(p)}</li>" for p in g["pitfalls"])
    slug = g["slug"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Everyday AI, Done Right</title>
  <meta name="description" content="{esc(g['hook'])}">
  <meta name="keywords" content="{esc(', '.join(g['tags']))}">
  <meta name="author" content="Everyday AI, Done Right">
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <a class="mark" href="../index.html">Everyday AI, Done Right</a>
      <button class="theme-toggle" type="button" onclick="toggleTheme()">Toggle theme</button>
    </header>

    <main id="main" tabindex="-1">
      <article>
        <span class="kicker">{esc(cat_label_map.get(g['category'], g['category'].replace('-', ' ').title()))}</span>
        <h1>{title}</h1>
        <p class="hook">{esc(g['hook'])}</p>

        <div class="stats">
          <div class="stat"><b>Tool</b><span>{esc(g['tool'])}</span></div>
          <div class="stat"><b>Cost</b><span>{esc(g['free'])}</span></div>
          <div class="stat"><b>Limits</b><span>{esc(g['limits'])}</span></div>
          <div class="stat"><b>Verified</b><span>8 October 2026</span></div>
        </div>

        <section>
          <h2>Why this works</h2>
          <p>{esc(g['intro'])}</p>
        </section>

        <section>
          <h2>Step by step</h2>
          <ol class="steps">
{steps_html}
          </ol>
        </section>

        <section>
          <h2>Copy-paste prompt</h2>
          <pre class="prompt" id="prompt-{slug}">{esc(g['prompt'])}</pre>
          <button class="copy" type="button" data-target="prompt-{slug}" onclick="copyPrompt(this)">Copy prompt</button>
        </section>

        <section>
          <h2>Check your result</h2>
          <ul class="checks">
{checks_html}
          </ul>
        </section>

        <section>
          <h2>Pitfalls to avoid</h2>
          <ul class="pitfalls">
{pit_html}
          </ul>
        </section>

        <div class="verify">
          <p><strong>What we checked:</strong> {esc(verification_note(g))} Source: <a href="{esc(g['source'])}" rel="noopener">{esc(g['source'])}</a>.</p>
        </div>
      </article>
    </main>
  </div>

  <footer>
    <p>Everyday AI, Done Right · about {reading} min read · guides are not legal, medical, or financial advice.</p>
  </footer>
  <script>{THEME_JS}</script>
</body>
</html>
"""


def render_pack(g: dict) -> str:
    lines = [
        f"# {g['title']}",
        "",
        f"- **Tool:** {g['tool']}",
        f"- **Cost:** {g['free']}",
        f"- **Limits:** {g['limits']}",
        f"- **Source:** {g['source']}",
        f"- **Verified:** {VERIFIED}",
        f"- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/{g['slug']}.html",
        "",
        "## Steps",
        "",
    ]
    for i, (t, b) in enumerate(g["steps"], 1):
        plain = re.sub(r"<[^>]+>", "", b)
        lines.append(f"{i}. **{t}.** {plain}")
    lines += ["", "## Prompt", "", "```text", g["prompt"], "```", "", "## Check your result", ""]
    lines += [f"- [ ] {c}" for c in g["checks"]]
    lines += ["", "## Pitfalls", ""]
    lines += [f"- {p}" for p in g["pitfalls"]]
    lines += ["", f"_{verification_note(g)}_", ""]
    return "\n".join(lines)


def main() -> int:
    guides = A + B + C + D
    assert len(guides) == 36, f"expected 36 guides, got {len(guides)}"
    slugs = [g["slug"] for g in guides]
    assert len(set(slugs)) == len(slugs), "duplicate slug in batch"

    data = json.loads(METADATA.read_text(encoding="utf-8"))
    existing_slugs = {a["slug"] for a in data["articles"]}
    clashes = [s for s in slugs if s in existing_slugs or (ARTICLES / f"{s}.html").exists()]
    assert not clashes, f"slug already exists: {clashes}"

    next_id = max(int(a["id"]) for a in data["articles"]) + 1
    PACKS.mkdir(parents=True, exist_ok=True)
    for g in guides:
        reading = max(3, round(words(g) / 230))
        (ARTICLES / f"{g['slug']}.html").write_text(render_article(g, reading), encoding="utf-8")
        (PACKS / f"{g['slug']}.md").write_text(render_pack(g), encoding="utf-8")
        data["articles"].append({
            "id": f"{next_id:04d}",
            "slug": g["slug"],
            "title": g["title"],
            "hook": g["hook"],
            "path": f"articles/{g['slug']}.html",
            "date": VERIFIED,
            "status": "published",
            "format": "guide",
            "category": g["category"],
            "tool": g["tool"],
            "tool_family": g["family"],
            "source_url": g["source"],
            "tags": g["tags"],
            "reading_time_minutes": reading,
            "pinned": False,
            "verified": VERIFIED,
        })
        next_id += 1

    METADATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"rendered {len(guides)} guides; ids {int(data['articles'][-len(guides)]['id'])}–{next_id - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
