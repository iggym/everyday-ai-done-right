#!/usr/bin/env python3
"""Validate (and optionally fix / canonically format) metadata.json.

Usage:
    python3 scripts/validate_metadata.py            # validate only, exit 1 on problems
    python3 scripts/validate_metadata.py --fix      # normalise categories + ids, then rewrite
    python3 scripts/validate_metadata.py --format   # rewrite in canonical formatting only

Checks performed
----------------
* every article has the required keys with sane types
* ``id`` is a unique, zero-padded 4-digit string
* ``slug`` is unique and matches ``path`` (articles/<slug>.html)
* the HTML file referenced by ``path`` exists on disk
* ``category`` is lowercase and one of the known categories
* ``status`` is ``published`` or ``draft``
* ``date`` / ``verified`` are ISO ``YYYY-MM-DD``
* every HTML file in ``articles/`` is referenced by metadata (no orphans)

``--fix`` lower-cases categories, coerces ids to zero-padded strings and
re-assigns duplicate ids (first occurrence keeps its id, later duplicates get
the lowest unused id).  Nothing else is changed automatically.

No third-party dependencies - standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "metadata.json"
ARTICLES_DIR = ROOT / "articles"

REQUIRED_KEYS = {
    "id": str,
    "slug": str,
    "title": str,
    "hook": str,
    "path": str,
    "date": str,
    "status": str,
    "format": str,
    "category": str,
    "tool": str,
    "tool_family": str,
    "source_url": str,
    "tags": list,
    "reading_time_minutes": int,
    "pinned": bool,
    "verified": str,
}
OPTIONAL_KEYS = {"pinned_reason": str}

KNOWN_CATEGORIES = {
    "accessibility",
    "business",
    "career",
    "civic",
    "creative",
    "family",
    "health",
    "household",
    "learning",
    "travel",
}
VALID_STATUS = {"published", "draft"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- #
# Canonical formatting
# --------------------------------------------------------------------------- #
def _dump(value, indent: int = 0) -> str:
    """json.dumps(indent=2) but with arrays of scalars kept on one line."""
    pad = "  " * indent
    inner = "  " * (indent + 1)
    if isinstance(value, dict):
        if not value:
            return "{}"
        items = [f'{inner}{json.dumps(k, ensure_ascii=False)}: {_dump(v, indent + 1)}' for k, v in value.items()]
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(v, (dict, list)) for v in value):
            return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in value) + "]"
        items = [f"{inner}{_dump(v, indent + 1)}" for v in value]
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    return json.dumps(value, ensure_ascii=False)


def canonical_json(data: dict) -> str:
    return _dump(data) + "\n"


# --------------------------------------------------------------------------- #
# Fixers
# --------------------------------------------------------------------------- #
def fix(data: dict) -> list[str]:
    """Apply safe, mechanical fixes in place. Returns a list of change notes."""
    notes: list[str] = []
    articles = data["articles"]

    # 1. category casing
    for a in articles:
        cat = a.get("category")
        if isinstance(cat, str) and cat != cat.lower():
            notes.append(f"{a['slug']}: category {cat!r} -> {cat.lower()!r}")
            a["category"] = cat.lower()

    # 2. ids -> zero-padded strings
    for a in articles:
        raw = a.get("id")
        if isinstance(raw, int) or (isinstance(raw, str) and raw.isdigit() and len(raw) != 4):
            new = f"{int(raw):04d}"
            notes.append(f"{a['slug']}: id {raw!r} -> {new!r}")
            a["id"] = new

    # 3. duplicate ids: first occurrence wins, others get the lowest unused id
    used = Counter(a["id"] for a in articles)
    seen: set[str] = set()
    taken = set(used)

    def next_free() -> str:
        n = 1
        while f"{n:04d}" in taken:
            n += 1
        new = f"{n:04d}"
        taken.add(new)
        return new

    for a in articles:
        if a["id"] in seen:
            new = next_free()
            notes.append(f"{a['slug']}: duplicate id {a['id']!r} -> {new!r}")
            a["id"] = new
        seen.add(a["id"])

    return notes


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def validate(data: dict) -> list[str]:
    problems: list[str] = []
    articles = data.get("articles")
    if not isinstance(articles, list):
        return ["'articles' must be a list"]

    # site.categories is the single source of truth for labels/emojis
    # (index.html and scripts/build.py read it too)
    site_cats = (data.get("site") or {}).get("categories") or {}
    known = set(site_cats) or KNOWN_CATEGORIES
    for key, meta in site_cats.items():
        if key != key.lower():
            problems.append(f"site.categories: key {key!r} must be lowercase")
        if not isinstance(meta, dict) or not meta.get("label") or not meta.get("emoji"):
            problems.append(f"site.categories[{key!r}] needs 'label' and 'emoji'")
    emojis = Counter(m.get("emoji") for m in site_cats.values() if isinstance(m, dict))
    for e, n in emojis.items():
        if n > 1:
            problems.append(f"site.categories: emoji {e!r} is used by {n} categories (must be distinct)")

    ids: dict[str, list[str]] = defaultdict(list)
    slugs: dict[str, int] = Counter()
    paths: set[str] = set()

    for i, a in enumerate(articles):
        label = a.get("slug") or f"#{i}"
        for key, typ in REQUIRED_KEYS.items():
            if key not in a:
                problems.append(f"{label}: missing key {key!r}")
            elif not isinstance(a[key], typ) or (typ is int and isinstance(a[key], bool)):
                problems.append(f"{label}: {key!r} should be {typ.__name__}, got {type(a[key]).__name__}")
        for key in a:
            if key not in REQUIRED_KEYS and key not in OPTIONAL_KEYS:
                problems.append(f"{label}: unknown key {key!r}")
        if not all(k in a for k in ("id", "slug", "path")):
            continue

        ids[str(a["id"])].append(label)
        slugs[a["slug"]] += 1
        paths.add(a["path"])

        if not re.fullmatch(r"\d{4}", str(a["id"])):
            problems.append(f"{label}: id {a['id']!r} is not a zero-padded 4-digit string")
        if a["path"] != f"articles/{a['slug']}.html":
            problems.append(f"{label}: path {a['path']!r} does not match slug")
        if not (ROOT / a["path"]).is_file():
            problems.append(f"{label}: file {a['path']!r} does not exist")
        cat = a.get("category")
        if cat != (cat or "").lower():
            problems.append(f"{label}: category {cat!r} is not lowercase")
        elif cat not in known:
            problems.append(f"{label}: unknown category {cat!r} (add it to site.categories in metadata.json)")
        if a.get("status") not in VALID_STATUS:
            problems.append(f"{label}: status {a.get('status')!r} not in {sorted(VALID_STATUS)}")
        for dk in ("date", "verified"):
            if isinstance(a.get(dk), str) and not ISO_DATE.match(a[dk]):
                problems.append(f"{label}: {dk} {a[dk]!r} is not YYYY-MM-DD")
        if isinstance(a.get("tags"), list) and not all(isinstance(t, str) for t in a["tags"]):
            problems.append(f"{label}: tags must all be strings")

    for id_, labels in ids.items():
        if len(labels) > 1:
            problems.append(f"duplicate id {id_!r}: {labels}")
    for slug, n in slugs.items():
        if n > 1:
            problems.append(f"duplicate slug {slug!r} ({n} times)")

    redirects = (data.get("site") or {}).get("redirects") or {}
    live = set(slugs)
    for old, new in redirects.items():
        if new not in live:
            problems.append(f"site.redirects: {old!r} -> {new!r} but no such slug exists")
        if old in live:
            problems.append(f"site.redirects: {old!r} is still a live slug (remove the redirect or the article)")

    on_disk = {f"articles/{p.name}" for p in ARTICLES_DIR.glob("*.html")}
    for orphan in sorted(on_disk - paths):
        problems.append(f"orphan file not in metadata: {orphan}")

    return problems


def main(argv: list[str]) -> int:
    do_fix = "--fix" in argv
    do_format = "--format" in argv or do_fix

    raw = METADATA.read_text(encoding="utf-8")
    data = json.loads(raw)

    if do_fix:
        for note in fix(data):
            print(f"fix: {note}")

    problems = validate(data)
    for p in problems:
        print(f"error: {p}")

    if do_format:
        out = canonical_json(data)
        if out != raw:
            METADATA.write_text(out, encoding="utf-8")
            print(f"wrote {METADATA.relative_to(ROOT)} (canonical format)")

    n = len(data["articles"])
    pub = sum(1 for a in data["articles"] if a.get("status") == "published")
    print(f"{n} articles ({pub} published, {n - pub} draft) - {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
