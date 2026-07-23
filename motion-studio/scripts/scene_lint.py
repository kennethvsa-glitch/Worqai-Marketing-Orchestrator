"""
scene_lint.py — Determinism-lock + scene-contract gate for hand-authored film scenes.

The film pipeline (scene-launch-*.html) has no JSON spec, so motion_preflight.py
never validates it. This script greps a scene HTML (and its linked CSS) and FAILs the
build when a determinism lock is violated or the structural scene contract is broken —
moving rules out of "the agent must remember" (markdown) into an enforced gate.

Usage:
    py scripts/scene_lint.py templates/scenes/scene-launch-villain-v3.html
    py scripts/scene_lint.py templates/scenes/scene-launch-villain-v3.html --strict   # WARN -> FAIL

Exit codes:
    0 = passed (no FAILs; WARNs allowed unless --strict)
    1 = FAILs present (or WARNs present under --strict)

Checks map to .claude/rules/motion-determinism.md:
  Lock 1  — gsap.ticker.lagSmoothing(0) present                         [FAIL]
  Lock 2  — gsap.globalTimeline.pause() present (paused at load)        [WARN]
  Lock 3  — CSS transition on animatable props (class+transition smell) [WARN]
  Lock 4/10 — setInterval / requestAnimationFrame for animation         [FAIL]
  Lock 8  — @keyframes without animation-play-state: paused             [WARN]
  Lock 10 — Lottie autoplay:true                                        [FAIL]
  Lock 10 — performance.now()/Date.now() as animation clock             [WARN]
  No-CDN  — <script src="http..."> in scene                             [FAIL]
Scene contract:
  data-duration / data-fps / data-name on <html>                        [WARN]
  window.MOTION_LABELS emitted (film timing)                            [WARN]
  signalReady(...) called (exporter readiness)                          [WARN]
  canvas references 1080 and 1920 (9:16)                                [WARN]
"""

import argparse
import re
import sys
from pathlib import Path

FAILS: list[str] = []
WARNS: list[str] = []


def fail(msg: str) -> None:
    FAILS.append(msg)


def warn(msg: str) -> None:
    WARNS.append(msg)


def load_scene(html_path: Path) -> tuple[str, str]:
    """Return (html_text, combined_css). Inlines linked <link rel=stylesheet> files."""
    html = html_path.read_text(encoding="utf-8")
    css_parts: list[str] = []
    # embedded <style> blocks
    css_parts += re.findall(r"<style[^>]*>([\s\S]*?)</style>", html, re.IGNORECASE)
    # linked stylesheets (resolve relative to the HTML file)
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        if href.startswith("http"):
            continue
        css_file = (html_path.parent / href).resolve()
        if css_file.exists():
            css_parts.append(css_file.read_text(encoding="utf-8"))
    return html, "\n".join(css_parts)


def strip_comments_js(html: str) -> str:
    """Remove HTML comments so commented-out code doesn't trip greps."""
    return re.sub(r"<!--[\s\S]*?-->", "", html)


# ── Determinism locks ──────────────────────────────────────────────────────────

def check_locks(html: str, css: str) -> None:
    body = strip_comments_js(html)

    # Lock 1 — lagSmoothing(0) mandatory
    if re.search(r"gsap\.ticker\.lagSmoothing\s*\(\s*0\s*\)", body):
        pass
    else:
        fail("Lock 1: gsap.ticker.lagSmoothing(0) not found — frame-stepper is silently non-deterministic without it")

    # Lock 2 — timeline paused once at load
    if not re.search(r"gsap\.globalTimeline\.pause\s*\(", body):
        warn("Lock 2: gsap.globalTimeline.pause() not found — confirm the timeline is paused once at load")

    # Lock 4 / 10 — no off-timeline clocks
    if re.search(r"\bsetInterval\s*\(", body):
        fail("Lock 4: setInterval() found — counters/animation must live on the GSAP timeline (proxy tween), not setInterval")
    if re.search(r"\brequestAnimationFrame\s*\(", body):
        fail("Lock 10: requestAnimationFrame() found — no library/own-clock loops; drive every effect from the GSAP timeline")

    # Lock 10 — Lottie autoplay must be false
    if re.search(r"lottie\.loadAnimation\s*\([^)]*autoplay\s*:\s*true", body, re.DOTALL):
        fail("Lock 10: Lottie autoplay:true — must be autoplay:false and driven via goToAndStop from a proxy tween")

    # Lock 10 — wall-clock sources for animation
    if re.search(r"performance\.now\s*\(", body) or re.search(r"\bDate\.now\s*\(", body):
        warn("Lock 10: performance.now()/Date.now() present — must not feed any animated value (use the GSAP proxy)")

    # No-CDN — scene scripts must load from vendor/
    cdn = re.findall(r'<script[^>]+src=["\']https?://[^"\']+["\']', body, re.IGNORECASE)
    if cdn:
        fail(f"No-CDN: {len(cdn)} CDN <script src> reference(s) — vendor/ only (CDN drift breaks reproducibility)")

    # Lock 3 — CSS transition on animatable props (class+transition anti-pattern smell)
    trans = []
    for m in re.finditer(r"transition\s*:\s*([^;}\n]+)", css, re.IGNORECASE):
        decl = m.group(1).lower()
        if any(p in decl for p in ("transform", "opacity", "clip-path", "filter", "all")):
            trans.append(decl.strip()[:60])
    if trans:
        warn(f"Lock 3: CSS transition on animatable prop(s) ({len(trans)}x, e.g. '{trans[0]}') — GSAP must own animated props, not CSS transitions")

    # Lock 8 — @keyframes must be frozen in video mode
    if "@keyframes" in css and "animation-play-state: paused" not in css.replace(" ", "") and "animation-play-state:paused" not in css.replace(" ", ""):
        warn("Lock 8: @keyframes present but no 'animation-play-state: paused' — animated geo layers must freeze at a settled pose")


# ── Scene contract ──────────────────────────────────────────────────────────────

def check_contract(html: str) -> None:
    head = html[:600]
    for attr in ("data-duration", "data-fps", "data-name"):
        if attr not in head:
            warn(f"Contract: <html> missing {attr} — film exporter/labels rely on it")

    # signalReady() sets motionReady AND exports window.MOTION_LABELS (see motion-lib.js),
    # so calling it satisfies both the readiness and the labels contract.
    has_signal = "signalReady" in html
    if not has_signal:
        warn("Contract: signalReady(...) not called — exporter waits on readiness signal before frame loop")
    if not (has_signal or "MOTION_LABELS" in html):
        warn("Contract: no MOTION_LABELS emitted (call signalReady(tl)) — SFX/VO/captions/cutdowns resolve off labels")

    if not ("1080" in html and "1920" in html):
        warn("Contract: canvas does not reference 1080 and 1920 — confirm 9:16 (1080x1920) dimensions")


def main() -> None:
    ap = argparse.ArgumentParser(description="Determinism + contract gate for film scenes")
    ap.add_argument("scene", help="Path to scene HTML")
    ap.add_argument("--strict", action="store_true", help="Treat WARN as FAIL")
    args = ap.parse_args()

    path = Path(args.scene)
    if not path.exists():
        print(f"ERROR: scene not found: {path}")
        sys.exit(1)

    html, css = load_scene(path)
    print(f"\nScene lint: {path.name}")

    check_locks(html, css)
    check_contract(html)

    for m in FAILS:
        print(f"  [FAIL]  {m}")
    for m in WARNS:
        print(f"  [WARN]  {m}")
    if not FAILS and not WARNS:
        print("  [ok]    all determinism locks and contract checks passed")

    print()
    blocked = bool(FAILS) or (args.strict and bool(WARNS))
    if blocked:
        n = len(FAILS) + (len(WARNS) if args.strict else 0)
        print(f"Scene lint FAILED — {n} blocking issue(s). Fix before render.")
    else:
        suffix = f" ({len(WARNS)} warning(s))" if WARNS else ""
        print(f"Scene lint PASSED{suffix}.")

    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()
