# PASTE THIS INTO CLAUDE

---

## CONTEXT

We are building the WorqAI carousel system. We have been exploring multiple background continuity techniques (algorithmic warping, per-slide recipe progressions, CSS effects, separate connected images). **ALL OF THESE ARE ABANDONED. Do not work on them.**

## THE ONLY APPROACH

The user generates ONE image containing all slide panels arranged in a grid (e.g., 5 panels in a 2x3 or 3x2 layout). A script extracts each panel, resizes it to 1080x1080, color-adapts it to WorqAI's design systems, and optionally applies visual treatments. This gives multiple variant sets from one source image.

## WHAT TO BUILD

### `scripts/panel_extractor.py`

A standalone script with these arguments:

- `--file FILE` (required) — the image with panels
- `--panels N` — number of panels to extract (default: 5)
- `--grid "rows,cols"` — grid layout, e.g., `"2,3"` or `"1,5"`. Auto-detected if omitted.
- `--name NAME` — becomes the bg_id slug (e.g., `"Deep Space"` → `deep-space`)
- `--output DIR` — base output directory (default: `./output`)
- `--systems s01,s04,s17,s29` — which design systems to generate variants for
- `--treatments none,glow,deep,soft,warm` — visual treatments to apply on top of color adaptation
- `--no-variants` — only extract panels, skip color adaptation and treatments
- `--preview` — show where panels will be extracted without actually doing it
- `--manifest PATH` — path to manifest.json (auto-detect if omitted)

### Pipeline

1. Load the image
2. Determine grid layout (auto-detect or use `--grid`):
   - Try all layouts that fit N panels (exact and near-fits)
   - Score by: panel squareness (30%) + fill efficiency (30%) + orientation match to image aspect ratio (40%)
3. If `--preview`: draw panel borders and numbers on a scaled preview, save as `{bg_id}_preview.png`, exit
4. Extract each panel using the grid, resize to 1080x1080
5. Save original extracted panel as `panel_XX/original.png`
6. For each panel, generate variants:
   - Color-adapt to each design system (numpy vectorized HSV hue shift)
   - Apply each treatment on top
   - Save as `panel_XX/{system_id}.png` and `panel_XX/{system_id}_{treatment}.png`
7. Update manifest.json with `recipe_variants["extracted"]` entry

### Color adaptation (numpy vectorized — no per-pixel loops)

Use these exact helpers:

```python
import numpy as np
from PIL import Image

def _rgb_to_hsv_np(rgb):
    """Convert float RGB (H,W,3) [0-1] -> H, S, V each (H,W) [0-1]."""
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    delta = mx - mn
    h = np.zeros_like(mx)
    mask = delta > 1e-9
    rc = np.where(mask, ((mx - r) / delta), 0)
    gc = np.where(mask, ((mx - g) / delta), 0)
    bc = np.where(mask, ((mx - b) / delta), 0)
    h = np.where((mx == r) & mask, (bc - gc), h)
    h = np.where((mx == g) & mask, (2.0 + rc - bc), h)
    h = np.where((mx == b) & mask, (4.0 + gc - rc), h)
    h = (h / 6.0) % 1.0
    s = np.where(mx > 1e-9, delta / mx, 0)
    return h, s, mx

def _hsv_to_rgb_np(h, s, v):
    """Convert HSV (H,W) [0-1] -> float RGB (H,W,3) [0-1]."""
    i = (h * 6.0).astype(int) % 6
    f = (h * 6.0) - np.floor(h * 6.0)
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    rgb = np.zeros((*h.shape, 3), dtype=np.float32)
    for idx in range(6):
        mask = i == idx
        if idx == 0:   rgb[mask] = np.stack([v[mask], t[mask], p[mask]], axis=-1)
        elif idx == 1: rgb[mask] = np.stack([q[mask], v[mask], p[mask]], axis=-1)
        elif idx == 2: rgb[mask] = np.stack([p[mask], v[mask], t[mask]], axis=-1)
        elif idx == 3: rgb[mask] = np.stack([p[mask], q[mask], v[mask]], axis=-1)
        elif idx == 4: rgb[mask] = np.stack([t[mask], p[mask], v[mask]], axis=-1)
        else:          rgb[mask] = np.stack([v[mask], p[mask], q[mask]], axis=-1)
    return np.clip(rgb, 0, 1)

def _hex_to_hue(hex_c):
    hex_c = hex_c.lstrip("#")
    r = int(hex_c[0:2], 16) / 255.0
    g = int(hex_c[2:4], 16) / 255.0
    b = int(hex_c[4:6], 16) / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 1e-9: return 0.0
    if mx == r: return (60 * ((g - b) / d) + 360) % 360
    if mx == g: return (60 * ((b - r) / d) + 120) % 360
    return (60 * ((r - g) / d) + 240) % 360

def adapt_hue(img_arr, target_hex, strength=0.85):
    target_hue = _hex_to_hue(target_hex)
    rgb = img_arr[:, :, :3].astype(np.float32) / 255.0
    h, s, v = _rgb_to_hsv_np(rgb)
    source_h = np.degrees(np.arctan2(
        (np.sin(h * 2 * np.pi) * s * v).sum(),
        (np.cos(h * 2 * np.pi) * s * v).sum()
    ))
    source_h = (source_h + 360) % 360
    diff = (target_hue - source_h + 360) % 360
    if diff > 180: diff -= 360
    h = (h + diff / 360.0) % 1.0
    # Saturation nudge toward target
    tr = np.array([int(target_hex.lstrip("#")[i:i+2], 16) / 255.0 for i in (0, 2, 4)])
    _, ts, _ = _rgb_to_hsv_np(tr.reshape(1, 1, 3))
    s = np.clip(s + (float(ts[0, 0]) - s.mean()) * strength * 0.3, 0, 1)
    adapted = _hsv_to_rgb_np(h, s, v)
    out = (adapted * 255).astype(np.uint8)
    if img_arr.shape[2] == 4:
        out = np.dstack([out, img_arr[:, :, 3]])
    return out
```

### Design systems

```python
DESIGN_SYSTEMS = {
    "s01": {"name": "Premium",   "accent": "#E8B86D"},
    "s04": {"name": "Corporate", "accent": "#4A6FA5"},
    "s17": {"name": "Brand",     "accent": "#C7FF3A"},
    "s29": {"name": "Cyber",     "accent": "#00F0FF"},
}
```

### Treatments (applied after color adaptation)

```python
from PIL import Image, ImageEnhance, ImageFilter

def apply_warm(img):
    arr = np.array(img).astype(np.float32)
    arr[:, :, 0] *= 1.08
    arr[:, :, 2] *= 0.95
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

TREATMENTS = {
    "none": lambda img: img,
    "glow": lambda img: ImageEnhance.Color(ImageEnhance.Brightness(img).enhance(1.08)).enhance(1.2),
    "deep": lambda img: ImageEnhance.Contrast(img.filter(ImageFilter.UnsharpMask(radius=2, percent=120))).enhance(1.12),
    "soft": lambda img: ImageEnhance.Brightness(ImageEnhance.Color(img.filter(ImageFilter.GaussianBlur(radius=0.8))).enhance(0.88)).enhance(0.95),
    "warm": apply_warm,
}
```

### Output structure

```
{output_dir}/{bg_id}/
  panel_01/
    original.png
    s17.png, s17_glow.png, s17_deep.png, ...
    s29.png, s29_glow.png, ...
  panel_02/
    original.png
    s17.png, s17_glow.png, ...
  ...
```

### Manifest format

```json
{
  "backgrounds": [
    {
      "id": "bg-id-slug",
      "recipe_variants": {
        "extracted": {
          "s17": ["path/to/panel_01/s17.png", "path/to/panel_02/s17.png", ...],
          "s29": ["path/to/panel_01/s29.png", ...]
        }
      },
      "source": "panel extraction from filename.png, N panels",
      "panels": 5
    }
  ]
}
```

### Integration notes

- `render_carousel.py` already reads `recipe_variants["extracted"][system_id][slide_index]` — no changes needed there
- `adapt_image_bg.py` is a separate tool for single-image adaptation — keep it, this script is self-contained
- Create directories: `ideation/ai-backgrounds/` and `ideation/ai-backgrounds/panels/` for the user to drop images

### EXPLICITLY ABANDONED

- `transform_bg_v2.py` and all its recipes (curl_flow, glow_bloom, deep_zoom, phase_distort, etc.)
- Per-slide recipe progressions
- CSS continuity approaches
- Generating separate-but-connected images
- Panoramic strip cutting — this is panel extraction from grids, not wide strips

### Success criteria

1. `python scripts/panel_extractor.py --help` shows all arguments
2. `python scripts/panel_extractor.py --file image.png --panels 5 --preview` generates a preview with panel borders
3. `python scripts/panel_extractor.py --file image.png --grid 2,3 --name "Test" --output brand/generated-bg` extracts panels and generates system variants
4. Manifest is correctly updated with `recipe_variants["extracted"]`
5. Color adaptation produces visibly different results per system
6. Works with any number of panels (3-10+)
