"""
split_voiceover.py — cut a single continuous AI voiceover into per-beat clips and
mix each onto the video at its GSAP-label time.

Why this exists: the AI voice apps return ONE back-to-back take with no pauses, but
the scene's voiceover beats are spread across ~46s (line 1 at ~1s, line 2 at ~10s,
the Turn at ~15s, ...). A single take can't line up with that. This slices the take
into N segments and places each at the right label — no hand-editing timecodes.

Cut modes:
  auto   (default) — ffmpeg silencedetect finds the sentence gaps; the N-1 longest
                     gaps become the cut points.
  manual           — pass --cuts "t1,t2,..." (N-1 timestamps in seconds of the take)
                     and it cuts exactly there. Always works, even on a gapless take.

Usage:
  # auto-detect the gaps
  py scripts/split_voiceover.py \
     --video export-video/video_output_2026-06-08.mp4 \
     --vo export-video/vo_blob.mp3 \
     --script motion/specs/voiceover_launch_honest_s01.json \
     --html templates/scenes/output.html \
     --output export-video/video_output_vo.mp4

  # if auto miscounts: listen once, note where each line STARTS, pass the 6 boundaries
  py scripts/split_voiceover.py ... --cuts "6.4,11.8,15.9,22.0,25.1,33.0"

The --script JSON is an ORDERED list; segment i is placed at entry i's label:
  [ { "label": "intro_line1", "volume": 1.0, "offset_ms_add": 0, "line": "..." }, ... ]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT   = Path(__file__).parent.parent
from _config import FFMPEG, FFPROBE

# Reuse the label resolver from add_sounds.py so timing stays identical to the SFX pass.
sys.path.insert(0, str(Path(__file__).parent))
try:
    from add_sounds import resolve_labels
except Exception as e:  # pragma: no cover
    raise SystemExit(f"FAIL: could not import resolve_labels from add_sounds.py: {e}")


def media_duration(path: Path) -> float:
    """Seconds, via ffprobe."""
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise SystemExit(f"FAIL: ffprobe could not read duration of {path.name}\n{r.stderr[-800:]}")
    return float(r.stdout.strip())


def detect_silences(vo: Path, noise_db: float, min_silence: float):
    """Return list of (start, end, dur) silences via ffmpeg silencedetect."""
    r = subprocess.run(
        [FFMPEG, "-i", str(vo), "-af",
         f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True)
    text = r.stderr
    starts = [float(m) for m in re.findall(r"silence_start:\s*([0-9.]+)", text)]
    ends   = [float(m) for m in re.findall(r"silence_end:\s*([0-9.]+)", text)]
    sils = []
    for s, e in zip(starts, ends):
        sils.append((s, e, e - s))
    return sils


def auto_cut_points(vo: Path, n_segments: int, noise_db: float, min_silence: float):
    """Pick n_segments-1 cut points (silence midpoints), choosing the longest gaps."""
    need = n_segments - 1
    if need == 0:
        return []
    sils = detect_silences(vo, noise_db, min_silence)
    if len(sils) < need:
        boundaries = ", ".join(f"{s:.2f}-{e:.2f}s" for s, e, _ in sils) or "(none)"
        raise SystemExit(
            f"FAIL: need {need} gaps but silencedetect found {len(sils)} at "
            f"noise={noise_db}dB d={min_silence}s.\n"
            f"  detected silences: {boundaries}\n"
            f"  → try a higher threshold (e.g. --noise -25), a shorter --min-silence 0.12,\n"
            f"    or list the cut points yourself with --cuts \"t1,t2,...\" (seconds in the take).")
    # take the longest `need` gaps, then order by time
    longest = sorted(sils, key=lambda x: x[2], reverse=True)[:need]
    cuts = sorted((s + e) / 2 for s, e, _ in longest)
    return cuts


def main():
    ap = argparse.ArgumentParser(description="Split one VO take into per-label clips and mix onto video")
    ap.add_argument("--video",  type=Path, required=True, help="Input MP4 (silent, or SFX already mixed)")
    ap.add_argument("--vo",     type=Path, required=True, help="Single continuous voiceover audio (mp3/wav)")
    ap.add_argument("--script", type=Path, required=True, help="Ordered voiceover JSON (entry i -> segment i)")
    ap.add_argument("--html",   type=Path, required=True, help="Rendered HTML for label resolution")
    ap.add_argument("--output", type=Path, required=True, help="Output MP4")
    ap.add_argument("--cuts",   type=str,  default=None,  help="Manual cut points: \"t1,t2,...\" (N-1 secs)")
    ap.add_argument("--noise",  type=float, default=-30.0, help="silencedetect noise floor dB (default -30)")
    ap.add_argument("--min-silence", type=float, default=0.18, help="min silence seconds (default 0.18)")
    ap.add_argument("--lead-ms", type=int, default=0, help="trim this many ms off the start of every segment")
    args = ap.parse_args()

    entries = json.loads(args.script.read_text(encoding="utf-8"))
    n = len(entries)
    if n == 0:
        raise SystemExit("FAIL: voiceover script is empty")

    if not args.vo.exists():
        raise SystemExit(f"FAIL: voiceover audio not found: {args.vo}")

    dur = media_duration(args.vo)

    # ── cut points (internal boundaries) ──────────────────────────────────────
    if args.cuts:
        cuts = [float(x) for x in args.cuts.split(",") if x.strip()]
        if len(cuts) != n - 1:
            raise SystemExit(f"FAIL: --cuts has {len(cuts)} points but {n} segments need {n - 1}")
    else:
        cuts = auto_cut_points(args.vo, n, args.noise, args.min_silence)
        print(f"Auto cut points (s): {', '.join(f'{c:.2f}' for c in cuts)}")

    bounds = [0.0] + cuts + [dur]   # n+1 boundaries -> n segments

    # ── resolve label times ───────────────────────────────────────────────────
    print(f"Reading MOTION_LABELS from {args.html.name}...")
    labels = resolve_labels(args.html)
    if not labels:
        raise SystemExit("FAIL: MOTION_LABELS empty — scene has no tl.addLabel() calls?")

    delays = []
    for i, e in enumerate(entries):
        lbl = e["label"]
        if lbl not in labels:
            raise SystemExit(f"FAIL: label '{lbl}' not in MOTION_LABELS — available: {sorted(labels)}")
        delays.append(int(labels[lbl]) + int(e.get("offset_ms_add", 0)))

    # ── build one ffmpeg filter graph: split -> trim -> delay -> mix ──────────
    split_outs = "".join(f"[c{i}]" for i in range(n))
    parts = [f"[1:a]asplit={n}{split_outs}"]
    for i, e in enumerate(entries):
        start = bounds[i] + args.lead_ms / 1000.0
        end   = bounds[i + 1]
        vol   = e.get("volume", 1.0)
        d     = max(0, delays[i])
        seg = (f"[c{i}]atrim=start={start:.3f}:end={end:.3f},"
               f"asetpts=PTS-STARTPTS,adelay={d}:all=1,volume={vol}[a{i}]")
        parts.append(seg)
        print(f"  seg {i+1}/{n}  take {start:6.2f}-{end:6.2f}s  ->  {e['label']} @ {d/1000:.2f}s")
    # Include existing video audio (SFX track) in the mix if present
    has_vid_audio = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type",
         "-of", "default=noprint_wrappers=1:nokey=1", str(args.video.resolve())],
        capture_output=True, text=True
    ).stdout.strip() != ""

    if has_vid_audio:
        mix_in = "".join(f"[a{i}]" for i in range(n)) + "[0:a]"
        parts.append(f"{mix_in}amix=inputs={n+1}:duration=longest:normalize=0[vo]")
        print(f"  + existing video audio included in mix (SFX preserved)")
    else:
        mix_in = "".join(f"[a{i}]" for i in range(n))
        parts.append(f"{mix_in}amix=inputs={n}:duration=longest:normalize=0[vo]")

    cmd = [
        FFMPEG, "-y", "-i", str(args.video.resolve()), "-i", str(args.vo.resolve()),
        "-filter_complex", ";".join(parts),
        "-map", "0:v", "-map", "[vo]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(args.output.resolve()),
    ]
    print(f"Mixing {n} voiceover segments -> {args.output.name}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg error:\n{r.stderr[-2000:]}")
    size_mb = args.output.stat().st_size / 1_048_576
    print(f"Done: {args.output.name}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
