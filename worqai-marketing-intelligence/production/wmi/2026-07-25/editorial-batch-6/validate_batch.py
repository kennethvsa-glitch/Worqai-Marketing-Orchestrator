"""Validate the six-carousel editorial batch and write machine/human QA reports."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
EXPECTED = [
    "01-career-change",
    "02-editing",
    "03-career-gap",
    "04-junior-evidence",
    "05-senior-criterion",
    "06-vacancy-strategy",
]

FORBIDDEN = {
    # Percentage-only radii are permitted for hand-drawn circles/ovals; fixed
    # radii are the repeated rounded-card treatment this lint is meant to catch.
    "rounded_cards": r"border-radius\s*:\s*\d+(?:\.\d+)?(?:px|rem|em)\b",
    "backdrop_filter": r"backdrop-filter\s*:",
    "thin_borders": r"border(?:-[a-z]+)?\s*:\s*[12]px\b",
    "radial_gradient": r"radial-gradient\s*\(",
    "linear_gradient": r"linear-gradient\s*\(",
    "fake_ui": r"\b(?:dashboard|progress-bar|browser-window|status-chip|metric-card)\b",
}


def visible_text(html: str) -> str:
    text = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def inspect_carousel(name: str) -> dict:
    folder = ROOT / name
    html_files = sorted(folder.glob("*.html"))
    caption = folder / "caption.md"
    final_dir = folder / "final"
    pngs = sorted(final_dir.glob("slide_*.png"))
    issues: list[str] = []

    if len(html_files) != 1:
        issues.append(f"Expected exactly one HTML file, found {len(html_files)}")
        html = ""
        html_path = None
    else:
        html_path = html_files[0]
        html = html_path.read_text(encoding="utf-8")

    caption_text = caption.read_text(encoding="utf-8") if caption.exists() else ""
    if not caption.exists():
        issues.append("Missing caption.md")

    slide_count = len(
        re.findall(
            r'<section[^>]+class="[^"]*\bslide\b[^"]*"',
            html,
            flags=re.I,
        )
    )
    if slide_count != 7:
        issues.append(f"Expected 7 HTML slides, found {slide_count}")

    if len(pngs) != 7:
        issues.append(f"Expected 7 rendered PNGs, found {len(pngs)}")

    dimensions: dict[str, list[int]] = {}
    for png in pngs:
        with Image.open(png) as image:
            dimensions[png.name] = [image.width, image.height]
            if image.size != (1080, 1350):
                issues.append(f"{png.name} is {image.width}x{image.height}")

    html_text = visible_text(html)
    combined = f"{html_text}\n{caption_text}"

    if re.search(r"\busted\b", combined, flags=re.I):
        issues.append("Found 'usted'; batch must use tú voice")

    for target, label in [
        ("CV", "CV keyword"),
        ("1 mes", "one-month offer"),
        ("WorqAI Pro", "product name"),
        ("DM", "DM delivery"),
    ]:
        if target.casefold() not in html_text.casefold():
            issues.append(f"HTML missing {label}")
        if target.casefold() not in caption_text.casefold():
            issues.append(f"Caption missing {label}")

    font_sizes = [
        int(match.group(1))
        for match in re.finditer(r"font-size\s*:\s*(\d+)px", html, flags=re.I)
    ]
    min_font = min(font_sizes) if font_sizes else None
    if min_font is None:
        issues.append("No explicit pixel font sizes found")
    elif min_font < 20:
        issues.append(f"Minimum font size is {min_font}px; floor is 20px")

    forbidden_hits: dict[str, int] = {}
    for key, pattern in FORBIDDEN.items():
        count = len(re.findall(pattern, html, flags=re.I))
        forbidden_hits[key] = count
        if count:
            issues.append(f"Forbidden pattern '{key}' found {count} time(s)")

    unsupported_percentages = sorted(set(re.findall(r"\b\d+(?:[.,]\d+)?%", combined)))
    if unsupported_percentages:
        issues.append(
            "Percentage claim(s) require manual verification: "
            + ", ".join(unsupported_percentages)
        )

    contact_sheet = final_dir / "contact-sheet.png"
    if not contact_sheet.exists():
        issues.append("Missing final/contact-sheet.png")

    return {
        "carousel": name,
        "html": str(html_path.relative_to(ROOT)) if html_path else None,
        "caption": str(caption.relative_to(ROOT)) if caption.exists() else None,
        "slides_html": slide_count,
        "slides_png": len(pngs),
        "dimensions": dimensions,
        "minimum_font_px": min_font,
        "forbidden_hits": forbidden_hits,
        "percentage_claims": unsupported_percentages,
        "contact_sheet": contact_sheet.exists(),
        "issues": issues,
        "pass": not issues,
    }


def main() -> None:
    results = [inspect_carousel(name) for name in EXPECTED]
    passed = all(result["pass"] for result in results)
    report = {
        "root": str(ROOT),
        "expected_carousels": len(EXPECTED),
        "expected_slides": 42,
        "pass": passed,
        "results": results,
    }
    (ROOT / "batch-qa.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Editorial batch QA",
        "",
        f"Overall: **{'PASS' if passed else 'FAIL'}**",
        "",
        "| Carousel | HTML | PNG | Min font | Result |",
        "|---|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['carousel']} | {result['slides_html']} | "
            f"{result['slides_png']} | {result['minimum_font_px'] or '—'}px | "
            f"{'PASS' if result['pass'] else 'FAIL'} |"
        )
    lines.extend(["", "## Issues", ""])
    issue_count = 0
    for result in results:
        if result["issues"]:
            issue_count += len(result["issues"])
            lines.append(f"### {result['carousel']}")
            lines.append("")
            lines.extend(f"- {issue}" for issue in result["issues"])
            lines.append("")
    if not issue_count:
        lines.append("No automated QA issues detected.")

    (ROOT / "batch-qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Validated {len(results)} carousels / {sum(r['slides_png'] for r in results)} PNG slides")
    print(f"Result: {'PASS' if passed else 'FAIL'}")
    print(f"Report: {ROOT / 'batch-qa.md'}")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
