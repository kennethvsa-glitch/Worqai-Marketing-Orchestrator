# Villain-v3 → Visual Redesign Plan (mockup-driven)

**For a lower model (Sonnet) to execute. Plan only — do not build until the gates below pass.**

Goal: build a **whole new video** from the remade scene mockups so it reads as "expensive" the way
the Scene 9 CTA does. This is **not** an edit or fork of v3 — **v3 stays untouched** as the old
version. The new video reuses the proven mechanics and primitives (`motion-lib.js`, the CTA block)
but as a **fresh composition** driven by the new design system.

---

## 0. Read this first — what changed and why

The previous round (`villain-v3-animation-uplift-plan.md`) added post-processing **seasoning**
(vignette, bloom, chromatic aberration, breathing) on top of the *same plain layouts*. Result:
the only visible change in the whole render was the Scene 3 lime underline. Proof that **polish is
invisible; composition is what reads.** The CTA feels premium because of *structure + a design
system + hero objects* — not post-FX.

So this is a **redesign, not a tweak.** It supersedes the "copy/structure stays byte-for-byte"
constraint of the uplift plan. Copy and layout WILL change. The uplift plan's post-FX layer
(vignette/bloom/particles/CA) is now applied **last, as seasoning** over the new compositions —
not as the main event.

## Source of truth & how to use it

- **Images:** `motion-studio/Ideation/Escenes remake/*.png` (already copied into this workspace)
- **Spec MD:** same folder, `SCenes remake specs.md`
- These are **ChatGPT image-gen mockups + a post-hoc CSS rationalization.** Treat them as
  **mood / composition / palette targets — NOT pixel specs.** Do not reproduce AI artifacts,
  garbled text, or impossible/edge-overflowing measurements. The real source of truth is:
  (1) the design system extracted below, (2) what renders **deterministically**, (3) what
  **reads on a 1080×1920 phone** within each scene's time budget.

---

## 1. Phase 0 — Design System extraction (do ONCE, before any scene)

The mockups are all built from the same handful of primitives. Build that shared layer first;
every scene composes from it. Put shared CSS in `templates/scenes/redesign-system.css` and shared
builders by extending `templates/motion-lib.js`.

### Tokens
- **Navy base:** `#02060C` → `#0B0F14` (gradients, never flat fill).
- **Lime accent:** `#C8F22A` / `#C9FF27` (warm/resolution), glow `rgba(200,242,42,0.2)`.
- **Villain red:** `#FF453A` / `#D8463D` (Scene 2 only).
- **Inks:** white `#F2F2F2`, muted `rgba(255,255,255,0.5)`.
- **Radii:** 16–40px. **Glow recipe:** layered `box-shadow` (never harsh; opacity ≤ 0.25).

### Fonts — DECISION (flag for sign-off)
Standardize hero/UI type on **Inter** (already vendored: `Inter-300..600` + `InterVariable`).
The mockups read as Inter. Moving heroes to **InterVariable** also unlocks real animated weight —
which makes the `weightShift` move from the prior plan finally work (it was a no-op on static
Archivo). Keep `JetBrains Mono` for code/mono UI bits. ⚠️ This changes the typeface of the whole
video — confirm before committing.

### Reusable primitives (each must be determinism-safe — see §2)
`grid-bg`, `wave-lines` (SVG paths), `glass-panel` (FAKE glass — §2), `corner-marks` (SVG L's),
`radar` (SVG, GSAP-rotated), `score-gauge` (SVG ring — reuse `makeScoreRing` pattern),
`keyword-pill` (red + lime variants), `skill-pill`, `section-label` (dot + caps),
`flow-line` (SVG `draw()`), `node-card`, `particle-layer` (reuse `particleField`).

---

## 2. Determinism spike + guardrails (BLOCKING)

- **`backdrop-filter: blur()` is the risk.** GPU compositing under the headless seek loop may not
  be hash-stable and is slow. **DEFAULT: do not use it.** Fake glass = solid `rgba(8,14,22,0.85)`
  fill + 1px border + inner/outer `box-shadow` glow. Over a dark bg it's visually identical.
  - If true glass is wanted anyway: run the Phase-4-style spike (render one glass panel twice,
    compare `sha256`; SwiftShader fallback per `motion-determinism.md` Phase 4). **PASS before use.**
- **All continuous loops** (radar 20s rotation, breathing glow, scan beam) = **GSAP `repeat:-1`
  tweens, never CSS animation** (Lock 3/7). `repeat:-1` is excluded from the duration preflight
  (Lock 9) — but **scope/kill each loop at its scene boundary** so it doesn't bleed (e.g. the
  villain radar must stop before the warm scenes; the Scene 8 bloom must die at the CTA cut).
- **Seed all randomness** (particles, grain) keyed to a per-scene seed (Lock 8/10).
- **Grain/noise** = a static seeded texture, never animated `Math.random()`.
- **Safe zones:** decorative chrome (corner marks, edge panels, radar) MAY bleed to edges, but any
  `[data-copy]` text MUST stay within top 120 / bottom 200 / x 56 or the exporter FAILS (Lock 6).
  The tailor card is near-full-bleed — verify its text content explicitly.
- **No CDN refs** — vendor everything (Lock: vendor-only).

---

## 3. Per-scene build specs

Each scene keeps its existing time budget and its place in the **intensity/temperature arc** (the
CTA is still the only 5; Scene 2 is high-intensity but cold/zero-life). Map every animation to an
**existing motion-lib primitive** before writing anything new.

### Scene 1 — Wound · intensity 2 · cold-with-sparks
**Image:** `Scene 1.png` + `Scene 1 second part.png`. This mockup *answers Kenneth's note* ("too
empty, no eye-catch, needs a descending line like the CTA"): grid bg + a glowing green node with a
**vertical line drawing downward** (left) + flowing lime wave-lines + drifting lime particles +
lime accents on the periods and the `?` badge.
- **Compose:** big white `40 postulaciones.` / `0 respuestas.` (lime periods); question line with
  lime `?` badge. Left: green node + descending draw-line. Lower third: wave-lines + particles.
  Faint grid + slow radial glow.
- **Second part:** same bg persists (no cut) — text swaps to `Nada.` (lime hero) /
  `Nadie te rechazó.` / `Nadie te leyó.` (lime) / kicker.
- **Animate:** grid fade + glow breathe (`repeat:-1`, slow); node line `draw()`; waves slow drift
  (`repeat:-1`); particles rise (`particleField`, seed `v3-s1`); text `blurInChars` stagger;
  `Nada.` scale-lift + lime turn.
- **Note:** Kenneth said "no lime on scene 1" — the mockup intentionally adds minimal lime sparks.
  Keep them *minimal* so the scene stays cold but no longer dead. This is the eye-catch fix.

### Scene 2 — Villain · intensity 4 · coldest/red · life 0 (frozen)
**Image:** `SCene 2.png`. Red ATS HUD: header `ASÍ TE LEE EL FILTRO` + warning icon, `RECHAZADO`
panel top-right, white CV card with **red** keyword pills, rotated `DESCARTADO` stamp, bottom panel
with red radar + score gauge `23 BAJO`.
- **Reuse current mechanics, re-skinned red:** existing `stamp()`, `scanSweep()` (red),
  `makeScoreRing` (red, 23). Radar = GSAP `repeat:-1` rotation that **stops at scene end.**
- **Keep from uplift plan:** `caFlash` on stamp impact + sustained vignette (raw `tl.to`, held).
- The only motion is mechanical (scan, radar) — **no warm "life," no `back.out`/settle.**

### Scene 3 — Turn · intensity 3 · warming
**Image:** `Scene 3.png`. Framed (rounded-rect border + corner marks), target icon top-left, white
headline → lime headline, check row with **hand-drawn lime underline** (this is the "line under the
text" Kenneth already saw — keep & elevate it).
- **Animate:** frame scale-in; corner marks `draw()`; target icon layers in (ring → crosshair →
  person) + pulse; headlines `blurInChars` line-by-line; underline `draw()`; first bloom pulse +
  vignette release (uplift plan) = first warmth.

### Scenes 4–6 — Tailors · intensity 3→4 · warm/lime rising
**Image (visuals):** `Scne(4-6)tailors.png`. **Component set:** Kenneth's pasted dark-glass spec.
**Rule from Kenneth:** "use those components but keep the visuals of the original; all 3 tailors
look like the remade image." → **ONE canonical tailor card, reused for all three** (vary only job
title, keywords, and score 92/94/93).
- **REDUCE the component set (Kenneth keeps saying overcharged — cut hard).**
  - **KEEP:** header w/ score badge · candidate header · 2 sections with keyword highlights
    (RESUMEN, EXPERIENCIA) · skills pills · the lime scan beam · bottom score-gauge · CTA button.
  - **CUT:** the 5 match-bars "optimization panel," the duplicate radar, the dot-matrix. They
    don't read in ~6s and they fight the scan story. ⚠️ This cut is my recommendation — adjust.
- **Visual style:** the original light-card look + lime accents on the deep-navy environment.
- **CRITICAL — this is the morph END-STATE, not a static card.** The card transforms from Scene 2's
  red rejected version → this optimized version as the lime scan beam passes. Reuse `scanSweep` +
  `morphSection`/`morphSkills` + `makeScoreRing`: keywords red→lime, score climbs. Tailor-3 keeps
  the hesitation beat (`worq-breathe`). Bloom pulse on each score land.
- Scan beam is driven by the timeline per cycle (not a free-running `repeat:-1`).

### Scene 7 — Fan-out · intensity 4
**Component image:** `esto es lo quehacen los que si cosniguen entervista .png` (success banner).
- Ghost-card fan now fans the **new dashboard cards** (reuse `fanOut`). Caption = the success-
  banner component: dark-glass pill, lime circle-check that **draws itself** (circle then tick),
  `sí` in lime, blur-in. Calm, not celebratory.

### Scene 8 — Human · intensity 3→4 · warmest pre-climax
**Image:** `Scne_8.png`. Fixes Kenneth's "too plain / text too close" note via a **right-side
vertical flow diagram**: building → robot → ✗-node → profile card → WORQAI checklist panel,
connected by a drawn lime flow-line. That's the missing visual interest.
- **Left:** the 4 manifesto lines (white + lime alternating). **Fix line-spacing** — increase
  leading; current is too tight. Heroes → Inter.
- **Animate:** flow-line `draw()`; nodes pop in top→bottom (`back.out`); WORQAI checklist checks
  `draw()`; left lines `blurInChars` varied cadence; one breathing bloom — **killed at the CTA cut**
  (per the uplift-plan fix).

### Scene 9 — CTA · port over unchanged (the reference)
Copy the existing CTA block from `scene-launch-villain-v3.html` into the new video as-is — it's the
proven reference ending. Just confirm the new tokens match it (lime-on-dark, particles, draws) so
the video reads as ONE piece and the CTA still feels like the peak.

---

## 3B. Animation choreography (beat-timed) — the layer that prevents static output

> "Map to primitives" is the altitude that produced the invisible last round. This section pins the
> **timing** so the executor hand-authors an absolute-timed timeline like the CTA block does — not a
> slideshow of fades. Times are **scene-relative offsets** (`sN + x`), the same pattern as the CTA's
> `ctaT + x`. They are **cadence guidance, matched to the CTA's feel — not gospel**; adjust to the
> real scene durations. Every scene must have all three: an **entry sequence**, **one continuous-life
> element that never stops**, and a **hero gesture**. Each `repeat:-1` loop is **scoped and killed at
> its scene boundary** (Lock 9 excludes it from the duration check; bleed is the bug).

**The cadence rule (from the CTA):** beats land ~0.3–0.6s apart, eases *vary* (draw = `power2.inOut`,
pop = `back.out`, settle = `settle`/`worq-settle`, villain = `mech`/`verdict`), and *something is
always moving* (a draw in progress, a breathe, a drift). Never two identical fades back-to-back.

### Scene 1 — Wound  (life: 3 ambient loops · hero: descending node-line + "Nada." turn)
```
s1+0.0  grid              opacity 0→1            0.6   power2.out
s1+0.0  radial glow       breathe scale1→1.03    6.0   sine.inOut   repeat:-1 yoyo   [LIFE]
s1+0.2  node line         draw() downward        1.2   power2.inOut                  [HERO build]
s1+0.3  wave-lines        drift x 0→-40          12.0  sine.inOut   repeat:-1 yoyo   [LIFE]
s1+0.4  particles         rise (seed v3-s1,~40)  10.0  (particleField, lime ≤0.2)    [LIFE]
s1+0.6  "40 postulaciones" blurInChars           0.6   power3.out
s1+1.3  "0 respuestas"     blurInChars           0.6   power3.out
s1+2.2  question + "?" badge blurIn + scale-in   0.5   back.out
s1+4.4  text A out         opacity→0,y-12,blur6  0.5   power2.in
s1+5.0  "Nada."            blurInChars + scale1→1.04 + lime   0.6   settle           [HERO turn]
s1+5.9  "Nadie te rechazó" blurInChars           0.5   power3.out
s1+6.6  "Nadie te leyó"    blurInChars (lime)    0.5   power3.out
s1+7.6  kicker             blurIn + vignetteUp pulse on land
s1+end  KILL glow/wave/particle loops at Scene 2 start
```

### Scene 2 — Villain  (life: radar only, cold · hero: DESCARTADO stamp + CA flash)
```
s2+0.0  cut to villain bg; header glass  y20→0,op0→1   0.8   power3.out
s2+0.3  RECHAZADO panel   slide from right + blur       0.6   power3.out   (NO bounce)
s2+0.5  CV card           scale .96→1, op0→1            1.1   expo.out
s2+0.5  red radar         rotate 360                    20.0  linear  repeat:-1   [LIFE-cold]
s2+1.4  red scan beam      sweep top→bottom             0.9   mech    → red keyword pills fade in
s2+1.4  score gauge        0→23                         0.9   mech    (red)
s2+2.6  warning flags      6× sequential                0.28 ea  power3.out
s2+3.6  DESCARTADO stamp   scale1.15→1, rot-12→-15      0.25  verdict                [HERO]
s2+3.6  caFlash(2) on impact frame  +  vignette → 0.18 SUSTAINED (raw tl.to, held)
s2+end  KILL radar + begin vignette release before Scene 3
```

### Scene 3 — Turn  (life: target pulse + bg breathe · hero: underline draw + target assembling)
```
s3+0.0  frame             scale .98→1, op0→1           1.2   expo.out
s3+0.3  corner marks      draw() ×4 staggered          0.5   power3.out             [HERO build]
s3+0.5  target icon       ring→crosshair→person (0.3 ea) then glow pulse
s3+0.5  target pulse      scale1→1.03 every 3s         sine.inOut  repeat:-1         [LIFE]
s3+1.0  white headline    blurInChars line-by-line     stagger 0.15  power4.out
s3+2.0  green headline    blurInChars (stronger+glow)  expo.out
s3+2.8  check row         blur 12→0                    0.7
s3+3.2  lime underline    draw()                       0.6   power1.out             [HERO]
s3+3.6  bloom pulse fires + vignette fully releases  (first warmth)
s3+end  KILL target pulse at Scene 4 start
```

### Scenes 4–6 — Tailors  (per cycle t; life: card-glow breathe + scan motion · hero: live morph)
```
t+0.0  job chip          landWith x28→0 + bounce       0.55  worq-settle
t+0.0  card border glow  breathe                       4.0   sine.inOut  repeat:-1  [LIFE]
t+0.3  cursor            cursorPress on "Optimizar" + ripple
t+0.6  lime scan beam    sweep down                    1.2   (scanSweep, timeline-driven)
t+0.6  →as beam crosses: reasoning lines stagger in; morphSection rewrites sections;
        red pills → lime pills; keyword highlights fade 0→1 (0.2 ea) behind the beam   [HERO morph]
t+1.8  score gauge       climb (makeScoreRing):
        T1 23→92 slow (settle, teach) | T2 92→94 fast | T3 94→68 dim held 0.4s (worq-breathe) →68→93 settle
t+score bloom pulse + ring center scale 1→1.05→1
t+end  "Puntuación 9X" chip pop (back.out 2) then fade;  KILL card-glow at sequence end
```

### Scene 7 — Fan-out  (life: brief · hero: fan + self-drawing check)
```
s7+0.0  ghost cards       fanOut (x/y/rot/scale/op staggered)   0.38  power3.out     [HERO]
s7+0.1  bloom burst as cards spread
s7+0.2  lime particles    rise from behind stack (short, ~2.5s)
s7+0.5  banner container  fade + y20→0                 0.7   power3.out
s7+0.5  circle-check      draw() circle 0.4 → tick 0.25 (delay 0.2)  power2.out      [HERO]
s7+0.9  "sí"              blur6→0 + scale .95→1        0.4   power4.out  (appears last)
s7+1.0  demo-group        scale .97 + fade (handoff to Scene 8)
```

### Scene 8 — Human  (life: breathing bloom + X-node pulse · hero: flow-line draw + line4)
```
s8+0.5  flow-line (right) draw() top→bottom           1.4   power2.inOut             [HERO build]
s8+0.2  line1 (white)     blurInChars                 0.5   luxe
s8+1.0  line2 (lime)      blurInChars                 0.45  settle
s8+1.0  building node     pop scale .8→1              0.4   back.out
s8+1.5  robot node        pop                          0.4   back.out
s8+1.8  line3 (white)     blurInChars                 0.5   luxe
s8+2.0  X-node            pop + pulse glow             sine.inOut  repeat:-1         [LIFE]
s8+2.5  profile card      fade + blur in               0.6
s8+2.7  line4 HERO (lime) held air → blurInChars + scale1→1.05   0.6   settle       [HERO]
s8+3.0  WORQAI panel      fade in; checklist checks draw() ×3 sequential
s8+3.0  breathing bloom   behind stack                 2.2   sine.inOut  repeat:-1   [LIFE]
s8+CTA  KILL breathing bloom at the CTA cut (tl.to op 0, 0.4)
```

### Scene 9 — CTA  (the cadence reference — already built)
`ctaT+0.1` trail draw 1.4 · `+0.2` particles + logo · `+0.7` badge settle · `+1.1` subtext ·
`+1.3` star pop back.out(2) · `+1.5` headline · `+1.8` star twinkle repeat:-1 · `+2.1` underline
draw · `+2.6` desc · `+3.1` button back.out · `+3.7` features · `+4.2` domain. **This is the feel
every scene above is calibrated against.**

---

## 4. Open decisions (defaults set — confirm or override)

- **Fonts:** default = move heroes/UI to Inter / InterVariable. (Unlocks weight animation.)
- **Copy:** the mockups add new labels (`10.6x más entrevistas`, `Análisis de Seguridad`,
  `ESCANEANDO CV...`). Default = **keep the current narrative/voiceover copy as canonical**; adopt
  mockup labels only as UI chrome where they don't fight the script. (Copy was carefully rewritten
  in prior sessions.)
- **Glass:** default = fake glass (no live `backdrop-filter`).
- **File:** **whole new video** (Kenneth's call) — build a fresh scene template, e.g.
  `templates/scenes/scene-launch-villain-v5.html` + film `films/launch-villain-v5.json` + its own
  fresh golden baseline. **Do not touch v3** (it stays as the old version). Reuse `motion-lib.js`
  and port the CTA block over unchanged. (`v5` is a placeholder name — rename to taste; v4 exists.)

---

## 5. Staging (so a lower model executes safely)

1. **Phase 0** system + determinism spike (glass). **Gate: spike PASS.**
2. **PILOT the Tailor card first** — it's the hardest (a morph), the most reused, and the biggest
   "expensive" payoff. Build one cycle, render it, contact-sheet vs the mockup.
   **Gate:** reads on a phone in ~6s · deterministic (golden frames stable) · looks expensive ·
   does NOT out-shout the CTA.
3. If the pilot holds → build Scenes 1/2/3 (they share bg + chrome), then 7 + 8. **CTA untouched.**
4. Full re-render → generate the golden baseline for the **new video** (v3's baseline stays as-is).

## 6. Ship as a hypothesis

**Falsifier — this is worse if:**
1. Glass/glow tanks render determinism or perf (golden frames won't stabilize, or render time blows up).
2. The dashboard still can't be read in ~6s on a phone (overcharge not actually solved).
3. The redesign looks great as stills but the **morph breaks** because the new card is too complex
   to animate from the red rejected state.
4. It stops feeling like ONE video (new scenes drift from the CTA's look).

**Cheapest test first:** the Tailor pilot, one cycle, before anything else is touched.

## 7. Determinism + safe-zone checklist (run per scene before commit)
- [ ] No live `backdrop-filter` (or spike PASSED)
- [ ] Every continuous loop is GSAP `repeat:-1`, scoped/killed at its scene boundary
- [ ] All randomness seeded to a per-scene seed
- [ ] Grain/noise is a static texture, not animated random
- [ ] All `[data-copy]` text inside safe zones (exporter FAIL otherwise)
- [ ] No CSS `@keyframes`/SMIL running in video mode (Lock 7)
- [ ] New effects are pure functions of `(t, seed)` (Lock 10)
- [ ] Vendor-only assets, no CDN
