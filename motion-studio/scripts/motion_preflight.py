"""
motion_preflight.py — validate a motion spec before rendering

Usage:
    py scripts/motion_preflight.py motion/specs/my-spec.json
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(Path(__file__).parent))
try:
    from orthography_check import scan_html_file as _ortho_scan
except ImportError:
    _ortho_scan = None

EFFECTS = {"fade", "slide", "textReveal", "counter", "scale", "reveal", "blur"}
COUNTER_SCENES = {"stat-reveal"}


def fail(msg: str) -> None:
    print(f"  [FAIL]  {msg}")


def warn(msg: str) -> None:
    print(f"  [WARN]  {msg}")


def ok(msg: str) -> None:
    print(f"  [ok]    {msg}")


def load_spec(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_template_copy_fields(scene: str) -> list[str]:
    """Return copy field names referenced as {{ copy.X }} in the scene template."""
    path = ROOT / "templates" / "scenes" / f"scene-{scene}.html"
    if not path.exists():
        return []
    html = path.read_text(encoding="utf-8")
    return re.findall(r'\{\{\s*copy\.(\w+)\s*\}\}', html)


def get_template_effect_calls(scene: str) -> list[str]:
    """Return effect function names called in the scene template."""
    path = ROOT / "templates" / "scenes" / f"scene-{scene}.html"
    if not path.exists():
        return []
    html = path.read_text(encoding="utf-8")
    return re.findall(r'\b(fade|slide|textReveal|counter|scale|reveal|blur)\s*\(', html)


def get_template_timeline_positions(scene: str) -> list[float]:
    """Extract absolute .add(..., position) values from the scene template."""
    path = ROOT / "templates" / "scenes" / f"scene-{scene}.html"
    if not path.exists():
        return []
    html = path.read_text(encoding="utf-8")
    # Match: tl.add(..., N.N) or .add(..., N)
    return [float(m) for m in re.findall(r'\.add\([^)]+,\s*(\d+(?:\.\d+)?)\s*\)', html)]


def run(spec_path: Path) -> bool:
    spec  = load_spec(spec_path)
    meta  = spec.get("meta", {})
    copy  = spec.get("copy", {})
    scene = spec.get("scene", "")

    passed = True
    print(f"\nPreflight: {spec_path.name}")
    print(f"  scene={scene}  system={meta.get('system','?')}  duration={meta.get('duration','?')}s\n")

    # ── FAIL: all copy fields in template must be present and non-empty ───────
    template_fields = get_template_copy_fields(scene)
    if not template_fields:
        warn(f"Scene template 'scene-{scene}.html' not found or has no copy fields — skipping copy checks")
    else:
        for field in set(template_fields):
            val = copy.get(field)
            if val is None:
                fail(f"copy.{field} missing from spec")
                passed = False
            elif str(val).strip() == "":
                fail(f"copy.{field} is empty")
                passed = False
            else:
                ok(f"copy.{field} = {repr(str(val))}")

    # ── FAIL: copy.stat must be numeric for counter scenes ───────────────────
    if scene in COUNTER_SCENES:
        stat = copy.get("stat")
        if stat is None:
            fail("copy.stat is required for stat-reveal scene")
            passed = False
        elif not isinstance(stat, (int, float)):
            fail(f"copy.stat must be numeric (got {type(stat).__name__}: {repr(stat)})")
            passed = False
        else:
            ok(f"copy.stat is numeric ({stat})")

    # ── FAIL: effects in template must exist in effect library ────────────────
    used_effects = set(get_template_effect_calls(scene))
    unknown = used_effects - EFFECTS
    if unknown:
        fail(f"Unknown effects in template: {unknown}")
        passed = False
    elif used_effects:
        ok(f"Effects used: {sorted(used_effects)} - all known")

    # ── FAIL: timeline positions must not exceed meta.duration ────────────────
    duration = meta.get("duration")
    if duration is not None:
        positions = get_template_timeline_positions(scene)
        if positions:
            max_pos = max(positions)
            # Allow up to duration (not strictly less than, since hold frames are fine)
            if max_pos >= float(duration):
                fail(f"Timeline position {max_pos}s >= meta.duration {duration}s — animation starts after video ends")
                passed = False
            else:
                ok(f"Timeline positions OK (max {max_pos}s < {duration}s)")

    # ── WARN: meta.seed should be set ─────────────────────────────────────────
    seed = meta.get("seed", "")
    if not seed or seed == "default":
        warn("meta.seed not set — geo layer randomness will be non-deterministic across runs")
    else:
        ok(f"meta.seed = {repr(seed)}")

    # ── WARN: Phase 1 system gate ─────────────────────────────────────────────
    system = meta.get("system")
    if system != "s01":
        warn(f"meta.system = '{system}' — Phase 1 only supports s01. Output may look wrong.")
    else:
        ok("meta.system = s01")

    # ── WARN: copy length limits ──────────────────────────────────────────────
    kicker = str(copy.get("kicker", ""))
    if kicker:
        words = len(kicker.split())
        if words > 6:
            warn(f"copy.kicker is {words} words (max 6) — may break GSAP timing")
        else:
            ok(f"copy.kicker word count OK ({words}/6)")

    context = str(copy.get("context", ""))
    if context:
        words = len(context.split())
        if words > 12:
            warn(f"copy.context is {words} words (max 12) — may overflow safe zone")
        else:
            ok(f"copy.context word count OK ({words}/12)")

    headline = str(copy.get("headline_1", copy.get("headline", "")))
    if headline:
        words = len(headline.split())
        if words > 8:
            warn(f"copy.headline is {words} words (max 8)")

    subhead = str(copy.get("subhead", ""))
    if subhead:
        words = len(subhead.split())
        if words > 10:
            warn(f"copy.subhead is {words} words (max 10)")

    # ── FAIL: orthography check on the scene HTML ─────────────────────────────
    scene_path = ROOT / "templates" / "scenes" / f"scene-{scene}.html"
    if _ortho_scan and scene_path.exists():
        ortho = _ortho_scan(scene_path)
        if ortho:
            for found, suggestion, ctx in ortho:
                fail(f"ortho: '{found}' -> '{suggestion}'  {ctx}")
            passed = False
        else:
            ok("orthography OK")
    elif not _ortho_scan:
        warn("orthography_check.py not found — skipping accent check")

    # ── WARN: CDN script references + raw easing strings ─────────────────────
    if scene_path.exists():
        scene_text = scene_path.read_text(encoding="utf-8")
        cdn_refs = re.findall(r'<script[^>]+src=["\']https?://[^"\']+["\']', scene_text, re.IGNORECASE)
        if cdn_refs:
            for ref in cdn_refs:
                warn(f"CDN script reference — use vendor/ path: {ref[:80]}")
        else:
            ok("no CDN script references (vendor paths OK)")
        raw_eases = re.findall(r'"(power[23]\.out)"', scene_text)
        if raw_eases:
            warn(f"raw easing strings found ({len(raw_eases)}x power*.out) — consider the named easing palette")

        # ── FAIL: Lottie autoplay must always be false ────────────────────────
        # lottie.loadAnimation({..., autoplay: true, ...}) produces a running animation
        # that is not on the GSAP timeline — breaks Lock 10.
        lottie_autoplay = re.findall(
            r'lottie\.loadAnimation\s*\([^)]*autoplay\s*:\s*true', scene_text, re.DOTALL
        )
        if lottie_autoplay:
            fail(f"Lottie autoplay:true detected ({len(lottie_autoplay)} instance(s)) — must be autoplay:false (Lock 10)")
            passed = False
        elif "lottie" in scene_text.lower():
            ok("Lottie init present with autoplay:false — OK")

        # ── WARN: VERSIONS.md mismatch — vendor file referenced but not in VERSIONS.md ─
        vendor_refs = re.findall(r'vendor/[^\s"\']+', scene_text)
        if vendor_refs:
            versions_path = ROOT / "vendor" / "VERSIONS.md"
            if versions_path.exists():
                versions_text = versions_path.read_text(encoding="utf-8")
                for ref in vendor_refs:
                    fname = Path(ref).name
                    if fname and fname not in versions_text:
                        warn(f"vendor file not in VERSIONS.md: {fname}")
            else:
                warn("vendor/ directory referenced but vendor/VERSIONS.md is missing")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    if passed:
        print("Preflight PASSED — safe to render")
    else:
        print("Preflight FAILED — fix errors above before rendering")

    return passed


def main():
    if len(sys.argv) < 2:
        print("Usage: py scripts/motion_preflight.py motion/specs/my-spec.json")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    if not spec_path.exists():
        print(f"FAIL: spec not found: {spec_path}")
        sys.exit(1)

    passed = run(spec_path)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
