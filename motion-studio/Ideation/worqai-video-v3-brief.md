# WorqAI — Video v3 Brief (scene-launch-villain)

Successor to `video_music_2026-06-08.mp4` (scene-launch-honest). Same format:
**9:16 · 1080×1920 · ~46s · 60fps.** Same pipeline, same scene-file pattern.

> Built with the Collapse Labs swarm + vault. Primary tunnel: **the Filtering Tunnel** —
> the candidate was always qualified; a dumb machine couldn't see them. Indict the filter,
> don't apologize for the candidate.

## Why this exists — the diagnosis v1 fixed

v1 was a flawless **product demo** that was quietly **on the filter's side**: it cataloged
the candidate's deficiencies in red, then sold a fix. v2 is a **story about a person the
system failed.** Five structural changes, each closing a gap in v1:

1. **Open on the wound, not a feature label.** v1 opened on "Un CV para cada vacante" — a
   feature. v2 opens on the pain and the lie (*no soy suficiente*), then cracks it. Target
   one body sensation by second 5: the exhale of "it's not me."
2. **Give it a villain — and indict it, not the candidate.** v1 framed 23/100 as the CV's
   fault. v2 names the antagonist the brand owns — *the filter that rejects you before a
   human reads you* — and shows it. The 23 is the machine's verdict, never the viewer's worth.
3. **Break the third rep.** v1 ran three identical tailor sequences. v2 makes the third one
   hesitate — one held breath in the whole film. That asymmetry is the visible human hand.
4. **Climax on the cheat code, not a paste-test failure.** v1's climax ("Personaliza tu CV
   a cada vacante en segundos") could run for Rezi or Teal unchanged. v2's climax is the
   line a competitor cannot say.
5. **Close on the human, then the logo.** v1 cut from fan-out to brand. v2 lands the
   consequence on the person first — their facts never changed, only their visibility did.

**No new effects required.** Everything reuses primitives proven in
`scene-launch-honest.html`. New constructs are recolors/recombinations only: red scan-bar,
RECHAZADO stamp (badge primitive, red + rotated), two-stage score tween.

---

## The villain device — read this before building

One visual idea carries the whole reframe and uses zero new code:

- **Red scan-bar = the filter rejecting you.** It reads your CV looking for coincidences,
  doesn't find them, stamps RECHAZADO.
- **Lime scan-bar = WorqAI rewriting.** Same sweep primitive, opposite color, opposite
  meaning. The first time the viewer sees lime, it already reads as "the good guy is working."

Same `#scan-bar` element. Red in Scene 2, lime in Scenes 4–6. That contrast is the story.

---

## Scene 1 — The Wound (0.0 – 6.0s)

**Intention:** Don't sell. Open the wound and the self-blame, then crack it. By second 5
the viewer knows: it's not me, it's a machine — and this video is going to expose it.
The whole open exists to manufacture one exhale.

Copy (ES-native, tú register):
- `0.4` slide up — "Mandaste el mismo CV a 40 vacantes." *(the behavior, flat)*
- `1.6` slide up — "Cero respuestas." *(short. let it sit. ~1s of nothing.)*
- `2.7` slide up, muted/smaller — "Y empezaste a creer que el problema eras tú." *(the lie)*
- `4.0` the muted line blurs out, lime line blurs in its place (morphSection on full-screen
  text) — "No eres tú." *(present tense, certain)*
- `4.7` slide up under it — "Es un filtro que te descarta antes de que un humano te lea."
  *(villain named)*
- `5.8` all drift up + fade

Primitives: bg-grid/glow bloom (keep — brand frame), slide-up text, one `morphSection` on
a headline. Nothing new.

## Scene 2 — Meet the Villain (6.0 – 12.0s)

**Intention:** Show the filter doing the damage. The 23 is the machine's verdict, framed as
the system's design — not the candidate's worth. v1's "before state" and "diagnosis"
collapse into one gut-punch here.

- `6.0` demo-group on, `#cv-card` wipes up (clipPath). Banner: "Asi lo ve el filtro:"
- `6.8` bottom panel fades in, ring empty
- `7.4` **red** scan-bar sweeps top→bottom — *the filter reading*
- `8.2` as the scan passes, kw-bad red highlights bleed onto weak words (remove
  `cv-clean-mode`, synced to the sweep — not all at once)
- `9.0` ring fills 0 → 23, grey → red. State label "Bajo" red.
- `9.5` **RECHAZADO stamp** scale-springs in over the card, rotated ≈ -8°, red (badge
  primitive, recolored). The villain's verdict made physical.
- `10.2` three section flags appear fast — keep it to flags, **drop v1's 4-row diagnostic
  panel.** It killed momentum. The stamp carries it.
- `11.2` "Optimizar con WorqAI" lime button fades in
- short hold

**Copy direction — indict the machine, don't apologize for the candidate.** This is the
swarm's core note. v1's flags read as shame ("línea débil" = *your* line is weak). v2's
flags indict the filter: **"el filtro no encontró esto"**, **"invisible para el ATS"**,
**"el bot no lo entendió"**. Same red overlays, opposite emotion.

Primitives: scan-bar (recolored red), kw-bad reveal, score-ring, badge→stamp (recolor +
rotate), section flags. Cut the diagnostic panel.

## Scene 3 — The Cheat Code (12.0 – 16.0s)

**Intention:** The reframe, delivered as **intel, not comfort.** v1 said "you don't need a
better CV" (self-help). v2 says "the people getting interviews already do this"
(competitive intel — the cheat code). Full-screen overlay, two lines, nothing competing.

- `12.0` issues/cursor gone, full-screen overlay up (~97% — CV fully hidden)
- `12.4` slide up — "Los que sí consiguen entrevista no tienen un mejor CV."
- `13.7` slide up, lime — "Tienen uno hecho para cada vacante."
- `14.6` slide up, smaller — "Y lo hacen en segundos." *(bridge to proof)*
- under cover (`15.3`): reset CV to clean, swap banner generic→stat *(existing trick — no
  visible pop-in)*
- `15.6` overlay lifts → clean CV + stat banner revealed in one cut

Primitives: overlay reset-under-cover (already in file), slide-up text, banner swap.

## Scene 4 — Proof 1, slow (16.0 – 25.0s)

**Intention:** The aha. Keep the slow tailor exactly as built — the morph-swap is the
product's real strength and the deliberate pace lets the viewer follow every step. First
appearance of the **lime** scan = the good guy working, the visual answer to Scene 2's red.

- Job chip "Analista de Seguridad" slides in → 1.2s read gap → cursor clicks Optimizar
  (compress + ripple) → **lime** scan sweep → reasoning lines type → 9 morph steps
  (role, resumen, skills, 6 bullets) → score 23 → 92, ring red → lime → "Puntuacion 92" badge
- Content: unchanged from v1 tailor 1.

Primitives: the entire `runTailor("slow")` path, unchanged.

## Scene 5 — Proof 2, fast (25.0 – 31.0s)

**Intention:** Prove range. Different field, different keywords, same clean process. Speed
says "effortless." Keep as built.

- Job chip "Analista de Datos · Reporting" → 0.85s read gap → click → snap morphs → score 94.
- Content: unchanged from v1 tailor 2.

## Scene 6 — Proof 3, BREAK THE RHYTHM (31.0 – 36.5s)

**Intention:** This is the move that breaks v1's monotone. "Coordinador Bilingüe" — the most
different role, human not technical, proving the system adapts to *register*, not just
keywords. And the score **hesitates.**

- Job chip "Coordinador Bilingüe" → fast read gap → click → morphs (fast)
- **The break:** split the score tween. Ring climbs fast to ≈ 68, then a **0.4s held beat** —
  VO drops out, SFX cut, ring dims ~10% — then springs to 93. One breath in the whole video.
- After it lands, micro-beat of copy is allowed (chip area): "incluso sin perfil técnico."

Primitives: `runTailor("fast")` but the single `pScore` tween split into two with a gap
between (trivial — two `fromTo`s instead of one). Everything else identical.

## Scene 7 — Fan-out + Cheat-Code Climax (36.5 – 39.5s)

**Intention:** Visual proof — one person, three targeted CVs — landed under the line a
competitor literally cannot paste onto their own site.

- Verify/optimize/score-info/stat-banner fade out
- Three ghost cards fan out (rotate -6° / +5° / 0°, offset) — as built
- Caption (replaces v1's paste-test failure):
  **"Esto es lo que hacen los que sí consiguen entrevista."** *(emphasis pulse: 1.04 → settle)*
- **Read the fan-out as superposition, not three files.** Three branches of *one* person's
  possibility-space, coexisting — same history, three renders. "One life, observed three
  ways" is why no copy beyond the caption is needed.
- Demo group fades to ~10% to make way for the close

Primitives: ghost-card fan-out, caption scale pulse — unchanged. **Copy only** changed.

## Scene 8 — The Human Consequence (39.5 – 42.5s) — NEW BEAT

**Intention:** Don't cut to the logo. Close the loop opened in Scene 1. The person who
thought they weren't enough now gets seen — and their facts never changed. True to the
product ("tus hechos se quedan tal cual"). The reframe completes here, not at the brand card.

- demo at ~10%, two lines slide up center-screen:
- `39.7` — "Tú no cambiaste. Tu historial tampoco."
- `40.8` lime — "Solo dejó de ser invisible para el filtro."
- `41.9` fade

Primitives: slide-up text over faded demo. Nothing new.

## Scene 9 — CTA (42.5 – 46.0s)

**Intention:** Clean landing. The headline already names the villain — keep it. One action,
one URL.

- `42.5` logo "W" scale-spring → `42.7` wordmark → `42.8` headline
  "Tu CV, hecho para pasar el filtro." (slide+scale) → `43.7` subline
  "Sube tu CV y descubre tu puntuacion. Gratis." → `44.4` CTA button
  "Analiza mi CV gratis" (spring) → `45.0` domain "worqai.io · espanol e ingles"

Primitives: the entire CTA stagger, unchanged.

---

## The arc, side by side

| Phase | v1 (plain) | v2 (villain) |
|---|---|---|
| Open | Feature label, 4 lines | The wound + the lie, then cracked |
| Before | Generic CV appears | The filter scans + stamps RECHAZADO |
| Problem | 23/100 = CV's fault | 23/100 = the machine's verdict |
| Reframe | "You don't need a better CV" (self-help) | "The winners already do this" (intel) |
| Proof | 3 identical wins | 2 wins + 1 that holds its breath |
| Climax | Paste-test-failing caption | The cheat code competitors can't say |
| Close | Cut to logo | Land on the human, then logo |

---

## Voiceover v2 (one continuous take — same split workflow)

Brand pronunciation stays `Workái`. ElevenLabs settings unchanged from v1.

```
Mandaste el mismo CV a cuarenta vacantes y no te llamaron. No eres tú. Es un filtro que te descarta antes de que un humano te lea. Hoy tu puntuacion es veintitres sobre cien: el filtro no encontró las palabras que pide la vacante. Los que sí consiguen entrevista no tienen un mejor CV. Tienen uno para cada vacante. Workái lee la vacante y reescribe cada linea con tus logros reales. De veintitres a noventa y dos. Otra vacante, otro CV, en segundos. Y hasta para un puesto que no es técnico... noventa y tres. Tú no cambiaste, tu historial tampoco. Solo dejó de ser invisible para el filtro. Sube tu CV y descubre tu puntuacion. Gratis, en workái punto io.
```

| # | Label | ~Time | Line |
|---|---|---|---|
| 1 | `wound` | ~0.4s | Mandaste el mismo CV a cuarenta vacantes y no te llamaron. No eres tú. Es un filtro que te descarta antes de que un humano te lea. |
| 2 | `score_low` | ~9.0s | Hoy tu puntuacion es veintitres sobre cien. El filtro no encontró las palabras que pide la vacante. |
| 3 | `cheat_code` | ~12.4s | Los que sí consiguen entrevista no tienen un mejor CV. Tienen uno para cada vacante. |
| 4 | `tailor1` | ~17.5s | Workái lee la vacante y reescribe cada linea con tus logros reales. De veintitres a noventa y dos. |
| 5 | `tailor2` | ~25.5s | Otra vacante, otro CV, en segundos. |
| 6 | `tailor3` | ~33.5s | Y hasta para un puesto que no es técnico... (hold the pause) noventa y tres. |
| 7 | `human_close` | ~39.7s | Tú no cambiaste, tu historial tampoco. Solo dejó de ser invisible para el filtro. |
| 8 | `cta` | ~42.8s | Sube tu CV y descubre tu puntuacion. Gratis, en workái punto io. |

**Paste test on every climax line:** none of "No eres tú / Es un filtro que te descarta",
"Los que sí consiguen entrevista...", or "Esto es lo que hacen los que sí consiguen
entrevista" can run on Jobscan, Teal, or Rezi's site unchanged. They stake the cheat-code
and bot-villain lanes — competitors cannot copy them without changing their product.

---

## Calibration — ship as a hypothesis, not a truth (Calibrator's terms)

v2 is a bet that the "villain/manifesto" frame beats the clean demo. It is *not* proven.
The vault rule applies: a glitch you cannot verify is a daydream; surety brings ruin.

- **Claim:** the Filtering-Tunnel cut produces higher saves/shares/CTR than v1 with tired
  LATAM job seekers.
- **Falsifier:** if v2 underperforms v1 on save-rate or 3-sec retention in an A/B (or in a
  5-person gut-check from the warm Reddit list), the manifesto theory is wrong *for this
  audience* — revert to the demo frame.
- **Cheapest test first:** before a full re-render, show v1 and a rough v2 animatic (even
  just new Scene 1 + Scene 2 copy over existing footage) to 5 real job seekers. Watch their
  faces at second 5. The exhale is the signal. No exhale → the open failed.
- **Cesar owns the call on the data.** This is the skeptic node's domain, not a taste vote.
- **Honesty lock:** the filter is mechanical, not malicious. No line implies the ATS is
  "evil," and nothing promises "te van a leer." Indict the mechanism, not with a lie.
