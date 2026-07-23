#!/usr/bin/env python3
"""
panel_extractor.py  -  Extract panels from a grid image, color-adapt to design
systems, apply visual treatments, and update the carousel background manifest.

The idea: generate ONE image in ChatGPT with N panels arranged in a grid
(e.g. 2x3 or 1x5). This script extracts each panel, resizes to 1080x1080,
color-adapts to every WorqAI visual system, and optionally applies treatments.
Result: one source image -> dozens of unique carousel-ready backgrounds.

IMPORTANT — "Always extract everything" policy:
    This script ALWAYS extracts ALL panels the source image contains, even if
    the carousel only needs a subset.  The carousel spec's bg_recipe sequence
    clamps to available panels at render time.  Never under-extract.

    Panel count authority (highest wins):
      1. --panels flag (explicit override)
      2. Filename   (e.g. "8 panels.png" → 8)
      3. Visual seam detection fallback

Usage:
    py scripts/panel_extractor.py --file my-grid.png --preview
    py scripts/panel_extractor.py --file my-grid.png --name "Deep Space"
    py scripts/panel_extractor.py --file my-grid.png --grid 2,3 --name "Nebula" --treatments none,glow,deep
    py scripts/panel_extractor.py --file my-grid.png --panels 8 --compare

Input file search order:
    1. ideation/ai-backgrounds/panels/{file}
    2. ideation/ai-backgrounds/{file}
    3. Path as-is (absolute or relative to cwd)

Auto-detection:
    --panels is now OPTIONAL. The script will:
    1. Parse panel count from --panels flag
    2. Parse panel count from filename (e.g. "8 panels.png" -> 8)
    3. Fall back to visual seam detection on the image itself
    4. Detect exact seam positions for pixel-perfect cropping
"""

import argparse
import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

# Suppress numpy divide-by-zero warnings from HSV operations on black pixels
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*divide by zero.*")

ROOT = Path(__file__).parent.parent
PANELS_DIR     = ROOT / "ideation" / "ai-backgrounds" / "panels"
AI_BG_DIR      = ROOT / "ideation" / "ai-backgrounds"
OUTPUT_DEFAULT = ROOT / "brand" / "generated-bg"
MANIFEST_PATH  = ROOT / "brand" / "generated-bg" / "manifest.json"

# ── Design systems ────────────────────────────────────────────────────────────
DESIGN_SYSTEMS = {
    "s01": {"name": "NOIR GOLD",       "accent": "#C8A84B"},
    "s02": {"name": "ROYAL BLUE",      "accent": "#4a8fff"},
    "s04": {"name": "CRIMSON NIGHT",   "accent": "#e05a7a"},
    "s06": {"name": "AURORA",          "accent": "#a855f7"},
    "s08": {"name": "GLASSMORPHISM",   "accent": "#60a5fa"},
    "s09": {"name": "CHROME SILVER",   "accent": "#b0bcd4"},
    "s11": {"name": "TROPIC",          "accent": "#00d68f"},
    "s14": {"name": "DEEP SEA",        "accent": "#38bdf8"},
    "s16": {"name": "NEON GRID",       "accent": "#00f0a0"},
    "s17": {"name": "WORQAI VERDE",    "accent": "#C7FF3A"},
    "s20": {"name": "Y2K CHROME",      "accent": "#44f5ff"},
    "s21": {"name": "VAPOR GRIDWAVE",  "accent": "#ffef74"},
    "s22": {"name": "DARK ACADEMIA",   "accent": "#c39d63"},
    "s25": {"name": "SWISS BRUT",      "accent": "#ff0015"},
    "s27": {"name": "NEO RISO",        "accent": "#00ffd1"},
    "s29": {"name": "CYBERPUNK ALLEY", "accent": "#00ff9c"},
    "s33": {"name": "CLEAN SAAS",      "accent": "#3b82f6"},
    "s40": {"name": "GLITCH",          "accent": "#22d3ee"},
    "s41": {"name": "HOLOGRAPHIC",     "accent": "#c084fc"},
}

# ── Vectorized HSV helpers ───────────────────────────────────────────────────

def _rgb_to_hsv_np(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    delta = mx - mn
    h = np.zeros_like(mx)
    mask = delta > 1e-9
    safe_delta = np.where(mask, delta, 1.0)
    rc = np.where(mask, (mx - r) / safe_delta, 0.0)
    gc = np.where(mask, (mx - g) / safe_delta, 0.0)
    bc = np.where(mask, (mx - b) / safe_delta, 0.0)
    h = np.where((mx == r) & mask, (bc - gc), h)
    h = np.where((mx == g) & mask, 2.0 + rc - bc, h)
    h = np.where((mx == b) & mask, 4.0 + gc - rc, h)
    h = (h / 6.0) % 1.0
    s = np.where(mx > 1e-9, delta / mx, 0.0)
    return h, s, mx


def _hsv_to_rgb_np(h, s, v):
    i = (h * 6.0).astype(int) % 6
    f = (h * 6.0) - np.floor(h * 6.0)
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    rgb = np.zeros((*h.shape, 3), dtype=np.float32)
    for idx, (rv, gv, bv) in enumerate([
        (v, t, p), (q, v, p), (p, v, t),
        (p, q, v), (t, p, v), (v, p, q),
    ]):
        mask = i == idx
        rgb[mask] = np.stack([rv[mask], gv[mask], bv[mask]], axis=-1)
    return np.clip(rgb, 0.0, 1.0)


def _hex_to_hue(hex_c: str) -> float:
    hex_c = hex_c.lstrip("#")
    r = int(hex_c[0:2], 16) / 255.0
    g = int(hex_c[2:4], 16) / 255.0
    b = int(hex_c[4:6], 16) / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 1e-9:
        return 0.0
    if mx == r:
        return (60.0 * ((g - b) / d) + 360.0) % 360.0
    if mx == g:
        return (60.0 * ((b - r) / d) + 120.0) % 360.0
    return (60.0 * ((r - g) / d) + 240.0) % 360.0


def adapt_hue(img_arr: np.ndarray, target_hex: str, strength: float = 0.85) -> np.ndarray:
    target_hue = _hex_to_hue(target_hex)
    rgb = img_arr[:, :, :3].astype(np.float32) / 255.0
    h, s, v = _rgb_to_hsv_np(rgb)

    weights = s * v
    sin_sum = (np.sin(h * 2 * np.pi) * weights).sum()
    cos_sum = (np.cos(h * 2 * np.pi) * weights).sum()
    source_h = (np.degrees(np.arctan2(sin_sum, cos_sum)) + 360.0) % 360.0

    diff = (target_hue - source_h + 360.0) % 360.0
    if diff > 180.0:
        diff -= 360.0
    h = (h + diff / 360.0) % 1.0

    tr = np.array([int(target_hex.lstrip("#")[i: i + 2], 16) / 255.0 for i in (0, 2, 4)])
    _, ts, _ = _rgb_to_hsv_np(tr.reshape(1, 1, 3))
    s = np.clip(s + (float(ts[0, 0]) - s.mean()) * strength * 0.3, 0.0, 1.0)

    adapted = _hsv_to_rgb_np(h, s, v)
    out = (adapted * 255.0).astype(np.uint8)
    if img_arr.shape[2] == 4:
        out = np.dstack([out, img_arr[:, :, 3]])
    return out


# ── Treatments ────────────────────────────────────────────────────────────────

def _apply_warm(img: Image.Image) -> Image.Image:
    arr = np.array(img).astype(np.float32)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.08, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.95, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


TREATMENTS: dict = {
    "none": lambda img: img,
    "glow": lambda img: ImageEnhance.Color(
        ImageEnhance.Brightness(img).enhance(1.08)
    ).enhance(1.2),
    "deep": lambda img: ImageEnhance.Contrast(
        img.filter(ImageFilter.UnsharpMask(radius=2, percent=120))
    ).enhance(1.12),
    "soft": lambda img: ImageEnhance.Brightness(
        ImageEnhance.Color(
            img.filter(ImageFilter.GaussianBlur(radius=0.8))
        ).enhance(0.88)
    ).enhance(0.95),
    "warm": _apply_warm,
}

# ── Auto panel-count detection ────────────────────────────────────────────────

def detect_panels_from_filename(filename: str) -> int | None:
    """Parse panel count from filename patterns like '8 panels', '6 panel', etc."""
    # Match patterns: "8 panels", "6 panel", "9 panels" etc.
    patterns = [
        r'(\d+)\s+panels?',
        r'(\d+)\s+panel',
        r'(\d+)p',
    ]
    for pat in patterns:
        m = re.search(pat, filename, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def compute_edge_profile(gray: np.ndarray, axis: int) -> np.ndarray:
    """
    Compute edge strength profile along an axis.
    axis=0: horizontal profile (diff between consecutive rows)
    axis=1: vertical profile (diff between consecutive cols)
    """
    if axis == 0:
        diff = np.abs(gray[1:, :].astype(np.float32) - gray[:-1, :].astype(np.float32))
        return diff.mean(axis=1)
    else:
        diff = np.abs(gray[:, 1:].astype(np.float32) - gray[:, :-1].astype(np.float32))
        return diff.mean(axis=0)


def smooth_profile(profile: np.ndarray, window_ratio: float = 0.01) -> np.ndarray:
    """Light smoothing to reduce noise."""
    size = len(profile)
    window = max(1, int(size * window_ratio))
    if window <= 1:
        return profile
    kernel = np.ones(window) / window
    return np.convolve(profile, kernel, mode='same')


def find_peaks(profile: np.ndarray, min_prominence: float = 0.08,
                edge_margin_ratio: float = 0.03) -> list[tuple[int, float]]:
    """Find local maxima in profile with minimum prominence.
    Rejects peaks too close to image edges (likely image boundary artifacts)."""
    pmin, pmax = profile.min(), profile.max()
    if pmax - pmin < 1e-9:
        return []
    norm = (profile - pmin) / (pmax - pmin)

    edge_margin = max(3, int(len(norm) * edge_margin_ratio))

    peaks = []
    for i in range(1, len(norm) - 1):
        pos = i + 1  # diff[i] is between pixel i and i+1
        # Skip peaks too close to edges
        if pos < edge_margin or pos > len(norm) - edge_margin:
            continue
        if norm[i] > min_prominence and norm[i] > norm[i - 1] and norm[i] >= norm[i + 1]:
            valley = max(norm[i - 1], norm[i + 1])
            prominence = norm[i] - valley
            if prominence >= min_prominence * 0.5:
                peaks.append((pos, norm[i]))
    return peaks


def find_evenly_spaced_subset(peaks: list[tuple[int, float]], total_size: int,
                               max_sections: int = 12) -> list[int]:
    """
    From a list of peak positions, find the best set of evenly-spaced peaks
    that divide the image into roughly equal sections.
    Returns sorted list of seam positions.
    """
    if not peaks:
        return []

    positions = [p[0] for p in peaks]
    strengths = {p[0]: p[1] for p in peaks}

    best_score = -1.0
    best_seams: list[int] = []

    for n_sections in range(2, max_sections + 1):
        expected_step = total_size / n_sections
        n_seams = n_sections - 1

        # Try each strong peak as anchor
        for anchor_pos, anchor_str in peaks[:min(5, len(peaks))]:
            for phase in range(-int(expected_step * 0.25), int(expected_step * 0.25) + 1, 2):
                start = anchor_pos + phase
                if start < expected_step * 0.3 or start > total_size - expected_step * 0.3:
                    continue

                seams = []
                score = 0.0
                valid = True

                for s in range(n_seams):
                    target = start + int(expected_step * s)
                    if target >= total_size:
                        valid = False
                        break

                    # Search window
                    search_radius = max(3, int(expected_step * 0.15))
                    best_local = None
                    best_local_str = -1.0

                    for pos in positions:
                        if abs(pos - target) <= search_radius:
                            if strengths[pos] > best_local_str:
                                best_local_str = strengths[pos]
                                best_local = pos

                    if best_local is None:
                        valid = False
                        break

                    seams.append(best_local)
                    # Score = strength - penalty for deviation from expected
                    deviation = abs(best_local - target) / max(1, expected_step)
                    score += best_local_str * (1.0 - deviation * 0.5)

                if valid and len(seams) == n_seams:
                    # Bonus for consistency: all seams should be roughly equally spaced
                    spacings = [seams[i + 1] - seams[i] for i in range(len(seams) - 1)]
                    if spacings:
                        spacing_std = np.std(spacings)
                        spacing_mean = np.mean(spacings)
                        consistency = max(0, 1.0 - spacing_std / max(spacing_mean * 0.3, 1))
                        score += consistency * 0.5 * n_seams

                    if score > best_score:
                        best_score = score
                        best_seams = seams

    return sorted(list(dict.fromkeys(best_seams)))  # dedupe while preserving order


def detect_grid_auto(img: Image.Image) -> tuple[int, int, int]:
    """
    Auto-detect grid layout from visual seams.
    Returns (rows, cols, n_panels).
    """
    gray = np.array(img.convert('L'))
    h, w = gray.shape

    h_profile = smooth_profile(compute_edge_profile(gray, axis=0))
    v_profile = smooth_profile(compute_edge_profile(gray, axis=1))

    h_peaks = find_peaks(h_profile)
    v_peaks = find_peaks(v_profile)

    h_seams = find_evenly_spaced_subset(h_peaks, h)
    v_seams = find_evenly_spaced_subset(v_peaks, w)

    n_rows = len(h_seams) + 1
    n_cols = len(v_seams) + 1
    n_panels = n_rows * n_cols

    return n_rows, n_cols, n_panels


def detect_grid_from_seams(img: Image.Image, n_panels: int) -> tuple[int, int, list[int], list[int]]:
    """
    Given expected panel count, detect exact seam positions for pixel-perfect cropping.
    Returns (rows, cols, h_seams, v_seams) where seams are boundary pixel positions.
    """
    gray = np.array(img.convert('L'))
    h, w = gray.shape

    # First, find the best (rows, cols) layout
    best_rows, best_cols = detect_grid_layout(w, h, n_panels)

    h_profile = smooth_profile(compute_edge_profile(gray, axis=0))
    v_profile = smooth_profile(compute_edge_profile(gray, axis=1))

    h_peaks = find_peaks(h_profile)
    v_peaks = find_peaks(v_profile)

    h_seams = find_seams_given_sections(h_peaks, h, best_rows)
    v_seams = find_seams_given_sections(v_peaks, w, best_cols)

    return best_rows, best_cols, h_seams, v_seams


def detect_grid_layout(img_w: int, img_h: int, n_panels: int) -> tuple[int, int]:
    """Return (rows, cols) best matching n_panels for the given image dimensions."""
    img_aspect = img_w / img_h
    best: tuple[int, int] = (1, n_panels)
    best_score = -1.0

    for rows in range(1, n_panels + 1):
        cols = -(-n_panels // rows)
        pw = img_w / cols
        ph = img_h / rows
        panel_aspect = pw / ph

        squareness = min(pw, ph) / max(pw, ph)
        fill = n_panels / (rows * cols)
        grid_aspect = cols / rows
        orientation = 1.0 / (1.0 + abs(img_aspect - grid_aspect * panel_aspect))

        score = squareness * 0.30 + fill * 0.30 + orientation * 0.40
        if score > best_score:
            best_score = score
            best = (rows, cols)
    return best


def find_seams_given_sections(peaks: list[tuple[int, float]], total_size: int,
                               n_sections: int) -> list[int]:
    """
    Given detected peaks and expected number of sections,
    find the exact n_sections-1 seam positions.
    """
    if n_sections <= 1:
        return []

    expected_step = total_size / n_sections
    n_seams = n_sections - 1

    positions = [p[0] for p in peaks]
    strengths = {p[0]: p[1] for p in peaks}

    best_score = -1.0
    best_seams: list[int] = []

    # Try multiple anchors including synthetic anchors at expected positions
    anchors = peaks[:min(10, len(peaks))]
    # Also try synthetic anchors near each expected seam position
    for i in range(n_seams):
        expected_pos = int(expected_step * (i + 0.5))
        anchors.append((expected_pos, 0.0))

    for anchor_pos, anchor_str in anchors:
        for phase in range(-int(expected_step * 0.3), int(expected_step * 0.3) + 1, 1):
            start = anchor_pos + phase
            if start < expected_step * 0.2 or start > total_size - expected_step * 0.2:
                continue

            seams = []
            score = 0.0
            valid = True

            for s in range(n_seams):
                target = int(start + expected_step * s)
                if target >= total_size - 1:
                    valid = False
                    break

                search_radius = max(5, int(expected_step * 0.15))
                best_local = None
                best_local_str = -1.0

                for pos in positions:
                    if abs(pos - target) <= search_radius:
                        if strengths[pos] > best_local_str:
                            best_local_str = strengths[pos]
                            best_local = pos

                if best_local is None:
                    # No peak found near target — this anchor is weak
                    valid = False
                    break

                seams.append(best_local)
                deviation = abs(best_local - target) / max(1, expected_step)
                score += (best_local_str + 0.1) * (1.0 - deviation)

            if valid and len(seams) == n_seams:
                # Consistency bonus: all seams should be roughly equally spaced
                spacings = [seams[i + 1] - seams[i] for i in range(len(seams) - 1)]
                if spacings:
                    spacing_std = np.std(spacings)
                    spacing_mean = np.mean(spacings)
                    consistency = max(0, 1.0 - spacing_std / max(spacing_mean * 0.25, 1))
                    score += consistency * n_seams * 2.0  # Heavy weight on consistency

                # Sanity check: no seam should be within 2% of image edge
                edge_margin = total_size * 0.02
                if all(edge_margin < s < total_size - edge_margin for s in seams):
                    if score > best_score:
                        best_score = score
                        best_seams = seams

    # If no good seams found, fall back to mathematical division
    if not best_seams:
        best_seams = [int(total_size * i / n_sections) for i in range(1, n_sections)]
        print(f"[SEAMS] Falling back to mathematical division: {best_seams}")

    return sorted(list(dict.fromkeys(best_seams)))


# ── Panel extraction with exact seam positions ─────────────────────────────────

def extract_panels_with_seams(img: Image.Image, h_seams: list[int], v_seams: list[int],
                               n_panels: int) -> list[Image.Image]:
    """
    Extract panels using exact seam positions for pixel-perfect cropping.
    h_seams: list of row boundary positions (0 < pos < H)
    v_seams: list of column boundary positions (0 < pos < W)
    """
    W, H = img.size

    # Build full boundary lists including edges
    h_bounds = [0] + h_seams + [H]
    v_bounds = [0] + v_seams + [W]

    panels = []
    for r in range(len(h_bounds) - 1):
        for c in range(len(v_bounds) - 1):
            if len(panels) >= n_panels:
                break
            y0, y1 = h_bounds[r], h_bounds[r + 1]
            x0, x1 = v_bounds[c], v_bounds[c + 1]
            panels.append(img.crop((x0, y0, x1, y1)))

    return panels


def extract_panels_fallback(img: Image.Image, rows: int, cols: int,
                            n_panels: int) -> list[Image.Image]:
    """Fallback: mathematical division when seam detection fails."""
    W, H = img.size
    pw, ph = W // cols, H // rows
    panels = []
    for r in range(rows):
        for c in range(cols):
            if len(panels) >= n_panels:
                break
            x0, y0 = c * pw, r * ph
            panels.append(img.crop((x0, y0, x0 + pw, y0 + ph)))
    return panels


# ── Preview ───────────────────────────────────────────────────────────────────

def draw_preview(img: Image.Image, rows: int, cols: int, n_panels: int,
                 h_seams: list[int], v_seams: list[int], out: Path) -> None:
    PREVIEW_W = 1400
    scale = PREVIEW_W / img.width
    prev_h = int(img.height * scale)
    preview = img.resize((PREVIEW_W, prev_h), Image.LANCZOS).convert("RGB")
    draw = ImageDraw.Draw(preview)

    # Draw seam lines in red (detected seams)
    for seam in h_seams:
        y = int(seam * scale)
        draw.line([(0, y), (PREVIEW_W, y)], fill=(255, 0, 0), width=2)
    for seam in v_seams:
        x = int(seam * scale)
        draw.line([(x, 0), (x, prev_h)], fill=(255, 0, 0), width=2)

    # Draw panel labels
    h_bounds = [0] + h_seams + [img.height]
    v_bounds = [0] + v_seams + [img.width]

    for r in range(len(h_bounds) - 1):
        for c in range(len(v_bounds) - 1):
            idx = r * (len(v_bounds) - 1) + c
            if idx >= n_panels:
                break
            y0 = int(h_bounds[r] * scale)
            y1 = int(h_bounds[r + 1] * scale)
            x0 = int(v_bounds[c] * scale)
            x1 = int(v_bounds[c + 1] * scale)
            draw.rectangle([x0 + 2, y0 + 2, x1 - 3, y1 - 3],
                           outline=(255, 220, 0), width=3)
            label = f"Panel {idx + 1}"
            draw.rectangle([x0 + 8, y0 + 8, x0 + 130, y0 + 38], fill=(0, 0, 0, 180))
            draw.text((x0 + 12, y0 + 10), label, fill=(255, 220, 0))

    out.parent.mkdir(parents=True, exist_ok=True)
    preview.save(str(out))
    print(f"[PREVIEW] {out}")
    print(f"          Grid: {rows}x{cols}, {n_panels} panels outlined")
    print(f"          Red lines = detected seams")
    print(f"          Open the preview image and confirm panel borders look right.")
    print(f"          Then rerun without --preview to extract.")


# ── Kit comparison visualization ───────────────────────────────────────────────

def build_kit_comparison(output_dir: Path, bg_id: str, systems: list[str], n_panels: int) -> None:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
    except ImportError:
        print("[SKIP] --compare requires matplotlib: pip install matplotlib")
        return

    THUMB = 180
    system_labels = [f"{sid}  {DESIGN_SYSTEMS[sid]['name']}" for sid in systems]

    fig = plt.figure(figsize=(n_panels * 2.4, len(systems) * 2.6))
    gs = gridspec.GridSpec(len(systems), n_panels, hspace=0.12, wspace=0.06)

    for row_i, sys_id in enumerate(systems):
        for col_i in range(n_panels):
            panel_num = f"panel_{col_i + 1:02d}"
            img_path = output_dir / panel_num / f"{sys_id}.png"
            ax = fig.add_subplot(gs[row_i, col_i])
            if img_path.exists():
                thumb = Image.open(img_path).resize((THUMB, THUMB), Image.LANCZOS)
                ax.imshow(thumb)
            else:
                ax.set_facecolor("#111")
                ax.text(0.5, 0.5, "missing", ha="center", va="center",
                        color="red", transform=ax.transAxes)
            ax.axis("off")
            if row_i == 0:
                ax.set_title(f"Slide {col_i + 1}", fontsize=9, color="#ccc")
            if col_i == 0:
                ax.set_ylabel(system_labels[row_i], fontsize=8, rotation=0,
                              ha="right", va="center", color="#eee")

    total = n_panels * len(systems)
    fig.patch.set_facecolor("#0a0a0a")
    plt.suptitle(
        f"1 IMAGE -> {len(systems)} SYSTEMS x {n_panels} PANELS = {total} UNIQUE SLIDES\n"
        f"Background: {bg_id}",
        fontsize=12, fontweight="bold", color="white", y=0.98,
    )

    compare_path = output_dir / f"{bg_id}_kit_comparison.png"
    plt.savefig(str(compare_path), dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"[COMPARE] {compare_path}")
    print(f"          {len(systems)} systems x {n_panels} panels = {total} slides visualized")


# ── Manifest helpers ──────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").strip("-")


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"backgrounds": []}


def save_manifest(manifest: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


# ── Post-extraction sanity check ─────────────────────────────────────────────

def _sanity_check_panels(panels: list, rows: int, cols: int) -> None:
    """Check each extracted panel for strong internal seams.

    A strong vertical or horizontal edge running through the center of a 1080x1080
    panel is a reliable indicator that the crop captured two sub-panels instead of one.
    Prints a WARNING for every suspicious panel — does not abort.
    """
    THRESHOLD = 18.0   # mean absolute difference across the center slice
    MARGIN    = 0.35   # check the middle 30% of the panel (skip outer 35% each side)

    bad: list[int] = []
    for idx, panel in enumerate(panels):
        arr = np.array(panel.convert("L")).astype(np.float32)
        H, W = arr.shape
        lo_r, hi_r = int(H * MARGIN), int(H * (1 - MARGIN))
        lo_c, hi_c = int(W * MARGIN), int(W * (1 - MARGIN))

        # Vertical edge at horizontal center
        cx = W // 2
        v_diff = float(np.abs(arr[lo_r:hi_r, cx] - arr[lo_r:hi_r, cx - 1]).mean())

        # Horizontal edge at vertical center
        cy = H // 2
        h_diff = float(np.abs(arr[cy, lo_c:hi_c] - arr[cy - 1, lo_c:hi_c]).mean())

        if v_diff > THRESHOLD or h_diff > THRESHOLD:
            bad.append(idx + 1)

    if bad:
        print(f"\n[SANITY] WARNING: panels {bad} have strong internal edges "
              f"(v or h diff > {THRESHOLD}). This usually means the crop captured "
              f"two sub-panels. Check --preview, then re-run with explicit --panels "
              f"or --grid if the count looks wrong.")
    else:
        print(f"[SANITY] All {len(panels)} panels passed internal-edge check.")


# ── Gutter trimming + edge quality check ─────────────────────────────────────

def trim_panel_gutters(img: Image.Image, trim_pct: float) -> Image.Image:
    """
    Crop trim_pct% from each edge of a panel, then resize back to original size.
    Removes canvas margins, ChatGPT grid gutters, and white outer borders baked
    into the source image by the generator's layout engine.

    trim_pct: percentage of each side to remove (e.g. 3.0 = 3% from all 4 edges).
    Recommended: 2 for thin gutters, 3-4 for full canvas-margin images.
    The panel is resized back to 1080x1080 after trimming so downstream code
    is unaffected.
    """
    if trim_pct <= 0:
        return img
    W, H = img.size
    trim_x = max(1, int(W * trim_pct / 100))
    trim_y = max(1, int(H * trim_pct / 100))
    cropped = img.crop((trim_x, trim_y, W - trim_x, H - trim_y))
    return cropped.resize((W, H), Image.LANCZOS)


def check_bright_edges(img: Image.Image, panel_idx: int,
                        threshold: float = 228.0, band_px: int = 10) -> bool:
    """
    Detect near-white outer edges in an extracted panel — the signature of
    unguttered canvas margins left by ChatGPT's grid generation or collage mode.

    Checks a band of pixels along each of the 4 edges. If any band's mean
    brightness exceeds `threshold` (0–255), the panel likely has a visible
    white/gray border that will ruin the carousel slide background.

    Returns True if a bright edge is found. Prints a [WARN] message naming
    the offending edge(s) so the user knows to use --trim-gutters.
    """
    arr = np.array(img.convert("RGB")).astype(np.float32)
    H, W = arr.shape[:2]
    band = max(4, min(band_px, H // 8, W // 8))

    named = {
        "top":    float(arr[:band, :, :].mean()),
        "bottom": float(arr[-band:, :, :].mean()),
        "left":   float(arr[:, :band, :].mean()),
        "right":  float(arr[:, -band:, :].mean()),
    }

    bright = {name: val for name, val in named.items() if val > threshold}
    if bright:
        edges_str = ", ".join(f"{k}({v:.0f})" for k, v in sorted(bright.items()))
        print(f"  [WARN] Panel {panel_idx + 1} has bright edge — {edges_str} "
              f"> threshold {threshold:.0f}. "
              f"Rerun with --trim-gutters 3 to remove canvas margins.")
        return True
    return False


# ── Trim existing extracted panels (in-place) ─────────────────────────────────

def trim_kit_panels(kit_dir: Path, trim_pct: float,
                    systems: list[str] | None = None) -> None:
    """
    Post-hoc gutter trimming for already-extracted panels.
    Walks kit_dir/panel_XX/ and trims every *.png found there.
    Use when you need to fix extracted panels without re-running the full pipeline.

    Called via: py scripts/panel_extractor.py --fix-kit brand/generated-bg/geo-blue-grid --trim-gutters 3
    """
    if systems is None:
        systems = []

    panel_dirs = sorted(kit_dir.glob("panel_*"))
    if not panel_dirs:
        print(f"[FIX-KIT] No panel_XX/ folders found in {kit_dir}")
        return

    print(f"[FIX-KIT] Trimming {len(panel_dirs)} panels in {kit_dir.name} at {trim_pct}%...")
    total_fixed = 0

    for pd in panel_dirs:
        for png in sorted(pd.glob("*.png")):
            if png.name == "original.png" or png.stem in (systems or []) or not systems:
                img = Image.open(png).convert("RGBA")
                trimmed = trim_panel_gutters(img, trim_pct).convert("RGB")
                trimmed.save(str(png), "PNG")
                total_fixed += 1
                print(f"  {pd.name}/{png.name}")

    print(f"[FIX-KIT] Done — {total_fixed} files updated.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract panels from a grid image and generate carousel backgrounds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  py scripts/panel_extractor.py --file grid.png --preview
  py scripts/panel_extractor.py --file grid.png --name "Deep Space"
  py scripts/panel_extractor.py --file grid.png --grid 2,3 --name "Nebula" --treatments none,glow
  py scripts/panel_extractor.py --file grid.png --panels 8 --compare
  py scripts/panel_extractor.py --file "8 panels.png" --name "Nebula"  # auto-detects 8
        """,
    )
    parser.add_argument("--file",       required=False, default=None, help="Grid image filename or path. Not required when using --fix-kit.")
    parser.add_argument("--panels",     type=int, default=None,   help="Panel count override (default: read from filename, then visual detection). "
                                                                  "ALWAYS extracts the full count — never capped to slide count.")
    parser.add_argument("--grid",       type=str,                 help="Override grid layout as 'rows,cols'")
    parser.add_argument("--name",       type=str,                 help="Background name (used as output folder slug)")
    parser.add_argument("--output",     type=str,                 help="Base output directory (default: brand/generated-bg)")
    parser.add_argument("--systems",    type=str, default="s01,s04,s17,s29",
                                                                  help="Design systems, comma-separated")
    parser.add_argument("--treatments", type=str, default="none",
                                                                  help="Treatments: none,glow,deep,soft,warm")
    parser.add_argument("--no-variants",action="store_true",      help="Only extract originals, skip color adaptation")
    parser.add_argument("--preview",    action="store_true",      help="Save a labeled preview image, then exit")
    parser.add_argument("--compare",    action="store_true",      help="Generate kit comparison grid after extraction")
    parser.add_argument("--manifest",   type=str,                 help="Custom manifest.json path")
    parser.add_argument("--trim-gutters", dest="trim_gutters", type=float, default=0.0, metavar="PCT",
                                                                  help="Crop PCT%% from each panel edge after extraction "
                                                                  "to remove ChatGPT canvas margins and white gutters. "
                                                                  "Recommended: 2 for thin lines, 3-4 for full canvas borders. "
                                                                  "Panel is resized back to 1080x1080 after trimming.")
    parser.add_argument("--fix-kit",  type=str, default=None,  metavar="KIT_DIR",
                                                                  help="Post-hoc trim mode: trim all panels in an already-extracted "
                                                                  "kit folder. Requires --trim-gutters. "
                                                                  "Example: --fix-kit brand/generated-bg/geo-blue-grid --trim-gutters 3")
    args = parser.parse_args()

    # ── --fix-kit mode: post-hoc trim of an already-extracted kit ─────────────
    if args.fix_kit:
        if args.trim_gutters <= 0:
            print("[FAIL] --fix-kit requires --trim-gutters PCT (e.g. --trim-gutters 3)")
            sys.exit(1)
        kit_path = Path(args.fix_kit)
        if not kit_path.is_absolute():
            kit_path = ROOT / args.fix_kit
        if not kit_path.exists():
            print(f"[FAIL] Kit directory not found: {kit_path}")
            sys.exit(1)
        trim_kit_panels(kit_path, args.trim_gutters)
        return

    # ── Resolve input file ────────────────────────────────────────────────────
    if not args.file:
        print("[FAIL] --file is required unless using --fix-kit")
        sys.exit(1)

    candidates = [
        PANELS_DIR / args.file,
        AI_BG_DIR / args.file,
        Path(args.file),
        ROOT / args.file,
    ]
    file_path: Path | None = next((p for p in candidates if p.exists()), None)
    if file_path is None:
        print(f"[FAIL] File not found: {args.file}")
        print(f"       Searched: {', '.join(str(c) for c in candidates[:3])}")
        sys.exit(1)

    # ── Load image ────────────────────────────────────────────────────────────
    img = Image.open(file_path).convert("RGBA")
    W, H = img.size
    print(f"[IN]   {file_path.name}  ({W} x {H} px)")

    # ── Determine panel count ─────────────────────────────────────────────────
    # Priority: --panels > filename > visual seam detection.
    # We ALWAYS extract the full count declared by the source — never under-extract.
    explicit_panels = args.panels  # may be None

    filename_panels = detect_panels_from_filename(file_path.name)
    if filename_panels:
        print(f"[COUNT] Filename declares {filename_panels} panels")

    # Resolve authoritative count
    if explicit_panels is not None:
        n_panels = explicit_panels
        if filename_panels and filename_panels != explicit_panels:
            print(f"[WARN]  --panels {explicit_panels} overrides filename count ({filename_panels}). "
                  f"Make sure you really want fewer panels than the image contains.")
        print(f"[COUNT] Using --panels override: {n_panels}")
    elif filename_panels:
        n_panels = filename_panels
        print(f"[COUNT] Trusting filename: {n_panels} panels")
    else:
        # Last resort: visual seam detection
        print("[COUNT] No filename clue found — running visual seam detection...")
        auto_rows, auto_cols, auto_panels = detect_grid_auto(img)
        n_panels = auto_panels
        print(f"[COUNT] Visual detection: {auto_rows}x{auto_cols} = {auto_panels} panels")

    if n_panels is None or n_panels < 1:
        print("[FAIL] Could not detect panel count. Use --panels to specify.")
        sys.exit(1)

    # ── Grid layout ───────────────────────────────────────────────────────────
    if args.grid:
        rows, cols = (int(x) for x in args.grid.split(","))
        h_seams: list[int] = []
        v_seams: list[int] = []
    else:
        # Use seam-aware detection for pixel-perfect cropping.
        # find_seams_given_sections already falls back to math division when
        # no visual seams are found, so this always produces n_panels cuts.
        rows, cols, h_seams, v_seams = detect_grid_from_seams(img, n_panels)

    # Safety: rows*cols must be >= n_panels — never silently shrink the count.
    actual_capacity = rows * cols
    if actual_capacity < n_panels:
        print(f"[WARN]  Grid layout {rows}x{cols} only fits {actual_capacity} panels "
              f"but source declares {n_panels}. Recomputing layout...")
        # Force math fallback: equal division, no seam detection
        rows, cols = detect_grid_layout(W, H, n_panels)
        h_seams = [int(H * i / rows) for i in range(1, rows)]
        v_seams = [int(W * i / cols) for i in range(1, cols)]
        print(f"[GRID]  Forced layout: {rows}x{cols}")

    print(f"[GRID] {rows} rows x {cols} cols  ->  {rows * cols} panels (extracting all)")
    if h_seams:
        print(f"[SEAMS] Horizontal: {h_seams}")
    if v_seams:
        print(f"[SEAMS] Vertical:   {v_seams}")

    # ── Names + paths ─────────────────────────────────────────────────────────
    bg_name = args.name or file_path.stem.replace("-", " ").replace("_", " ").title()
    bg_id = slugify(bg_name)
    out_root = Path(args.output) if args.output else OUTPUT_DEFAULT
    output_dir = out_root / bg_id
    manifest_path = Path(args.manifest) if args.manifest else MANIFEST_PATH

    # ── Preview mode ─────────────────────────────────────────────────────────
    if args.preview:
        draw_preview(img, rows, cols, n_panels, h_seams, v_seams,
                     output_dir / f"{bg_id}_preview.png")
        return

    # ── Extract panels — always extract the full grid, never cap to slide count ──
    total_in_grid = rows * cols
    if h_seams or v_seams:
        panels = extract_panels_with_seams(img, h_seams, v_seams, total_in_grid)
        print(f"[EXTRACT] {len(panels)} panels (seam-aware cropping)")
    else:
        panels = extract_panels_fallback(img, rows, cols, total_in_grid)
        print(f"[EXTRACT] {len(panels)} panels (mathematical fallback)")

    # ── Sanity check — detect panels that contain internal seams (bad crops) ──
    _sanity_check_panels(panels, rows, cols)

    systems = [s.strip() for s in args.systems.split(",") if s.strip()]
    treatments = [t.strip() for t in args.treatments.split(",") if t.strip()]

    recipe_extracted: dict[str, list[str]] = {sid: [] for sid in systems}

    for panel_idx, panel in enumerate(panels):
        panel_num = f"panel_{panel_idx + 1:02d}"
        panel_dir = output_dir / panel_num
        panel_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n  panel_{panel_idx + 1:02d}/")

        # ── Gutter trimming ───────────────────────────────────────────────────
        # Must happen BEFORE resize so we're working at source resolution.
        # This removes white canvas margins, ChatGPT grid gutters, and outer borders.
        if args.trim_gutters > 0:
            panel = trim_panel_gutters(panel, args.trim_gutters)
            print(f"    [TRIM] Gutters trimmed {args.trim_gutters}% per edge")

        # ── Edge quality check ────────────────────────────────────────────────
        # Warn if bright outer borders remain after trimming (or if no trim was requested).
        check_bright_edges(panel, panel_idx)

        # Original — use ImageOps.fit (center-crop to square) instead of resize,
        # so non-square source panels don't get stretched to 1080x1080.
        from PIL import ImageOps as _ImageOps
        orig = _ImageOps.fit(panel.convert("RGB"), (1080, 1080), method=Image.LANCZOS, centering=(0.5, 0.5))
        orig.save(str(panel_dir / "original.png"), "PNG")

        orig_rel = str((panel_dir / "original.png").relative_to(ROOT)).replace("\\", "/")
        for sid in systems:
            recipe_extracted.setdefault(sid, [])

        if args.no_variants:
            for sid in systems:
                recipe_extracted[sid].append(orig_rel)
            print(f"    original.png  (no-variants)")
            continue

        panel_arr = np.array(orig)  # use the square-cropped original for color adaptation

        for sys_id in systems:
            cfg = DESIGN_SYSTEMS.get(sys_id)
            if not cfg:
                print(f"    [WARN] Unknown system: {sys_id} — skipping")
                continue

            adapted_arr = adapt_hue(panel_arr, cfg["accent"])
            adapted_img = Image.fromarray(adapted_arr).convert("RGB")  # already 1080x1080

            for treatment in treatments:
                treat_fn = TREATMENTS.get(treatment)
                if treat_fn is None:
                    print(f"    [WARN] Unknown treatment: {treatment} — skipping")
                    continue
                result = treat_fn(adapted_img.copy())

                fname = f"{sys_id}.png" if treatment == "none" else f"{sys_id}_{treatment}.png"
                out_path = panel_dir / fname
                result.save(str(out_path), "PNG")
                size_kb = out_path.stat().st_size // 1024

                if treatment == "none":
                    rel = str(out_path.relative_to(ROOT)).replace("\\", "/")
                    recipe_extracted[sys_id].append(rel)

                print(f"    {panel_num}/{fname}  ({size_kb} KB)")

    # ── Manifest update ───────────────────────────────────────────────────────
    manifest = load_manifest(manifest_path)
    entry_idx = next(
        (i for i, b in enumerate(manifest["backgrounds"]) if b["id"] == bg_id), None
    )
    source_str = f"panel extraction from {file_path.name}, {len(panels)} panels"

    if entry_idx is not None:
        existing = manifest["backgrounds"][entry_idx]
        existing.setdefault("recipe_variants", {})
        existing["recipe_variants"]["extracted"] = recipe_extracted
        existing["panels"] = len(panels)
        existing["source"] = source_str
        print(f"\n[MANIFEST] Updated entry '{bg_id}'")
    else:
        manifest["backgrounds"].append({
            "id": bg_id,
            "name": bg_name,
            "source": source_str,
            "panels": len(panels),
            "recipe_variants": {"extracted": recipe_extracted},
        })
        print(f"\n[MANIFEST] Added new entry '{bg_id}'")

    save_manifest(manifest, manifest_path)
    print(f"[MANIFEST] Saved -> {manifest_path}")

    # ── Kit comparison ────────────────────────────────────────────────────────
    if args.compare:
        build_kit_comparison(output_dir, bg_id, systems, len(panels))

    # ── Summary ───────────────────────────────────────────────────────────────
    n_sys = len(systems)
    n_trts = len(treatments)
    total = len(panels) * n_sys * n_trts
    print(f"\n[DONE] {len(panels)} panels x {n_sys} systems x {n_trts} treatments = {total} images")
    print(f"[OUT]  {output_dir}")
    print()
    print("Next step: use in a carousel spec with:")
    print(f'  "layers": ["{bg_id}"],')
    print(f'  "bg_recipe": "extracted"')
    print(f'  (set in meta, same as any other bg_recipe)')


if __name__ == "__main__":
    main()
