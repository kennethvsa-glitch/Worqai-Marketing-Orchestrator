"""
make_film.py — one-command film builder.

Reads a manifest JSON and runs the full pipeline:
  export → sfx → voiceover → music+ducking → loudnorm → captions → cutdowns

Usage:
    py scripts/make_film.py --film films/launch-villain.json
    py scripts/make_film.py --film films/launch-villain.json --draft
    py scripts/make_film.py --film films/launch-villain.json --skip-export

Manifest format (all fields optional except name + scene):
{
  "name":    "launch-villain",
  "scene":   "templates/scenes/scene-launch-villain-v3.html",
  "sounds":  "motion/specs/sounds_villain.json",
  "voiceover": {
    "audio":  "export-video/vo_villain.mp3",
    "script": "motion/specs/vo_villain.json"
  },
  "music": {
    "file":    "Ideation/music/bed.mp3",
    "volume":  0.18,
    "duck_db": 8.0
  },
  "cutdowns": [
    { "name": "hook-6s",  "from_label": "wound_start", "to_label": "stamp" },
    { "name": "15s-cut",  "from_sec": 0, "to_label": "turn_end" }
  ],
  "captions": true
}

VO script format (motion/specs/vo_*.json):
[
  { "label": "intro_line1", "line": "El 73% de los CVs...", "volume": 1.0, "offset_ms_add": 0 },
  ...
]
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from _config import FFMPEG, FFPROBE
from _browser import launch_chromium



_SEGMENT_ENDPOINT_KEYS = {"to_label", "to_sec"}
_CUTDOWN_ENDPOINT_KEYS = {"to_label", "to_sec"}


def validate_manifest(manifest: dict, manifest_dir: Path) -> dict:
    """Browser-free asset and structure check.

    Returns {"status": "ok"|"error", "errors": [...], "warnings": [...]}.
    Each entry: {"asset": str, "path": str, "reason": str}.
    manifest_dir is the base for resolving all relative paths in the manifest.
    """
    errors: list[dict] = []
    warnings: list[dict] = []

    scene_rel = manifest.get("scene", "")
    if not scene_rel:
        errors.append({"asset": "scene", "path": "", "reason": "scene key missing from manifest"})
    else:
        scene_path = (manifest_dir / scene_rel).resolve()
        if not scene_path.exists():
            errors.append({"asset": "scene", "path": scene_rel, "reason": "file not found"})

    sounds_rel = manifest.get("sounds", "")
    if sounds_rel:
        sounds_json_path = (manifest_dir / sounds_rel).resolve()
        if not sounds_json_path.exists():
            errors.append({"asset": "sounds_json", "path": sounds_rel, "reason": "file not found"})
        else:
            sounds_dir = manifest_dir / "Ideation" / "Sound effects"
            entries = json.loads(sounds_json_path.read_text(encoding="utf-8"))
            seen_prefixes: set[str] = set()
            for entry in entries:
                prefix = entry.get("file", "")
                if not prefix or prefix in seen_prefixes:
                    continue
                seen_prefixes.add(prefix)
                if sounds_dir.exists():
                    matches = [f for f in sounds_dir.iterdir() if f.name.startswith(prefix)]
                    if not matches:
                        errors.append({
                            "asset": "sound_file",
                            "path": str(sounds_dir / prefix),
                            "reason": f"no file starting with '{prefix}' in sounds directory",
                        })
                else:
                    errors.append({
                        "asset": "sound_file",
                        "path": str(sounds_dir / prefix),
                        "reason": "sounds directory does not exist",
                    })

    vo_cfg = manifest.get("voiceover")
    if vo_cfg:
        vo_audio_rel = vo_cfg.get("audio", "")
        vo_script_rel = vo_cfg.get("script", "")
        if vo_audio_rel:
            if not (manifest_dir / vo_audio_rel).resolve().exists():
                warnings.append({
                    "asset": "voiceover_audio",
                    "path": vo_audio_rel,
                    "reason": "file not found",
                })
        if vo_script_rel:
            if not (manifest_dir / vo_script_rel).resolve().exists():
                warnings.append({
                    "asset": "voiceover_script",
                    "path": vo_script_rel,
                    "reason": "file not found",
                })

    music_cfg = manifest.get("music")
    if music_cfg:
        music_rel = music_cfg.get("file", "")
        if music_rel:
            if not (manifest_dir / music_rel).resolve().exists():
                warnings.append({
                    "asset": "music",
                    "path": music_rel,
                    "reason": "file not found",
                })

    for i, cut in enumerate(manifest.get("cutdowns", [])):
        if "name" not in cut:
            errors.append({
                "asset": f"cutdown[{i}]",
                "path": "",
                "reason": "missing required key: name",
            })
            continue
        cut_name = cut["name"]
        if "segments" in cut:
            for j, seg in enumerate(cut["segments"]):
                if not _SEGMENT_ENDPOINT_KEYS.intersection(seg):
                    errors.append({
                        "asset": f"cutdown '{cut_name}' segment[{j}]",
                        "path": "",
                        "reason": "segment missing end point (to_label or to_sec)",
                    })
        else:
            if not _CUTDOWN_ENDPOINT_KEYS.intersection(cut):
                errors.append({
                    "asset": f"cutdown '{cut_name}'",
                    "path": "",
                    "reason": "missing end point (to_label or to_sec)",
                })

    status = "error" if errors else "ok"
    return {"status": status, "errors": errors, "warnings": warnings}


def resolve_labels(html_path: Path) -> dict[str, float]:
    """Returns {label: seconds} from MOTION_LABELS in the rendered scene."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("playwright not installed: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.as_posix()}")
        try:
            page.wait_for_function("window.motionReady === true", timeout=20_000)
        except Exception:
            browser.close()
            raise SystemExit(f"FAIL: motionReady never fired for {html_path.name}")
        raw = page.evaluate("window.MOTION_LABELS || {}")
        browser.close()
    return {k: v / 1000.0 for k, v in raw.items()}


def has_audio_stream(mp4: Path) -> bool:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type",
         "-of", "default=noprint_wrappers=1:nokey=1", str(mp4)],
        capture_output=True, text=True)
    return bool(r.stdout.strip())


def lint_scene(html_path: Path) -> None:
    """Run the determinism/contract gate (scene_lint.py). FAILs abort the build."""
    script = ROOT / "scripts" / "scene_lint.py"
    if not script.exists():
        print("  WARN: scene_lint.py not found — skipping determinism gate")
        return
    r = subprocess.run([sys.executable, str(script), str(html_path)])
    if r.returncode != 0:
        raise SystemExit("Scene lint FAILED — fix determinism/contract issues above (or pass --skip-lint)")


def export_scene(html_path: Path, out_dir: Path, stem: str, draft: bool) -> Path:
    script = ROOT / "scripts" / "motion_exporter.py"
    cmd = [sys.executable, str(script),
           "--input", str(html_path),
           "--output", str(out_dir),
           "--name", stem]
    if draft:
        cmd.append("--draft")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit("Export failed — see output above")
    date_str = datetime.now().strftime("%Y-%m-%d")
    suffix = "_draft" if draft else ""
    mp4 = out_dir / f"video_{stem}{suffix}_{date_str}.mp4"
    if not mp4.exists():
        candidates = sorted(out_dir.glob(f"video_{stem}*.mp4"),
                            key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            raise SystemExit(f"Export produced no MP4 in {out_dir}")
        mp4 = candidates[0]
    return mp4


def mix_sfx(video: Path, sounds_json: Path, html_path: Path, tmp: Path) -> Path:
    out = tmp / f"{video.stem}_sfx.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([
        sys.executable, str(ROOT / "scripts" / "add_sounds.py"),
        "--video", str(video),
        "--sounds", str(sounds_json),
        "--html", str(html_path),
        "--output", str(out),
    ])
    if r.returncode != 0:
        raise SystemExit("SFX mix failed — see output above")
    return out


def mix_vo(video: Path, vo_audio: Path, vo_script: Path, html_path: Path, tmp: Path) -> Path:
    out = tmp / f"{video.stem}_vo.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([
        sys.executable, str(ROOT / "scripts" / "split_voiceover.py"),
        "--video", str(video),
        "--vo", str(vo_audio),
        "--script", str(vo_script),
        "--html", str(html_path),
        "--output", str(out),
    ])
    if r.returncode != 0:
        raise SystemExit("VO mix failed — see output above")
    return out


def get_vo_times(vo_script: Path, labels: dict[str, float]) -> list[tuple[float, float]]:
    """Estimate (start, end) seconds for each VO segment — used for music ducking."""
    entries = json.loads(vo_script.read_text(encoding="utf-8"))
    times: list[tuple[float, float]] = []
    sorted_entries = [(e, labels.get(e.get("label", ""), None)) for e in entries]
    for i, (entry, start) in enumerate(sorted_entries):
        if start is None:
            continue
        start += entry.get("offset_ms_add", 0) / 1000.0
        # end = next label start - 0.2s, or word-count estimate
        word_count = len(entry.get("line", "").split()) or 5
        est_dur = max(1.5, word_count / 2.5)
        # check next segment for a tighter bound
        for next_entry, next_start in sorted_entries[i + 1:]:
            if next_start is not None:
                gap = next_start - start
                if gap < est_dur:
                    est_dur = max(1.0, gap - 0.2)
                break
        times.append((start, start + est_dur))
    return times


def mix_music(video: Path, music_file: Path,
              normal_vol: float, duck_db: float,
              vo_times: list[tuple[float, float]], tmp: Path) -> Path:
    """Mix a music bed, ducked during VO windows."""
    out = tmp / f"{video.stem}_music.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    duck_vol = normal_vol * (10 ** (-duck_db / 20.0))

    if vo_times:
        conditions = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in vo_times)
        vol_expr = f"if(gt({conditions},0),{duck_vol:.4f},{normal_vol:.4f})"
        bed_filter = f"[1:a]volume=eval=frame:volume='{vol_expr}'[bed]"
    else:
        bed_filter = f"[1:a]volume={normal_vol}[bed]"

    if has_audio_stream(video):
        fc = f"{bed_filter};[0:a][bed]amix=inputs=2:duration=first:normalize=0[out]"
    else:
        fc = f"{bed_filter};[bed]aresample=async=1[out]"

    cmd = [FFMPEG, "-y",
           "-i", str(video), "-i", str(music_file),
           "-filter_complex", fc,
           "-map", "0:v", "-map", "[out]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Music mix failed:\n{r.stderr[-2000:]}")
    return out


def apply_loudnorm(src: Path, dst: Path, target_lufs: float = -14.0) -> None:
    cmd = [FFMPEG, "-y", "-i", str(src),
           "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Loudnorm failed:\n{r.stderr[-2000:]}")


def _sec_to_ass(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def gen_captions_ass(vo_script: Path, labels: dict[str, float]) -> str:
    """Build an ASS subtitle file in the brand style from VO script + label times."""
    entries = json.loads(vo_script.read_text(encoding="utf-8"))
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        # PrimaryColour: white &H00FFFFFF; BackColour semi-black &HCC000000
        "Style: Caption,Inter,40,&H00ECEAE1,&H000000FF,&H00000000,"
        "&H99000000,0,0,0,0,100,100,0.5,0,1,2,0,2,80,80,200,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    lines: list[str] = []
    sorted_entries = [(e, labels.get(e.get("label", ""), None)) for e in entries]
    for i, (entry, start_t) in enumerate(sorted_entries):
        if start_t is None:
            continue
        text = entry.get("line", "").strip()
        if not text:
            continue
        start_t += entry.get("offset_ms_add", 0) / 1000.0
        word_count = len(text.split()) or 5
        est_dur = max(2.0, word_count / 2.5)
        for next_entry, next_t in sorted_entries[i + 1:]:
            if next_t is not None:
                gap = next_t - start_t
                if gap < est_dur:
                    est_dur = max(1.5, gap - 0.15)
                break
        end_t = start_t + est_dur
        lines.append(
            f"Dialogue: 0,{_sec_to_ass(start_t)},{_sec_to_ass(end_t)},"
            f"Caption,,0,0,0,,{text}"
        )
    return header + "\n".join(lines) + "\n"


def burn_captions(video: Path, ass_content: str, output: Path, tmp: Path) -> None:
    ass_path = tmp / "captions.ass"
    ass_path.write_text(ass_content, encoding="utf-8")
    # Use relative filename + cwd=tmp to avoid Windows drive-letter colon escaping
    # in ffmpeg filter strings (C\:/ splits incorrectly as original_size option).
    cmd = [FFMPEG, "-y", "-i", str(video.resolve()),
           "-vf", "ass=captions.ass",
           "-c:a", "copy", str(output.resolve())]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(tmp))
    if r.returncode != 0:
        raise SystemExit(f"Caption burn failed:\n{r.stderr[-2000:]}")


def make_cutdown(src: Path, from_sec: float, to_sec: float, output: Path) -> None:
    """Stream-copy slice — no re-encode."""
    cmd = [FFMPEG, "-y",
           "-ss", f"{from_sec:.3f}",
           "-i", str(src),
           "-t", f"{to_sec - from_sec:.3f}",
           "-c", "copy", str(output)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Cutdown failed:\n{r.stderr[-2000:]}")


def make_multiseg_cutdown(src: Path, segments: list, labels: dict,
                          output: Path, tmp: Path) -> tuple[Path | None, str | None]:
    """Re-encode each segment to a temp file, then concat. Required for mid-file accuracy."""
    seg_files: list[Path] = []
    for i, seg in enumerate(segments):
        if "from_label" in seg:
            lbl = seg["from_label"]
            if lbl not in labels:
                return None, f"from_label '{lbl}' not in labels"
            from_s = labels[lbl] + seg.get("from_offset_s", 0.0)
        else:
            from_s = float(seg.get("from_sec", 0.0))

        if "to_label" in seg:
            lbl = seg["to_label"]
            if lbl not in labels:
                return None, f"to_label '{lbl}' not in labels"
            to_s = labels[lbl] + seg.get("to_offset_s", 0.0)
        elif "to_sec" in seg:
            to_s = float(seg["to_sec"])
        else:
            return None, "segment has no end point"

        seg_f = tmp / f"_seg_{i:02d}.mp4"
        cmd = [FFMPEG, "-y",
               "-ss", f"{from_s:.3f}", "-i", str(src),
               "-t",  f"{to_s - from_s:.3f}",
               "-c:v", "libx264", "-crf", "18", "-preset", "fast",
               "-c:a", "aac", "-b:a", "192k",
               str(seg_f)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            return None, f"Segment {i} failed:\n{r.stderr[-1000:]}"
        seg_files.append(seg_f)

    concat_list = tmp / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{f.as_posix()}'" for f in seg_files),
        encoding="utf-8"
    )
    cmd = [FFMPEG, "-y",
           "-f", "concat", "-safe", "0",
           "-i", str(concat_list),
           "-c", "copy", str(output)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None, f"Concat failed:\n{r.stderr[-1000:]}"
    return output, None


def main() -> None:
    ap = argparse.ArgumentParser(description="One-command motion film builder")
    ap.add_argument("--film",        type=Path, required=True, help="Film manifest JSON")
    ap.add_argument("--draft",       action="store_true",      help="Draft-mode export (15fps, 540p)")
    ap.add_argument("--skip-export",   action="store_true",      help="Reuse most-recent existing export")
    ap.add_argument("--validate-only", action="store_true",      help="Browser-free asset check; print JSON and exit")
    ap.add_argument("--skip-lint",     action="store_true",      help="Skip the scene determinism/contract gate (scene_lint.py)")
    ap.add_argument("--output",        type=Path, default=ROOT / "export-video")
    args = ap.parse_args()

    try:
        manifest = json.loads(args.film.resolve().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if not args.validate_only:
            raise
        result = {
            "status": "error",
            "errors": [{
                "asset": "manifest",
                "path": str(args.film),
                "reason": str(exc),
            }],
            "warnings": [],
        }
        print(json.dumps(result, separators=(",", ":")))
        sys.exit(1)

    if args.validate_only:
        result = validate_manifest(manifest, ROOT)
        print(json.dumps(result, separators=(",", ":")))
        sys.exit(1 if result["errors"] else 0)

    name      = manifest["name"]
    scene     = (ROOT / manifest["scene"]).resolve()
    out_dir   = args.output.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str  = datetime.now().strftime("%Y-%m-%d")

    print(f"\n[make_film] {name}")

    # ── Scene gate (determinism locks + contract) ─────────────────────────────
    if not args.skip_lint:
        print("Linting scene (determinism + contract)...")
        lint_scene(scene)

    # ── Label resolution (shared across all stages) ───────────────────────────
    print("Resolving scene labels...")
    labels = resolve_labels(scene)
    if labels:
        print(f"  {len(labels)} labels: {', '.join(sorted(labels))}")
    else:
        print("  WARN: no MOTION_LABELS found — label-based features unavailable")

    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)

        # ── 1. Export ─────────────────────────────────────────────────────────
        if args.skip_export:
            suffix = "_draft" if args.draft else ""
            master_re = re.compile(rf"^video_{re.escape(name)}{suffix}_\d{{4}}-\d{{2}}-\d{{2}}\.mp4$")
            candidates = sorted(
                [p for p in out_dir.glob(f"video_{name}*.mp4") if master_re.match(p.name)],
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not candidates:
                raise SystemExit(f"--skip-export: no existing master export for {name} in {out_dir}")
            current = candidates[0]
            print(f"Reusing export: {current.name}")
        else:
            print("\nStep 1/7 — Exporting scene...")
            current = export_scene(scene, out_dir, name, args.draft)

        # ── 2. SFX ───────────────────────────────────────────────────────────
        if manifest.get("sounds"):
            sounds_path = (ROOT / manifest["sounds"]).resolve()
            if sounds_path.exists():
                print("\nStep 2/7 — Mixing SFX...")
                current = mix_sfx(current, sounds_path, scene, tmp)
            else:
                print(f"WARN: sounds file not found: {sounds_path.relative_to(ROOT)}")

        # ── 3. Voiceover ─────────────────────────────────────────────────────
        vo_times: list[tuple[float, float]] = []
        vo_script_path: Path | None = None
        if manifest.get("voiceover"):
            vo_cfg        = manifest["voiceover"]
            vo_audio      = (ROOT / vo_cfg["audio"]).resolve()
            vo_script_path = (ROOT / vo_cfg["script"]).resolve()
            if vo_audio.exists() and vo_script_path.exists():
                print("\nStep 3/7 — Mixing voiceover...")
                current   = mix_vo(current, vo_audio, vo_script_path, scene, tmp)
                vo_times  = get_vo_times(vo_script_path, labels)
            else:
                missing = [str(p.relative_to(ROOT))
                           for p in [vo_audio, vo_script_path] if not p.exists()]
                print(f"WARN: voiceover files not found: {missing}")

        # ── 4. Music bed + sidechain ducking ─────────────────────────────────
        if manifest.get("music"):
            mc = manifest["music"]
            music_file = (ROOT / mc["file"]).resolve()
            if music_file.exists():
                print("\nStep 4/7 — Mixing music bed (ducked under VO)...")
                # Extend vo_times with extra_duck windows from manifest
                all_duck_times = list(vo_times)
                for xd in mc.get("extra_duck", []):
                    lbl = xd.get("label")
                    if lbl and lbl in labels:
                        t0 = labels[lbl] + float(xd.get("offset_s", 0.0))
                        t1 = t0 + float(xd.get("dur_s", 1.0))
                        all_duck_times.append((t0, t1))
                    else:
                        print(f"  WARN: extra_duck label '{lbl}' not in labels — skipped")
                current = mix_music(
                    current, music_file,
                    float(mc.get("volume", 0.18)),
                    float(mc.get("duck_db", 8.0)),
                    all_duck_times, tmp,
                )
            else:
                print(f"WARN: music file not found: {music_file.relative_to(ROOT)}")

        # ── 5. Loudnorm ───────────────────────────────────────────────────────
        final_stem = f"video_{name}_{date_str}"
        final_path = out_dir / f"{final_stem}.mp4"

        if has_audio_stream(current):
            print("\nStep 5/7 — Loudnorm (-14 LUFS)...")
            apply_loudnorm(current, final_path)
        else:
            shutil.copy2(current, final_path)
            print(f"\nStep 5/7 — Silent master (no audio track).")

        size_mb = final_path.stat().st_size / 1_048_576
        print(f"\nMaster: {final_path.name}  ({size_mb:.1f} MB)")

        # ── 6. Burned captions ────────────────────────────────────────────────
        if manifest.get("captions") and vo_script_path and vo_script_path.exists():
            print("\nStep 6/7 — Burning captions...")
            ass = gen_captions_ass(vo_script_path, labels)
            cap_path = out_dir / f"{final_stem}_captions.mp4"
            burn_captions(final_path, ass, cap_path, tmp)
            size_mb = cap_path.stat().st_size / 1_048_576
            print(f"  {cap_path.name}  ({size_mb:.1f} MB)")
        else:
            print("\nStep 6/7 — Captions: skipped (no VO script or captions not requested)")

        # ── 7. Cutdowns ───────────────────────────────────────────────────────
        cutdowns = manifest.get("cutdowns", [])
        if cutdowns:
            print(f"\nStep 7/7 — Generating {len(cutdowns)} cutdown(s)...")
            for cut in cutdowns:
                cut_name = cut["name"]
                cut_path = out_dir / f"{final_stem}_{cut_name}.mp4"

                if "segments" in cut:
                    # Multi-segment cutdown: re-encode each slice + concat
                    result, err = make_multiseg_cutdown(
                        final_path, cut["segments"], labels, cut_path, tmp
                    )
                    if err:
                        print(f"  WARN: '{cut_name}' multi-seg failed — {err}")
                        continue
                    size_mb = cut_path.stat().st_size / 1_048_576
                    print(f"  {cut_name}: multi-seg — {cut_path.name}  ({size_mb:.1f} MB)")
                else:
                    # Single-range cutdown (legacy): stream-copy
                    if "from_label" in cut:
                        lbl = cut["from_label"]
                        if lbl not in labels:
                            print(f"  WARN: '{cut_name}' from_label '{lbl}' not in labels — skipped")
                            continue
                        from_sec = labels[lbl]
                    else:
                        from_sec = float(cut.get("from_sec", 0.0))

                    if "to_label" in cut:
                        lbl = cut["to_label"]
                        if lbl not in labels:
                            print(f"  WARN: '{cut_name}' to_label '{lbl}' not in labels — skipped")
                            continue
                        to_sec = labels[lbl]
                    elif "to_sec" in cut:
                        to_sec = float(cut["to_sec"])
                    else:
                        print(f"  WARN: '{cut_name}' has no end point — skipped")
                        continue

                    make_cutdown(final_path, from_sec, to_sec, cut_path)
                    dur = to_sec - from_sec
                    size_mb = cut_path.stat().st_size / 1_048_576
                    print(f"  {cut_name}: {dur:.1f}s — {cut_path.name}  ({size_mb:.1f} MB)")
        else:
            print("\nStep 7/7 — Cutdowns: none specified")

    print(f"\n[make_film] Complete — {final_path.name}")


if __name__ == "__main__":
    main()
