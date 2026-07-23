"""Loads the WorqAI design contract from brand/*.json.

design-core architecture: Markdown/JSON hold taste; Python enforces it. This
module is the single bridge every lane imports. Nothing here renders or
mutates -- it exposes the locked tokens, motion language, and banned lists,
plus the GateFailure/report helpers shared by the linter and frame auditor.
"""

from __future__ import annotations

import json
from pathlib import Path

# design-core/src/design_core/contract.py -> design-core/
ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"


def _load(name: str) -> dict:
    return json.loads((BRAND / name).read_text(encoding="utf-8"))


TOKENS = _load("tokens.json")
MOTION = _load("motion.json")
BANNED = _load("banned.json")

# Convenience views ----------------------------------------------------------

COLORS = {k: v["hex"] for k, v in TOKENS["colors"].items()}
ALLOWED_HEX = {h.lstrip("#").lower() for h in COLORS.values()}
ACCENT_MAX_FRACTION = TOKENS["rules"]["accent_max_fraction"]
INTER_DISPLAY_MIN_PX = TOKENS["rules"]["inter_display_min_px"]

DUR_MS = MOTION["durations_ms"]
EXIT_RATIO = MOTION["exit_ratio"]

BANNED_DESIGNED_COPY = BANNED["banned_designed_copy"]
BANNED_DISPLAY_FONTS = BANNED["banned_display_fonts"]
EMOJI_ICONS = BANNED["emoji_icons"]


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


class GateFailure:
    """One enforcement finding. severity BLOCK stops the lane."""

    def __init__(self, gate: str, severity: str, message: str, where: str = ""):
        self.gate = gate
        self.severity = severity  # BLOCK | WARN
        self.message = message
        self.where = where

    def as_dict(self) -> dict:
        return {"gate": self.gate, "severity": self.severity,
                "message": self.message, "where": self.where}

    def __repr__(self) -> str:
        loc = f" {self.where}" if self.where else ""
        return f"[{self.severity}] {self.gate}{loc}: {self.message}"


def report(findings: list[GateFailure], label: str) -> bool:
    """Print ASCII-only; return True when no BLOCK finding exists."""
    for f in findings:
        print(repr(f))
    blocks = sum(1 for f in findings if f.severity == "BLOCK")
    warns = sum(1 for f in findings if f.severity == "WARN")
    if not findings:
        print(f"[{label}] ok, no findings")
    else:
        print(f"[{label}] {blocks} blocking, {warns} warning(s)")
    return blocks == 0
