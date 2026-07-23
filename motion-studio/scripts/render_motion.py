"""
render_motion.py — spec JSON + motion tokens -> animated HTML

Usage (single scene):
    py scripts/render_motion.py motion/specs/my-spec.json
    py scripts/render_motion.py motion/specs/my-spec.json --output templates/scenes/output.html

Usage (multi-scene spec):
    py scripts/render_motion.py motion/specs/multi-spec.json
    Outputs: templates/scenes/output_scene-0.html, output_scene-1.html, ...

Multi-scene spec format:
    {
      "meta": { "system": "s01", "fps": 30, "video_mode": true },
      "scenes": [
        { "scene": "stat-reveal", "duration": 8, "seed": "...", "copy": { ... } },
        { "scene": "text-poster", "duration": 6, "seed": "...", "copy": { ... } }
      ]
    }
"""

import json
import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_spec(spec_path: Path) -> dict:
    with open(spec_path, encoding="utf-8") as f:
        return json.load(f)


def load_tokens(system: str) -> dict:
    tokens_path = ROOT / "motion" / "tokens" / "motion-tokens.json"
    with open(tokens_path, encoding="utf-8") as f:
        data = json.load(f)
    if system not in data:
        raise SystemExit(f"FAIL: Unknown system '{system}'. Available: {list(data.keys())}")
    return data[system]


def load_scene_template(scene: str) -> str:
    path = ROOT / "templates" / "scenes" / f"scene-{scene}.html"
    if not path.exists():
        raise SystemExit(f"FAIL: Scene template not found: {path}")
    return path.read_text(encoding="utf-8")


def inject_copy(html: str, copy: dict) -> str:
    def replacer(match):
        key = match.group(1).strip()
        parts = key.split(".")
        if parts[0] == "copy" and len(parts) == 2:
            field = parts[1]
            if field not in copy:
                raise SystemExit(f"FAIL: '{{{{ copy.{field} }}}}' in template but not in spec. Have: {list(copy.keys())}")
            return str(copy[field])
        raise SystemExit(f"FAIL: Unknown template variable: {{{{{key}}}}}")
    return re.sub(r'\{\{\s*([\w.]+)\s*\}\}', replacer, html)


def inject_seed(html: str, seed: str) -> str:
    if 'window.MOTION_SEED = "default"' not in html:
        print("WARN: MOTION_SEED placeholder not found in template")
        return html
    return html.replace('window.MOTION_SEED = "default"', f'window.MOTION_SEED = "{seed}"')


def inject_video_mode_css(html: str) -> str:
    freeze_css = (
        "\n    /* VIDEO MODE — geo layer freeze (Lock 8) */"
        "\n    .geo-layer-animated { animation-play-state: paused; animation-delay: -3s; }"
    )
    if "</style>" not in html:
        return html
    return html.replace("</style>", freeze_css + "\n  </style>", 1)


def inject_fps(html: str, fps: int) -> str:
    """Stamp data-fps onto the <html> tag so the exporter can read it."""
    if f'data-fps=' in html:
        return re.sub(r'data-fps=["\'][\d]+["\']', f'data-fps="{fps}"', html)
    return html.replace("<html", f'<html data-fps="{fps}"', 1)


def inject_linked_css(html: str) -> str:
    """Inline <link rel="stylesheet" href="scene-X.css"> for self-contained output."""
    scenes_dir = ROOT / "templates" / "scenes"

    def replacer(m):
        href = m.group(1)
        css_path = scenes_dir / href
        if css_path.exists():
            css = css_path.read_text(encoding="utf-8")
            return f'<style>\n{css}\n</style>'
        print(f"WARN: linked CSS not found: {css_path}")
        return m.group(0)

    return re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+\.css)">', replacer, html)


def inject_lib(html: str) -> str:
    """Inline <script src="../motion-lib.js"> for self-contained output."""
    marker = '<script src="../motion-lib.js"></script>'
    if marker not in html:
        return html
    lib_path = ROOT / "templates" / "motion-lib.js"
    if not lib_path.exists():
        print("WARN: motion-lib.js not found — scene will load it as a relative URL")
        return html
    lib_js = lib_path.read_text(encoding="utf-8")
    return html.replace(marker, f'<script>\n{lib_js}\n</script>')


def render_one(scene: str, copy: dict, meta: dict) -> str:
    """Render a single scene and return the HTML string."""
    system = meta.get("system", "s01")
    seed   = meta.get("seed", "default")
    load_tokens(system)  # validate system exists
    html = load_scene_template(scene)
    html = inject_copy(html, copy)
    html = inject_seed(html, seed)
    html = inject_linked_css(html)         # inline CSS before video_mode may need </style>
    if meta.get("video_mode"):
        html = inject_video_mode_css(html)
    if meta.get("fps"):
        html = inject_fps(html, int(meta["fps"]))
    html = inject_lib(html)
    return html


def main():
    parser = argparse.ArgumentParser(description="Render a motion spec to animated HTML")
    parser.add_argument("spec", type=Path, help="Path to spec JSON")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output HTML path (single-scene) or output directory (multi-scene)")
    args = parser.parse_args()

    spec    = load_spec(args.spec)
    meta    = spec.get("meta", {})
    scenes  = spec.get("scenes")   # multi-scene key
    scene   = spec.get("scene")    # single-scene key

    # ── Multi-scene ───────────────────────────────────────────────────────────
    if scenes:
        out_dir = (args.output or ROOT / "templates" / "scenes").resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        out_paths = []
        for i, s in enumerate(scenes):
            scene_meta = {**meta, **{k: v for k, v in s.items() if k not in ("copy",)}}
            html = render_one(s["scene"], s.get("copy", {}), scene_meta)
            out_path = out_dir / f"output_scene-{i}.html"
            out_path.write_text(html, encoding="utf-8")
            out_paths.append(out_path)
            print(f"  [{i}] {s['scene']:20s}  {s.get('duration', '?')}s  -> {out_path.name}")
        print(f"Rendered {len(scenes)} scenes to {out_dir}")
        return

    # ── Single scene ──────────────────────────────────────────────────────────
    if not scene:
        raise SystemExit("FAIL: spec must have 'scene' (single) or 'scenes' (multi) key")

    html = render_one(scene, spec.get("copy", {}), meta)

    out_path = (args.output or ROOT / "templates" / "scenes" / "output.html").resolve()
    out_path.write_text(html, encoding="utf-8")

    try:
        display = out_path.relative_to(ROOT)
    except ValueError:
        display = out_path
    print(f"Rendered  {display}")
    print(f"  scene:      {scene}")
    print(f"  system:     {meta.get('system', 's01')}")
    print(f"  seed:       {meta.get('seed', 'default')}")
    print(f"  video_mode: {meta.get('video_mode', False)}")
    print(f"  duration:   {meta.get('duration', '?')}s  fps: {meta.get('fps', '?')}")


if __name__ == "__main__":
    main()
