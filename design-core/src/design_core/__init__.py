"""design-core: the shared WorqAI anti-slop enforcement package.

Markdown/JSON hold taste; Python enforces it. One brand contract, consumed by
every lane -- reels, carousels, single pictures, motion.
"""

from .contract import (
    ALLOWED_HEX,
    BANNED,
    COLORS,
    DUR_MS,
    MOTION,
    TOKENS,
    GateFailure,
    report,
)

__all__ = [
    "TOKENS", "COLORS", "MOTION", "DUR_MS", "BANNED", "ALLOWED_HEX",
    "GateFailure", "report",
]
