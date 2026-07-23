# WorqAI — villain-v4 "El Loop Cerrado" — Full Production Plan

The remake. Same villain thesis, two structural upgrades v3 doesn't have:
**the story closes its own loop** (the device that delivers the wound returns to deliver
the healing), and **the frame carries the Expensive Layer** (house easing, particles,
variable-weight typography, post-processing) from the expansion plan.

**9:16 · 1080×1920 · ~50s · 60fps.** Built as `scene-launch-villain-v4.{html,css}` —
a copy of v3 *after* the round-2 fixes land, ported onto `motion-lib.js`.

> Naming note: `worqai-v4-plan-rebuilt.md` in this folder describes the **v3 build**
> (its scene file is `scene-launch-villain-v3.html`). This file is the actual v4 film.
> The easing palette, orthography gate, dev scrubber, and gut-check protocol it defined
> are inherited here, not redefined.

## Prerequisites — hard gates, in order

1. **Audit PLAN executed** (docs match territory, strata separated). Paths below assume
   the post-audit tree; if the audit moved `output_*.html` out of `templates/scenes/`,
   nothing here breaks — v4 only references source files.
2. **Expansion Phase 0** (vendor/) and **Phase 1** (expensive pass) landed.
3. **Expansion Phase 2 particle spike PASSED** (`spikes/particle-spike/`, double-export,
   identical hashes). If the spike fails, v4 ships without particles — every particle
   call below is additive and removable; the story does not depend on them.
4. v3 round-2 fixes applied (this plan builds on the post-fix timeline).

## Files in play

- `templates/scenes/scene-launch-villain-v4.html` + `.css` — copy of post-fix v3 pair
- `templates/motion-lib.js` — gains `particleField`, `drawParticles`, `landWith`,
  `weightShift` (from expansion Phase 1–2) if not already extracted
- `motion/specs/voiceover_launch_villain_v4.json`, `sounds_launch_villain_v4.json`
- `export-video/golden/scene-launch-villain-v4.json` — new golden set

## The two devices that carry the film

1. **The notification is a character.** It appears three times: as the wound (×3 identical
   rejections — proof a bot wrote them), absent through the middle (the silence), and as
   the callback (one human invitation). Same DOM component all three times. The audience
   learns the symbol, then we turn it over — same trick as red scan → lime scan.
2. **Motion as characterization** (inherited): filter = `mech`/`verdict`, human/WorqAI =
   `luxe`/`settle`. New additions: `worq-breathe` (CustomWiggle micro-oscillation) for the
   held beat, weight-shift typography for the reversal line.

---

## Scene 1 — The Proof (0.0 – 9.0s) — REBUILT

**Intention:** v3 *told* the viewer a bot rejected them; v4 *proves* it in 3 seconds, before
a single line of persuasion. Three rejections, word-for-word identical, from three
different companies. Nobody who sees that needs to be told no human wrote it.
The wound stops being a claim and becomes evidence.

**Fixes the v3 contradiction:** v3's single notification came from "Reclutadora Tech" — a
human sender disproving the no-human thesis three seconds before we state it. v4's senders
are company accounts, and the *identical template text* is the indictment.

Beats (all Spanish copy below is final and diacritic-complete — the orthography gate
applies):

- `0.0` — bg grid + glow bloom (brand frame, unchanged). **`ambient-dust` particle field
  on, opacity 0.25** — depth behind everything. **Corner wordmark on from frame 0**
  (see Persistent Watermark below).
- `0.4` — notif 1 slides in (`mech`): **Talento Humano — Grupo Andino** ·
  *"Gracias por tu postulación. Hemos decidido continuar con otros candidatos."*
  SFX: buzz.
- `1.2` — notif 2 stacks under it: **Reclutamiento — TecnoSur** · *identical text,
  word for word.* SFX: **the same buzz, identical sample.**
- `1.8` — notif 3 stacks: **RRHH — Logística MX** · *identical text.* Same buzz.
  The stack sits ~0.8s. Three companies, one paragraph.
- `2.8` — line 1 reveals over the stack (SplitText word-mask, `luxe`):
  **"Tres empresas. El mismo copy-paste."**
- `4.0` — line 2, smaller: **"Nadie lo escribió. Nadie te leyó."** *(the gut punch — hold ~0.9s)*
- `5.2` — notifs mask-close (`mech` — the filter's world taking them away); line 3 reveals,
  muted: **"Y tú empezaste a creer que el problema eras tú."** — "tú" arrives last,
  longer duration (inherited beat).
- `6.4` — lines 1–2 mask-close; `morphSection` on line 3 → **"No eres tú."** lime —
  **and `weightShift` 500 → 900 over 0.5s as it turns.** The line physically gains weight
  as it becomes true. This is the film's signature frame.
- `7.2` — line 4 reveals under it: **"Es el filtro."**
- `7.6` — line 5, smaller, muted — **the restored line, hardened:**
  **"Un robot te descartó antes de que un humano te leyera."**
- `8.6` — designed exit: masks close (`mech`), dust dims to 0.15.

Primitives: notif component (cloned ×3 — exists), SplitText masks, morphSection,
`weightShift` (new, Phase 1), `ambient-dust` (new, Phase 2). Vignette at base 0.06.

## Scene 2 — Meet the Villain (9.0 – 16.5s)

Structurally the post-fix v3 scene (card wipe, red position-driven bleed, ring drains to
23 in `mech`, RECHAZADO `verdict` stamp + 2-frame card impact, flags, button, long hold
on the 23). Expensive-layer additions only:

- **Red `scan-sparks`** emitted along the bar as it sweeps — the filter *shredding*,
  sparse (≤20 live particles), dark red, falling. The lime sparks later will answer them.
- **Chromatic aberration pulse** (0→2px→0, 100ms) on the stamp impact frame.
- **Vignette deepens** 0.06 → 0.12 across the scene — quiet pressure (tweened, Lock 3).
- Camera push 1.000 → 1.020 (inherited from the v3 plan if not already in).

Copy: four flags kept verbatim; the weakest ("no coincidió con la vacante" — bureaucratic,
no blood) is **replaced** with:
**"descartado en menos de un segundo"**
— the cruelest *true* fact about ATS screening. Speed is the insult.

## Scene 3 — The Cheat Code (16.5 – 21.0s) — copy REPLACED, first brand moment

Overlay + reset-under-cover mechanics unchanged. **New copy** (truth → rule → tool;
lines 1–2 stay brandless intel, the brand signs only the speed — its first on-screen
appearance, in its own color):

1. **"Los que consiguen entrevista no son mejores que tú."**
2. **"Solo conocen las reglas: un CV por vacante."**
3. **"WorqAI lo hace en segundos."** *(lime — the brand enters in the film's
   good-guy color, priming the lime button two seconds later)*

Additions: `ambient-dust` behind the text at 0.3 (the overlay is otherwise dead space),
and the overlay lift pairs with vignette easing back to 0.06 — the pressure releasing.

## Scenes 4–6 — The Three Tailors (21.0 – 39.5s)

Post-fix v3 mechanics preserved exactly (position-driven lime morphs under the bar, slow/
fast/fast+break pacing, two-stage 68→93 hesitation). Expensive-layer additions:

- **Lime `scan-sparks`** along the bar in all three tailors — the rewrite throws light.
  Answer to Scene 2's red sparks; same emitter, opposite color. (The villain device,
  third instance.)
- **`score-burst`** (one-shot radial, 120–180 lime particles) exactly on the 92 landing in
  Tailor 1 — *only* Tailor 1. Tailors 2–3 land with `settle` alone; repetition would
  cheapen it.
- **The hesitation gets `worq-breathe`:** during the 0.4s held beat at 68, the ring gets a
  CustomWiggle micro-oscillation (±1.5%) — it visibly *trembles* while it thinks. VO and
  SFX drop out (inherited). Then the spring to 93 (`settle`) and the post-break micro-copy
  "incluso sin perfil técnico." (inherited).
- Cursor moves on MotionPath arcs with the 2-frame pre-click hover (Phase 1e) — applies
  to all three `cursorPress` calls via motion-lib, no per-scene work.

## Scene 7 — Fan-out (39.5 – 44.0s) — caption ADVANCES, stat gets a source

- Ghost-card fan-out unchanged. `ambient-dust` up to 0.3 behind the fan (depth).
- **Caption replaced** (v3's repeated the Scene 3 sentiment):
  **"Misma experiencia. Tres entrevistas posibles."**
  Shorter, stranger, says what the superposition image says.
- Stat banner kept: "x10.6 más entrevistas. Solo por adaptar el CV a la vacante."
  **Add the source line, small, under it** (calibrator condition — the claim needs its
  anchor on screen): e.g. "— estudio interno sobre postulaciones, 2025" or the real
  citable source. **If no citable source exists, the stat comes OFF the screen** and the
  caption carries the scene. Verify with Cesar before build; do not ship an unanchored
  number.

## Scene 8 — The Callback (44.0 – 48.0s) — NEW. The missing beat.

**Intention:** the film opened with the phone delivering three identical rejections.
It closes with the phone buzzing once — differently. The loop the wound opened, closed
by the same device. This is the emotional payoff the viewer has been owed since second 1,
and it lands *before* the brand card so the feeling belongs to the person, not the logo.

- `44.0` — demo dims to ghost (opacity 0.22, inherited Fix-5 behavior), dust at 0.2.
- `44.4` — **one notification slides in** — same component as Scene 1, lime-edged accent
  instead of neutral: **Coordinación RH — Laboratorio Vitae** ·
  *"Hola Andrés, tu perfil nos interesó. ¿Puedes el jueves a las 10?"*
  SFX: **a different buzz** — warmer, single, lower pitch. The sound says it before the
  text does.
- `45.6` — held. No copy competes. One full second of just the invitation over the ghosted
  tailored CV.
- `46.2` — the two human lines slide up beneath it — **rewritten to close Scene 1's
  self-worth wound explicitly:**
  **"Tú no cambiaste. Siempre fuiste suficiente."**
  `47.0` — lime: **"Solo dejaste de ser invisible."**
  *(declarative past — lands ~4s before the CTA's imperative "Deja de ser invisible.";
  the viewer hears the statement, then receives the command. That echo is the hook.)*
- `47.8` — notif + lines exit (`luxe` — the human world's exit, not the filter's).

**Honesty lock, applied:** the callback is one invitation, not a guarantee. The copy is an
interview *question*, never "conseguiste el trabajo." It dramatizes exactly what the
on-screen x10.6 stat already claims (more interviews) — nothing beyond it. No line
anywhere says "te van a leer." The Scene 7 caption frames this as what *los que sí* do.

## Scene 9 — CTA (48.0 – 51.5s)

Post-fix v3 CTA structure (headline / promise / subline / button / domain) with:

- **Headline replaced** — v3's "Tu CV, hecho para pasar el filtro." describes the product;
  the new headline closes the film's own sentence:
  **"Deja de ser invisible."**
  Four words, imperative, and it's the film's own vocabulary — Scene 8 just said
  "Solo dejó de ser invisible para el filtro," so the CTA lands as the answer to the
  whole story, not a slogan bolted on. The promise line beneath it
  ("Adapta tu CV a cada vacante en segundos.") keeps the concrete what-it-does.
  *(Alternates if the gut-check rejects it: "Que el filtro no decida por ti." /
  "El filtro ya no decide.")*
- **`ember-rise`** particles behind the logo, opacity ≤0.3, warm — the only warm-toned
  particle preset, reserved for the brand.
- **Headline `weightShift`** 600 → 800 on arrival — the same typographic gesture as
  "No eres tú." now in the brand's voice. Bookends. (Short headline = bigger type;
  re-check safe zones — Lock 6 will FAIL an overflow.)
- **Origin micro-line (CONDITIONAL)** — small, muted, under the domain line:
  **"Hecho por gente que también fue rechazada por un filtro."**
  Nine words that move this from "another AI startup" to "born from the injustice."
  **Calibrator's hard condition: ships ONLY if literally true of the founders.** If it's
  embellishment, it's exactly the bullshit this audience smells instantly and it poisons
  every line above it. Kenneth/Cesar confirm before build; if not confirmed, the line
  does not exist.
- **The corner watermark travels** — the persistent wordmark animates from its corner
  position into the CTA wordmark slot (MotionPath + scale, `luxe`, ~0.6s). The mark that
  watched the whole film steps forward. Detail nobody consciously notices and everybody
  feels.

## Persistent Watermark (frame 0 → Scene 9)

Small `worqai` wordmark, top-left, inside safe zones, opacity 0.4, static (no animation
until its Scene 9 travel). Solves paid-social attribution (most viewers never reach 0:18)
without branding the wound — presence, not interruption. It is **on from frame 0** and
its `data-copy` attribute feeds the safe-zone check.

---

## Voiceover v4 (one continuous take — split by labels, ElevenLabs settings unchanged, "Workái")

```
Tres empresas. El mismo copy-paste. Nadie lo escribió. Nadie te leyó. No eres tú.
Es un filtro que te descarta antes de que un humano te lea. Hoy tu puntuación es
veintitrés sobre cien: el filtro no encontró las palabras que pide la vacante. Los que
consiguen entrevista no son mejores que tú. Solo conocen las reglas: un CV por vacante.
Workái lo hace en segundos. Workái lee la vacante y reescribe cada línea con tus logros
reales. De veintitrés a noventa y dos.
Otra vacante, otro CV, en segundos. Y hasta para un puesto que no es técnico...
noventa y tres. Misma experiencia. Tres entrevistas posibles. Y un día, el teléfono suena
distinto. Tú no cambiaste. Siempre fuiste suficiente. Solo dejaste de ser invisible.
Sube tu CV y descubre tu puntuación. Gratis, en workái punto io.
```

| # | Label | ~Time | Line |
|---|---|---|---|
| 1 | `proof` | 0.6 | Tres empresas. El mismo copy-paste. Nadie lo escribió. Nadie te leyó. |
| 2 | `wound_turn` | 6.0 | No eres tú. Es un filtro que te descarta antes de que un humano te lea. |
| 3 | `score_low` | 12.0 | Hoy tu puntuación es veintitrés sobre cien: el filtro no encontró las palabras que pide la vacante. |
| 4 | `cheat_code` | 16.9 | Los que consiguen entrevista no son mejores que tú. Solo conocen las reglas: un CV por vacante. Workái lo hace en segundos. |
| 5 | `tailor1` | 22.5 | Workái lee la vacante y reescribe cada línea con tus logros reales. De veintitrés a noventa y dos. |
| 6 | `tailor2` | 30.5 | Otra vacante, otro CV, en segundos. |
| 7 | `tailor3` | 36.0 | Y hasta para un puesto que no es técnico... (hold) noventa y tres. |
| 8 | `fanout` | 40.0 | Misma experiencia. Tres entrevistas posibles. |
| 9 | `callback` | 44.4 | Y un día, el teléfono suena distinto. |
| 10 | `human_close` | 46.2 | Tú no cambiaste. Siempre fuiste suficiente. Solo dejaste de ser invisible. |
| 11 | `cta` | 48.3 | Sube tu CV y descubre tu puntuación. Gratis, en workái punto io. |

**Paste test:** "Nadie lo escribió," "Misma experiencia. Tres entrevistas posibles," and
"el teléfono suena distinto" cannot run on Jobscan/Teal/Rezi unchanged. Lane held.

## SFX map (additions to the inherited spec)

| Beat | Sound |
|---|---|
| Notifs ×3 (Scene 1) | **identical buzz sample ×3** — the repetition IS the sound design |
| Stamp impact | low thud + the aberration pulse frame |
| Lime scans | faint shimmer under the spark emission (≤ -30dB, texture not event) |
| Hesitation at 68 | full silence (inherited) — also duck the music bed |
| Callback buzz | one warm, lower-pitched buzz — must be audibly different from Scene 1's |
| Score burst (Tailor 1 only) | soft pop, no whoosh |

## Build order

1. Copy post-fix v3 pair → v4 pair; port onto motion-lib if extraction landed.
2. Scene 1 rebuild (the proof stack) — **gate scene.** Draft-export 0–9s, contact sheet.
3. Scene 8 callback (notif component reuse + new copy + timing).
4. Scene 7 caption/stat-source swap. Scene 9 watermark travel + embers + weightShift.
5. Particle passes (dust → sparks → burst → embers), each verified on a label-range draft.
6. Post-processing pass (vignette arc, aberration pulses).
7. Full timeline shift verification (`data-duration` → ~52), VO re-record, sounds, captions.

## Verification (the law, unchanged)

1. Orthography preflight — every `data-copy` string (all copy above is pre-accented; the
   gate confirms).
2. Label-frame contact sheet — inspect: identical-text stack legible; "No eres tú."
   weight-shift frame; sparks under both scan colors; the 68 tremble; callback notif in
   safe zone; watermark travel endpoint.
3. Double export → byte-identical. Golden hashes captured
   (`golden_frames.py --write` then `--check --strict`).
4. Full-quality 60fps export + sound pass + caption variant.
5. **Cutdowns from labels:** 6s (proof → stamp → CTA) and 15s (proof → tailor 1 →
   callback → CTA) for paid tests — the callback makes the 15s cut for the first time.

## Calibration — ship as a hypothesis (Calibrator, mandatory, logged)

- **Claim:** the proof-stack open + callback close beat v3 on 3s hook, save-rate, and the
  second-5 exhale.
- **The unrun test comes first.** The v3 brief's 5-person gut-check was never run. Run it
  ONCE with both cuts: v3 as-is vs a v4 animatic (Scene 1 + Scene 8 rough over existing
  footage). Watch: faces at second 5, faces at the callback buzz, and ask afterward who
  the video says is at fault. **If v3's open already produces the exhale and the stack
  doesn't beat it, build only Scene 8 and the expensive pass onto v3 — the full remake
  is optional, the callback is not.**
- **Falsifier:** v4 underperforms v3 on hook or save-rate → the proof-stack open is wrong
  for this audience; keep the callback, revert the open.
- **Stat integrity:** x10.6 ships with a visible source or ships not at all. Cesar owns
  this call and the test data. No retroactive goalposts.
- **Honesty lock holds everywhere:** mechanical filter, no malice, one interview
  *question* dramatized, nothing promised.
