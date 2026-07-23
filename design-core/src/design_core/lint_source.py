"""Deterministic anti-slop linter for WorqAI source across every lane.

Dispatches by file type:
  .tsx/.ts/.jsx/.js  -> Remotion / React composition rules (reels, motion)
  .html/.css/.svg    -> carousel and single-picture markup rules

Rules and thresholds come from design-core brand/*.json via contract.py, so
one edit to the brand data reconfigures every lane. ASCII-only output for
Windows cp1252 consoles.

Usage:
    python -m design_core.lint_source <paths...> [--strict] [--json out.json]

--strict exits 1 on any BLOCK finding (wire this into a lane's build gate).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .contract import (
    ALLOWED_HEX,
    BANNED,
    BANNED_DESIGNED_COPY,
    EMOJI_ICONS,
    INTER_DISPLAY_MIN_PX,
    GateFailure,
    report,
)

HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
WEB_EXT = {".html", ".htm", ".css", ".svg"}
CODE_EXT = {".tsx", ".ts", ".jsx", ".js"}

# CSS font-size like 48px / 3rem / 2.5em considered "display" when large.
CSS_FONT_SIZE = re.compile(r"font-size\s*:\s*([\d.]+)(px|rem|em)")
CSS_FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;{}]+)")


def _px(value: float, unit: str) -> float:
    return value * 16 if unit in ("rem", "em") else value


def _severity(default: str) -> str:
    return default


def lint_web(text: str, path: Path) -> list[GateFailure]:
    out: list[GateFailure] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        loc = f"{path.name}:{i}"
        for rule in BANNED["banned_css_patterns"]:
            if re.search(rule["regex"], line, re.I):
                out.append(GateFailure(rule["id"], "BLOCK", rule["why"], loc))
        for m in HEX_RE.finditer(line):
            val = m.group(1).lower()
            exp = "".join(c * 2 for c in val) if len(val) == 3 else val
            if exp not in ALLOWED_HEX:
                out.append(GateFailure("HEX-OFF-TOKEN", "BLOCK",
                    f"off-token color #{val} (brand tokens only)", loc))
        # Inter (or any banned display font) at display size on the same rule.
        fam = CSS_FONT_FAMILY.search(line)
        if fam:
            names = fam.group(1).lower()
            size = CSS_FONT_SIZE.search(line)
            big = size and _px(float(size.group(1)), size.group(2)) >= INTER_DISPLAY_MIN_PX
            for banned in BANNED["banned_display_fonts"]:
                if banned.lower() in names and (big or "display" in names):
                    out.append(GateFailure("BANNED-DISPLAY-FONT", "BLOCK",
                        f"'{banned}' used at display size", loc))
        _copy_and_emoji(line, loc, out)
    return out


def lint_code(text: str, path: Path) -> list[GateFailure]:
    out: list[GateFailure] = []
    lines = text.splitlines()
    inter = re.compile(r"fontFamily\s*:\s*['\"`]Inter['\"`]")
    fontsize = re.compile(r"fontSize\s*:\s*(\d+)")
    for i, line in enumerate(lines, 1):
        loc = f"{path.name}:{i}"
        for rule in BANNED["banned_tsx_patterns"]:
            if re.search(rule["regex"], line):
                out.append(GateFailure(rule["id"], "BLOCK",
                    rule.get("why", "banned pattern"), loc))
        for m in HEX_RE.finditer(line):
            val = m.group(1).lower()
            exp = "".join(c * 2 for c in val) if len(val) == 3 else val
            if exp not in ALLOWED_HEX:
                out.append(GateFailure("HEX-OFF-TOKEN", "BLOCK",
                    f"off-token color #{val} (brand tokens only)", loc))
        if inter.search(line):
            for m in fontsize.finditer(line):
                if int(m.group(1)) >= INTER_DISPLAY_MIN_PX:
                    out.append(GateFailure("INTER-DISPLAY", "BLOCK",
                        f"Inter at {m.group(1)}px display size", loc))
        _copy_and_emoji(line, loc, out)
    return out


def _copy_and_emoji(line: str, loc: str, out: list[GateFailure]) -> None:
    low = line.lower()
    for phrase in BANNED_DESIGNED_COPY:
        if phrase in low:
            out.append(GateFailure("BANNED-COPY", "BLOCK",
                f"banned designed-copy phrase '{phrase}'", loc))
    for glyph in EMOJI_ICONS:
        if glyph in line:
            out.append(GateFailure("EMOJI-ICON", "WARN",
                "emoji used as icon/bullet (hallmark gate 30)", loc))


def lint_file(path: Path) -> list[GateFailure]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in WEB_EXT:
        return lint_web(text, path)
    if path.suffix.lower() in CODE_EXT:
        return lint_code(text, path)
    return []


def collect(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            for ext in WEB_EXT | CODE_EXT:
                files.extend(p.rglob(f"*{ext}"))
        elif p.exists():
            files.append(p)
        else:
            print(f"[warn] not found: {p}")
    return sorted(set(files))


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    strict = "--strict" in argv
    files = collect([Path(a) for a in args])
    if not files:
        print("[warn] no lintable files")
        return 0
    findings: list[GateFailure] = []
    for f in files:
        findings.extend(lint_file(f))
    ok = report(findings, "design-core lint")
    print(f"[scanned] {len(files)} file(s)")
    if "--json" in argv:
        out = Path(argv[argv.index("--json") + 1])
        out.write_text(json.dumps([x.as_dict() for x in findings],
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if (strict and not ok) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
