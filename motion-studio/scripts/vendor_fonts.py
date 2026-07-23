"""
vendor_fonts.py — one-time vendoring of Google Fonts into vendor/fonts/.

Downloads the exact woff2 binaries Google serves (latin + latin-ext subsets),
writes vendor/fonts/fonts.css with the same family names the templates already
use (no CSS changes needed), and rewrites template <link> tags to the local css.

Why: CDN fonts are the last non-deterministic dependency — offline renders fall
back silently, and Google can update font binaries without notice, invalidating
every golden hash. See Ideation/motion-expansion-plan.md Phase 0.

Usage:
    py scripts/vendor_fonts.py           # download + write css + rewrite templates
    py scripts/vendor_fonts.py --check   # report CDN references without changing anything
"""

import argparse
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
FONT_DIR = ROOT / "vendor" / "fonts"
FONTS_CSS = FONT_DIR / "fonts.css"

# Superset of every family/weight/style any template requests (audited 2026-06-12).
# Newsreader requested with its optical-size axis (variable) to match both usages.
CSS2_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Archivo+Black"
    "&family=Archivo:wght@400;500;600"
    "&family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400"
    "&family=JetBrains+Mono:wght@400;500"
    "&family=Newsreader:ital,opsz,wght@0,6..72,600;1,6..72,400"
    "&display=swap"
)

# Modern Chrome UA → Google serves woff2 (+ variable fonts where available)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

SUBSETS = ("latin", "latin-ext")  # Spanish diacritics live in latin; ext for safety

LINK_RE = re.compile(
    r'\s*<link[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>\s*\n?')


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def download_fonts() -> str:
    """Fetch Google's css2, download each latin/latin-ext woff2, return local css."""
    css = fetch(CSS2_URL).decode("utf-8")
    # css2 format: /* subset */\n@font-face { ... src: url(...) ... }
    blocks = re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face\s*\{[^}]+\})", css)
    out_css, seen = [], set()
    for subset, block in blocks:
        if subset not in SUBSETS:
            continue
        m = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", block)
        if not m:
            continue
        url = m.group(1)
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        weight = re.search(r"font-weight:\s*([\d ]+)", block).group(1).strip()
        fname = f"{fam.replace(' ', '')}-{weight.replace(' ', 'to')}-{style}-{subset}.woff2"
        if fname not in seen:
            seen.add(fname)
            (FONT_DIR / fname).write_bytes(fetch(url))
            print(f"  downloaded {fname}")
        out_css.append(f"/* {subset} */\n" + block.replace(url, fname))
    return "\n".join(out_css) + "\n"


def rewrite_templates() -> int:
    """Replace googleapis <link> tags with a single local fonts.css link."""
    changed = 0
    for html in list((ROOT / "templates").glob("*.html")) + \
                list((ROOT / "templates" / "scenes").glob("scene-*.html")) + \
                [ROOT / "templates" / "motion-shell.html"]:
        if not html.exists():
            continue
        text = html.read_text(encoding="utf-8")
        if "fonts.googleapis.com" not in text:
            continue
        rel = "../../vendor/fonts/fonts.css" if html.parent.name == "scenes" \
              else "../vendor/fonts/fonts.css"
        local_link = f'  <link href="{rel}" rel="stylesheet">\n'
        new, n = LINK_RE.subn("", text)
        # insert the local link where the first removed link used to be (after <meta charset>)
        new = re.sub(r'(<meta charset[^>]*>\s*\n)', r"\1" + local_link, new, count=1)
        if n:
            html.write_text(new, encoding="utf-8")
            print(f"  rewrote {html.relative_to(ROOT)} ({n} CDN tags removed)")
            changed += 1
    return changed


def check_only():
    hits = []
    for html in (ROOT / "templates").rglob("*.html"):
        if "fonts.googleapis.com" in html.read_text(encoding="utf-8"):
            hits.append(str(html.relative_to(ROOT)))
    print("CDN font references:" if hits else "No CDN font references — fully vendored.")
    for h in hits:
        print(f"  {h}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        check_only()
        return
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading font binaries…")
    css = download_fonts()
    FONTS_CSS.write_text(css, encoding="utf-8")
    print(f"Wrote {FONTS_CSS.relative_to(ROOT)}")
    print("Rewriting templates…")
    n = rewrite_templates()
    print(f"\nDone — {n} templates now load fonts locally.")
    print("Next: re-run golden_frames --check on villain-v3 to confirm pixels unchanged.")


if __name__ == "__main__":
    main()
