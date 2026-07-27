"""Crop the official WorqAI wordmark to its visible alpha bounds.

The source artwork has unusually large transparent margins. Browsers size the
transparent canvas, which makes the visible logo look clipped or badly pasted
inside small carousel labels.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE = (
    ROOT
    / ".."
    / ".."
    / ".."
    / "higgsfield-worqai-ats-2026-07-21"
    / "sources"
    / "worqai-official"
    / "logo2_no_bg.png"
).resolve()
OUTPUT = ROOT / "brand" / "worqai-wordmark-cropped.png"

image = Image.open(SOURCE).convert("RGBA")
alpha_bounds = image.getchannel("A").getbbox()
if alpha_bounds is None:
    raise RuntimeError(f"No visible pixels found in {SOURCE}")

# A small transparent breathing margin keeps anti-aliased edge pixels intact.
left, top, right, bottom = alpha_bounds
pad = 22
box = (
    max(0, left - pad),
    max(0, top - pad),
    min(image.width, right + pad),
    min(image.height, bottom + pad),
)
cropped = image.crop(box)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
cropped.save(OUTPUT, optimize=True)
print(f"Saved {OUTPUT} at {cropped.width}x{cropped.height}")
