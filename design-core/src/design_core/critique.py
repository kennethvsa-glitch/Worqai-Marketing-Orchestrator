"""Pre-emit six-axis self-critique, shared by every lane.

Adapted from nutlope/hallmark's pre-emit critique. Before an asset (reel,
carousel, picture, motion) is submitted for human review, score it 1-5 on
each axis. Any axis < 3 forces a revision pass before review.

This module records and validates the scores; the scoring itself is Claude's
creative judgment, written into the asset's QA record.

Usage (as a check on a scores JSON):
    python -m design_core.critique scores.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .contract import GateFailure, report

AXES = {
    "philosophy": "Does this asset take a position, or is it just elements arranged?",
    "hierarchy": "In 2 seconds, is it obvious what to look at first?",
    "execution": "Tokens, timing, contrast all in spec?",
    "specificity": "Does it look like THIS topic/person, or any generic asset?",
    "restraint": "Has everything not earning its place been removed?",
    "variety": "Does it share a structural fingerprint with a previous asset?",
}
MIN_PASS = 3


def check(scores: dict) -> list[GateFailure]:
    findings: list[GateFailure] = []
    for axis in AXES:
        if axis not in scores:
            findings.append(GateFailure("CRITIQUE", "BLOCK", f"missing axis '{axis}'"))
            continue
        v = scores[axis]
        if not isinstance(v, (int, float)) or not (1 <= v <= 5):
            findings.append(GateFailure("CRITIQUE", "BLOCK", f"axis '{axis}' must be 1-5, got {v!r}"))
        elif v < MIN_PASS:
            findings.append(GateFailure("CRITIQUE", "BLOCK",
                f"axis '{axis}' scored {v} (<{MIN_PASS}); revise before review"))
    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print("Axes:", ", ".join(AXES))
        return 2
    scores = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    ok = report(check(scores), "design-core critique")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
