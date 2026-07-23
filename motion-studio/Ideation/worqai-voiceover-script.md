# WorqAI — Voiceover Script (scene-launch-villain-v3, 46s cut)

Spanish voiceover for `video_villain_v3_*.mp4`. 7 beats, ~70 words, placed by GSAP label —
not by hand-timing in an editor. You generate **one continuous take**; `split_voiceover.py`
cuts it into the 7 clips and drops each at its label.

> Replaces the old 20s/single-tailor script. Beats below match the current 46s, three-tailor cut.

---

## ElevenLabs settings

| Setting | Value |
|---|---|
| **Voice** | A native Spanish voice (e.g. *Mateo* / *Diego*) |
| **Model** | Eleven Multilingual v2 |
| **Language Override** | Spanish |
| **Speed** | **1.0x** (the cut is 46s now — no need to rush) |
| **Stability** | 60–65% |
| **Similarity** | 85–90% |
| **Style** | 10–15% |
| **Speaker Boost** | ON |
| **Output** | WAV (best) or MP3 44.1 kHz — save as `export-video/vo_villain_v3.mp3` |

**Brand pronunciation: "wor-KAI" (one word).** It's written **`Workái`** in the script below so
the TTS says it correctly — do not "fix" it back to WorqAI before generating.

---

## The script — paste this whole block as ONE generation

```
El mismo CV para todas las vacantes. Por eso no te llaman. Hoy su puntuación es veintitrés sobre cien: le faltan las palabras clave del puesto. No necesitas un mejor CV. Necesitas uno para cada vacante. Workái lee la vacante y reescribe cada línea con tus logros reales. Otra vacante, otro CV, en segundos. De veintitrés a más de noventa, en cada postulación. Sube tu CV y descubre tu puntuación. Gratis, en workái punto io.
```

> Generate it once, back to back. The pauses don't matter — the splitter places each line by time.

---

## The 7 beats (what lands where)

Labels and times are the scene's actual `MOTION_LABELS` (resolved 2026-06-11).

| # | Label | Time | Line |
|---|---|---|---|
| 1 | `wound` | 0.4s | El mismo CV para todas las vacantes. Por eso no te llaman. |
| 2 | `score_low` | 10.0s | Hoy su puntuación es veintitrés sobre cien. Le faltan las palabras clave del puesto. |
| 3 | `cheat_code` | 14.6s | No necesitas un mejor CV. Necesitas uno para cada vacante. |
| 4 | `tailor1_start` | 18.2s | Workái lee la vacante y reescribe cada línea con tus logros reales. |
| 5 | `tailor2_start` | 24.5s | Otra vacante. Otro CV. En segundos. |
| 6 | `tailor3_score` | 32.0s | De veintitrés a más de noventa. En cada postulación. |
| 7 | `cta` | 40.5s | Sube tu CV y descubre tu puntuación. Gratis, en workái punto io. |

Order is fixed in `motion/specs/vo_villain_v3.json` — segment 1 → entry 1, etc.
(The json uses brand spelling — WorqAI, worqai.io — because its `line` fields feed the burned captions; the phonetic `Workái` lives only in the TTS block above.)

---

## How to assemble

One command once `export-video/vo_villain_v3.mp3` exists:

```bash
py scripts/make_film.py --film films/launch-villain-v3.json
```

Or step-by-step with `add_sounds.py` / `split_voiceover.py` — see their docstrings.

### If the auto-split miscounts
A gapless take may not have detectable silences. Two levers:

```bash
# more sensitive gap detection
... --noise -25 --min-silence 0.12

# or cut exactly where you say: listen once, note where each of lines 2–7 STARTS
# (6 timestamps in seconds of the take), pass them in order:
... --cuts "6.4,11.8,15.9,22.0,25.1,33.0"
```

`--cuts` always works, even on a take with no pauses at all.

---

## Notes
- Numbers are spelled out (`veintitrés`, `noventa`) so the TTS reads them as words.
- Line 3 is the only line that's also on screen — reinforcing the hero line at the emotional
  peak is intentional. Every other line adds what the screen doesn't say.
- The voiceover is your own narration — safe to bake in. Music comes from the manifest's
  licensed bed (ducked under VO) or is added in-app after upload. Never bake platform/
  copyrighted audio.
