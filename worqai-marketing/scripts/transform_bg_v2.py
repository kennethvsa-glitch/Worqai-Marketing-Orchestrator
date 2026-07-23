#!/usr/bin/env python3
"""
transform_bg_v2.py — Background Transformation Engine v2.0

Generates per-slide image progressions from a single adapted system variant.
Each recipe creates a visual arc across N slides — slide 1 is the base state,
slide N is the fully-transformed end state.

8 Recipes (numpy + Pillow only — no cv2, no scipy required):
    glow_bloom     Bubbles get bioluminescent. Energy builds toward CTA.
    deep_zoom      Starts dreamy-blur, ends razor-sharp. Cinematic arc.
    breathe_life   Organic inhale/exhale scale pulse. Scene feels alive.
    phase_distort  Multi-sine coordinate warp. Glass/water refraction.
    seamless_drift Seamless tile drift along a curved path.
    liquid_ripple  Radial sine displacement from center. Water/liquid themes.
    curl_flow      Approximated curl noise. Bubbles swirl in gentle currents.
    fluid_warp     Brightness-gradient velocity field. Dynamic, techy feel.

Usage:
    # Single recipe from a PNG file
    py scripts/transform_bg_v2.py brand/generated-bg/ai-bubbles-01/s17.png \\
        --recipe glow_bloom --slides 4 \\
        --output brand/generated-bg/ai-bubbles-01/recipes/glow_bloom/s17/

    # All systems for a background (called from adapt_image_bg.py)
    py scripts/transform_bg_v2.py \\
        --bg-id ai-bubbles-01 --recipe glow_bloom --slides 4 --all-systems

    # List all available recipes
    py scripts/transform_bg_v2.py --list

Requirements:
    pip install numpy Pillow
"""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Run: pip install numpy", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image, ImageFilter
except ImportError:
    print("ERROR: Pillow required. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent.parent
MANIFEST_PATH = ROOT / "brand" / "generated-bg" / "manifest.json"
GENERATED_DIR = ROOT / "brand" / "generated-bg"

# ── Vectorized HSV helpers ──────────────────────────────────────────────────────

def _rgb_to_hsv_np(rgb_float: np.ndarray):
    """Convert float RGB array (H,W,3) → H, S, V each (H,W). Input range 0-1."""
    r, g, b = rgb_float[..., 0], rgb_float[..., 1], rgb_float[..., 2]
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    delta = maxc - minc

    v = maxc
    with np.errstate(invalid="ignore", divide="ignore"):
        s = np.where(maxc > 1e-5, delta / maxc, 0.0)

    h = np.zeros_like(r)
    md = delta > 1e-5  # mask where hue is defined
    mr = md & (maxc == r)
    mg = md & (maxc == g) & ~mr
    mb = md & ~mr & ~mg

    h[mr] = ((g[mr] - b[mr]) / delta[mr]) % 6.0
    h[mg] = (b[mg] - r[mg]) / delta[mg] + 2.0
    h[mb] = (r[mb] - g[mb]) / delta[mb] + 4.0
    h /= 6.0  # normalize to 0-1

    return h, s, v


def _hsv_to_rgb_np(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Convert HSV (H,W) arrays → float RGB (H,W,3). Output range 0-1."""
    i = (h * 6.0).astype(int) % 6
    f = h * 6.0 - (h * 6.0).astype(int)
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    r = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [v, q, p, p, t, v])
    g = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [t, v, v, q, p, p])
    b = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [p, p, t, v, v, q])

    return np.stack([r, g, b], axis=-1)


# ── Coordinate warp helper ──────────────────────────────────────────────────────

def _warp_coords(arr: np.ndarray, dx: np.ndarray, dy: np.ndarray) -> np.ndarray:
    """Inverse nearest-neighbor warp. Displacement in pixels (float arrays).
    For each output pixel, samples from source offset by (-dx, -dy)."""
    H, W = arr.shape[:2]
    ys, xs = np.mgrid[0:H, 0:W]
    src_x = np.clip(xs + dx, 0, W - 1).astype(np.int32)
    src_y = np.clip(ys + dy, 0, H - 1).astype(np.int32)
    return arr[src_y, src_x]


# ── Recipe implementations ──────────────────────────────────────────────────────

def recipe_glow_bloom(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Brightness extraction + additive saturation boost.
    Slide 1 = base. Slide N = up to +40% brightness, +30% saturation.
    Bubbles get bioluminescent; energy builds toward CTA."""
    if t < 0.01:
        return arr.copy()

    has_alpha = arr.shape[2] == 4
    rgb = arr[..., :3].astype(float) / 255.0
    alpha = arr[..., 3:4] if has_alpha else None

    h, s, v = _rgb_to_hsv_np(rgb)

    # Dark pixel mask — don't bloom near-black backgrounds
    dark_mask = v < 0.04

    new_v = np.where(dark_mask, v, np.clip(v * (1.0 + t * 0.40), 0, 1))
    new_s = np.where(dark_mask, s, np.clip(s * (1.0 + t * 0.30), 0, 1))

    rgb_out = _hsv_to_rgb_np(h, new_s, new_v)
    rgb_u8 = np.clip(rgb_out * 255, 0, 255).astype(np.uint8)

    if has_alpha:
        return np.concatenate([rgb_u8, alpha], axis=-1)
    return rgb_u8


def recipe_deep_zoom(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Frequency layer blending — Gaussian blur decreasing per slide.
    Slide 1 = dreamy soft focus. Slide N = razor-sharp. Cinematic arc."""
    max_blur = 8.0
    blur_radius = max_blur * (1.0 - t)
    if blur_radius < 0.3:
        return arr.copy()

    # Blur the PIL image (handles both RGBA and RGB)
    blurred = pil_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return np.array(blurred)


def recipe_breathe_life(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Sine-wave scale modulation. Scene inhales and exhales organically.
    Pattern: 1.0 (base) → 1.04 (inhale) → 0.96 (exhale) → 1.0 (return)."""
    H, W = arr.shape[:2]
    # Full sine cycle — organic breath
    scale = 1.0 + math.sin(t * math.pi * 2) * 0.04
    if abs(scale - 1.0) < 0.002:
        return arr.copy()

    new_W = max(1, int(W * scale))
    new_H = max(1, int(H * scale))

    resized = pil_img.resize((new_W, new_H), Image.LANCZOS)
    mode = pil_img.mode
    result = Image.new(mode, (W, H), (0, 0, 0, 0) if mode == "RGBA" else (0, 0, 0))
    paste_x = (W - new_W) // 2
    paste_y = (H - new_H) // 2
    result.paste(resized, (paste_x, paste_y))
    return np.array(result)


def recipe_phase_distort(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Multi-sine XY coordinate warp. Amplitude builds per slide.
    Glass/water refraction effect — luxury, abstract feel."""
    amplitude = t * 12.0  # 0 → 12 pixels
    if amplitude < 0.3:
        return arr.copy()

    H, W = arr.shape[:2]
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    freq_x = 2 * math.pi / W * 3
    freq_y = 2 * math.pi / H * 2
    phase = t * math.pi

    dx = amplitude * (
        np.sin(ys * freq_y + phase) * np.cos(xs * freq_x * 0.5)
        + 0.4 * np.cos(ys * freq_y * 1.3 + phase * 0.7)
    )
    dy = amplitude * (
        np.cos(xs * freq_x + phase * 0.7) * np.sin(ys * freq_y * 0.8)
        + 0.4 * np.sin(xs * freq_x * 1.7 + phase)
    )
    return _warp_coords(arr, dx, dy)


def recipe_seamless_drift(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Seamless tile offset along a curved path.
    Image drifts 0 → 80px horizontally + sine arc vertically. Infinite scroll feel."""
    if t < 0.01:
        return arr.copy()

    # Horizontal drift + gentle vertical arc
    offset_x = int(round(t * 80))
    offset_y = int(round(math.sin(t * math.pi) * 24))

    out = np.roll(arr, offset_y, axis=0)  # vertical (seamless — wraps)
    out = np.roll(out, offset_x, axis=1)  # horizontal (seamless — wraps)
    return out


def recipe_liquid_ripple(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Multi-frequency radial waves propagating from center.
    Amplitude builds 0 → 18px per slide. Water / liquid themes."""
    amplitude = t * 18.0
    if amplitude < 0.3:
        return arr.copy()

    H, W = arr.shape[:2]
    cy, cx = H / 2.0, W / 2.0
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)

    # Two overlapping frequencies for organic, non-uniform ripple
    phase = dist / (W / 8.0) * 2 * math.pi - t * math.pi
    ripple = (
        amplitude * 0.65 * np.sin(phase)
        + amplitude * 0.35 * np.sin(phase * 2.1 + 0.8)
    )

    # Radial direction unit vectors
    safe_dist = np.where(dist > 0.5, dist, 1.0)
    norm_x = (xs - cx) / safe_dist
    norm_y = (ys - cy) / safe_dist

    return _warp_coords(arr, ripple * norm_x, ripple * norm_y)


def recipe_curl_flow(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Approximated curl noise via rotational sine displacement.
    Divergence-free field — bubbles swirl in gentle, artifact-free currents."""
    amplitude = t * 10.0
    if amplitude < 0.3:
        return arr.copy()

    H, W = arr.shape[:2]
    ys, xs = np.mgrid[0:H, 0:W].astype(float)

    # Curl field: (-∂F/∂y, ∂F/∂x) for F = sin(x/sx)*sin(y/sy)
    sx, sy = W / 4.0, H / 4.0
    # Multi-octave for richness
    F1_dx = (math.pi / sx) * np.cos(xs / sx) * np.sin(ys / sy)
    F1_dy = (math.pi / sy) * np.sin(xs / sx) * np.cos(ys / sy)
    F2_dx = (math.pi / (sx * 0.6)) * np.cos(xs / (sx * 0.6)) * np.sin(ys / (sy * 0.6))
    F2_dy = (math.pi / (sy * 0.6)) * np.sin(xs / (sx * 0.6)) * np.cos(ys / (sy * 0.6))

    dx = amplitude * (-F1_dy * 0.7 - F2_dy * 0.3)
    dy = amplitude * (F1_dx * 0.7 + F2_dx * 0.3)
    return _warp_coords(arr, dx, dy)


def recipe_fluid_warp(pil_img: Image.Image, arr: np.ndarray, t: float) -> np.ndarray:
    """Brightness-gradient velocity field. High-contrast edges create micro-eddies.
    Dynamic, techy feel — edges drive the motion."""
    amplitude = t * 10.0
    if amplitude < 0.3:
        return arr.copy()

    H, W = arr.shape[:2]
    # Luma brightness map
    rgb = arr[..., :3].astype(float)
    gray = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255.0

    # Finite-difference gradient (simple Sobel-like)
    dg_dx = np.roll(gray, -1, axis=1) - np.roll(gray, 1, axis=1)  # dI/dx
    dg_dy = np.roll(gray, -1, axis=0) - np.roll(gray, 1, axis=0)  # dI/dy

    # Perpendicular-to-gradient flow (rotated 90°) — advects along iso-brightness lines
    dx = amplitude * (-dg_dy)
    dy = amplitude * dg_dx
    return _warp_coords(arr, dx, dy)


# ── Recipe registry ─────────────────────────────────────────────────────────────

RECIPES = {
    "glow_bloom":    (recipe_glow_bloom,   "Bubbles glow brighter each slide. Energy builds toward CTA."),
    "deep_zoom":     (recipe_deep_zoom,    "Starts dreamy-blur, ends razor-sharp. Cinematic arc."),
    "breathe_life":  (recipe_breathe_life, "Organic inhale/exhale pulse. The scene feels alive."),
    "phase_distort": (recipe_phase_distort,"Multi-sine coordinate warp. Glass/water refraction."),
    "seamless_drift":(recipe_seamless_drift,"Seamless tile drift. Infinite curved scroll."),
    "liquid_ripple": (recipe_liquid_ripple, "Radial waves propagate from center. Water themes."),
    "curl_flow":     (recipe_curl_flow,    "Gentle divergence-free swirl currents."),
    "fluid_warp":    (recipe_fluid_warp,   "Brightness-gradient velocity field. Techy, dynamic."),
}


# ── Core API ────────────────────────────────────────────────────────────────────

def generate_slides(
    input_png: Path,
    recipe: str,
    n_slides: int,
    output_dir: Path,
    size: int = 1080,
) -> list[str]:
    """Transform a single PNG into N slide variants using the given recipe.

    Args:
        input_png:  Source 1080×1080 PNG (system-adapted color variant).
        recipe:     One of the 8 recipe names.
        n_slides:   Number of output slides (1 = base, N = fully transformed).
        output_dir: Where to write slide_01.png … slide_N.png.
        size:       Output resolution (default 1080px square).

    Returns:
        List of relative output paths (str) for manifest storage.
    """
    if recipe not in RECIPES:
        raise ValueError(f"Unknown recipe '{recipe}'. Available: {', '.join(RECIPES)}")

    fn, _ = RECIPES[recipe]
    output_dir.mkdir(parents=True, exist_ok=True)

    pil = Image.open(input_png).convert("RGBA")
    if pil.size != (size, size):
        pil = pil.resize((size, size), Image.LANCZOS)
    arr = np.array(pil)

    paths: list[str] = []
    for i in range(n_slides):
        t = i / max(n_slides - 1, 1)  # 0.0 at slide 1, 1.0 at slide N
        result_arr = fn(pil, arr, t)
        result_img = Image.fromarray(result_arr)
        if result_img.mode == "RGBA":
            result_img = result_img.convert("RGB")

        out_path = output_dir / f"slide_{i + 1:02d}.png"
        result_img.save(out_path, "PNG", optimize=True)
        size_kb = out_path.stat().st_size // 1024
        print(f"      slide_{i + 1:02d}.png  t={t:.2f}  {size_kb} KB")
        paths.append(str(out_path.relative_to(ROOT)).replace("\\", "/"))

    return paths


def generate_all_systems(
    bg_id: str,
    recipe: str,
    n_slides: int,
    size: int = 1080,
) -> dict[str, list[str]]:
    """Run a recipe across all 4 system variants for a given background.

    Returns:
        Dict[system_id → list of relative slide paths]
    """
    bg_dir = GENERATED_DIR / bg_id
    systems = ["s01", "s04", "s17", "s29"]
    result: dict[str, list[str]] = {}

    for sys_id in systems:
        variant_png = bg_dir / f"{sys_id}.png"
        if not variant_png.exists():
            print(f"  SKIP {sys_id} — variant not found: {variant_png}", file=sys.stderr)
            continue

        out_dir = bg_dir / "recipes" / recipe / sys_id
        print(f"  [{sys_id}] {recipe} -> {out_dir.relative_to(ROOT)}")
        paths = generate_slides(variant_png, recipe, n_slides, out_dir, size)
        result[sys_id] = paths

    return result


def update_manifest_recipes(bg_id: str, recipe: str, system_slides: dict[str, list[str]]):
    """Merge recipe_variants into the manifest entry for bg_id."""
    manifest: dict = {"backgrounds": []}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    entries = manifest.get("backgrounds", [])
    idx = next((i for i, b in enumerate(entries) if b["id"] == bg_id), None)
    if idx is None:
        print(f"  WARN: background '{bg_id}' not found in manifest — recipe_variants not saved.", file=sys.stderr)
        return

    entry = entries[idx]
    recipe_variants: dict = entry.get("recipe_variants", {})
    recipe_variants[recipe] = system_slides
    entry["recipe_variants"] = recipe_variants
    entries[idx] = entry
    manifest["backgrounds"] = entries

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"  [MANIFEST] '{bg_id}'.recipe_variants.{recipe} updated.")


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Background Transformation Engine v2 — 8 cinematic slide recipes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input_png",
        nargs="?",
        help="Source PNG to transform (single-system mode)",
    )
    parser.add_argument(
        "--recipe",
        type=str,
        required=False,
        help=f"Recipe name. Available: {', '.join(RECIPES)}",
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=5,
        help="Number of slide variants to generate (default: 5)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=1080,
        help="Output resolution in px (default: 1080)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory (single-system mode)",
    )
    parser.add_argument(
        "--bg-id",
        type=str,
        help="Background ID from manifest (all-systems mode, e.g. 'ai-bubbles-01')",
    )
    parser.add_argument(
        "--all-systems",
        action="store_true",
        help="Generate for all 4 systems (s01/s04/s17/s29) of --bg-id",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available recipes and exit",
    )

    args = parser.parse_args()

    if args.list:
        print("\n8 Available Recipes\n" + "-" * 40)
        for name, (_, desc) in RECIPES.items():
            print(f"  {name:<18} {desc}")
        print()
        return

    if not args.recipe:
        parser.error("--recipe is required (unless using --list)")

    if args.recipe not in RECIPES:
        parser.error(f"Unknown recipe '{args.recipe}'. Use --list to see options.")

    if args.all_systems:
        # All-systems mode: generate for all variants of a background
        if not args.bg_id:
            parser.error("--all-systems requires --bg-id")
        print(f"\n-> Recipe '{args.recipe}' x all systems for '{args.bg_id}'")
        system_slides = generate_all_systems(args.bg_id, args.recipe, args.slides, args.size)
        update_manifest_recipes(args.bg_id, args.recipe, system_slides)
        print(f"\n[DONE] {sum(len(v) for v in system_slides.values())} slides generated.")

    elif args.input_png:
        # Single-PNG mode
        input_png = Path(args.input_png)
        if not input_png.is_absolute():
            input_png = ROOT / input_png
        if not input_png.exists():
            print(f"[FAIL] File not found: {input_png}", file=sys.stderr)
            sys.exit(1)

        output_dir = Path(args.output) if args.output else input_png.parent / "recipe_out" / args.recipe
        if not output_dir.is_absolute():
            output_dir = ROOT / output_dir

        print(f"\n-> Recipe '{args.recipe}' on {input_png.name} ({args.slides} slides)")
        paths = generate_slides(input_png, args.recipe, args.slides, output_dir, args.size)
        print(f"\n[DONE] {len(paths)} slides in {output_dir}")

    else:
        parser.error("Provide either an input PNG or --bg-id + --all-systems")


if __name__ == "__main__":
    main()
