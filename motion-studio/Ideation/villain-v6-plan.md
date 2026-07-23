# WorqAI Launch Video — v6 Plan (rev 2: green-world rebuild)

**Plan only. Do not build until the Scene-1 decoration pilot gate (§9) passes.**

New video (`scene-launch-villain-v6.html` + `films/launch-villain-v6.json` + fresh golden baseline).
Does not touch v3 or v5. Reuses `motion-lib.js` primitives, the morph engine, and ports the CTA.

## Why this revision exists (I was wrong about v5's first scenes)

rev 1 of this plan said "keep Scenes 1/3/8 from v5 — they rendered fine." They did not. Comparing the
v5 render (`export-video/_diag/f_3s.png`, `f_6s.png`, `f_20s.png`, `f_46s.png`) to the reference
images, v5 **under-built the green-world scenes**:

- Three independent models (Kimi 2.7, Gemini 3.5, Codex 5.5 — see
  `manifest-claude-system/Ideation/3ai'sanalisisonscenes.md`) all describe a **rich decoration
  system** for Scenes 1/1b/3/8 that v5 mostly omitted: a faint **grid mesh**, **dot-grid clusters**,
  **scattered hollow squares**, a **vertical anchor line + glow dot**, and the signature **glowing
  wave/topographic cluster** (6–8 fanning SVG paths).
- And **glow** — every lime element in the references blooms (text-shadow + SVG `feGaussianBlur`).
  v5's lime is flat. **The single biggest "cheap vs premium" lever is the glow, and v5 has none.**

v5's Scene 1 = a thin node-line + 3 flat waves, no grid/dots/squares, no bloom. That is the
"terrible/plain" the user sees. **The green-world scenes must be rebuilt to reference fidelity, not
carried over.** The tailor reduction and bug fixes from rev 1 still stand.

---

## 1. The consensus design system (distilled from 3 models, determinism-reconciled)

Where the three models agree, confidence is high. Where they differ (exact hue, exact px), I pick a
center value; the pilot tunes it.

### Tokens
```
--bg        : #06090d   (near-black; radial gradient #0e1622 → #03070b)
--lime      : #C8FF2A   (bright electric — consensus of #c8ff00 / #b7ff18 / #bef264)
--lime-soft : #D8FF68
--white     : #F5F7F5
--muted     : #A8AFB2
--red       : #EF463B   (villain only)
--red-dark  : #8F211D
--grid      : rgba(160,255,60,0.05)
```

### THE GLOW SYSTEM — the missing premium lever (build first, use everywhere)
- **Lime text glow:** `text-shadow: 0 0 20px rgba(200,255,42,0.40), 0 0 60px rgba(200,255,42,0.15)`.
  Apply to every lime numeral/headline. This alone closes most of the "cheap" gap.
- **Lime SVG glow:** one shared static filter, reused by every lime SVG (lines, waves, target, nodes):
  `<filter id="limeGlow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`
  Static filter = computed once = deterministic. Confirm in the pilot golden frames.
- Restraint: glow on lime accents/heroes only — not on body copy, not on the white card scenes.

### Fonts
Inter Variable (already vendored, auto-injected by `motion-lib.js`). Keep. Numerals weight 800,
~82–96px. Headlines bold. All three models read the type as Inter/Manrope — Inter is correct.

### Determinism reconciliation (the models' recipes vs our locks)
| Their recipe | Our rule | Do this |
|---|---|---|
| `backdrop-filter: blur()` (Gemini, Codex glass panels) | Lock risk (non-deterministic GPU) | **Fake glass:** `rgba(11,20,24,0.78)` fill + 1px border + `box-shadow` glow. No backdrop-filter. |
| `DrawSVG` plugin (all three) | not vendored | Use existing `draw()` / `strokeDashoffset` — same effect. |
| `feTurbulence`+`feDisplacementMap` animated stamp | filter under frame-step = risk | Static filter only (no animated baseFrequency), OR pre-baked transparent PNG. Reuse existing `stamp()` motion. |
| `mix-blend-mode: screen` on waves/glow | static = ok | Allowed if static; verify in pilot golden frames. |
| ambient drift / "loops" | Lock 3/7/9 | GSAP `repeat:-1`, killed at scene boundary. Never CSS animation. |
| all entrance motion | Lock 3 | transform/opacity/strokeDashoffset via GSAP only. |

---

## 2. Green-world decoration system (build ONCE, reuse in Scenes 1/1b/3/8)

This is the heart of the rebuild — the layer v5 was missing. Build as reusable CSS/SVG so all four
green-world scenes share it (the models confirm it's the same environment across these frames).

| Element | Build | Notes |
|---|---|---|
| **Base** | `radial-gradient(ellipse at 50% 40%, #0e1622, #03070b 70%)` | not flat black |
| **Grid mesh** | `repeating-linear-gradient` both axes, `--grid` color, ~44px cells, ~5% opacity | faint; can clip to a quadrant |
| **Dot-grid clusters** | small lime divs/SVG circles in 5×5 grids, corners (top-left, lower-right), opacity 0.3–0.6 | seeded positions if randomized (Lock 10) |
| **Scattered hollow squares** | `border:1px solid lime; transform:rotate(45deg)`, opacity ~0.25, absolute | a few, sparse |
| **Vertical anchor line** | SVG `<line>` lime + top `<circle>` glow dot (`#limeGlow`) | draws downward via `draw()` |
| **Wave cluster (SIGNATURE)** | 6–8 fanning sinusoidal SVG `<path>`, `fill:none`, `stroke=url(#waveGrad)` (transparent→lime→transparent), widths 1.5–2.5, opacities 0.3→0.9, all wrapped in `<g filter="#limeGlow">` | **the element v5 botched** — must be a luminous fan, not 3 thin lines. `draw()` them in with stagger. |
| **Corner brackets** (Scene 3) | SVG L-shapes, 4 corners, lime, opacity ~0.3 | draw-on |

**Continuous life (all `repeat:-1`, killed at each scene's end):** glow breathe on the radial; slow
x-drift on the wave cluster; gentle float on dots. Subtle — the references are calm, not busy.

---

## 3. Per-scene rebuild specs

Intensity/temperature arc unchanged (CTA only 5; Scene 2 cold peak; resolution warms). Each scene =
entry sequence + one continuous-life loop + a hero gesture.

### Scene 1 / 1b — Wound · REBUILD · cold-tech, lime accents
Full decoration system (§2) + glowing huge numerals. **This is the scene to fix first.**
- 1a: `40` (lime, glow, ~90px) `postulaciones.` (white) / `0` (lime) `respuestas.` / question line + lime
  `?` bubble icon. Left anchor line, grid, dots, squares, wave cluster all present.
- 1b: same environment persists; text swaps to `Nada.` (lime hero, ~100px, glow) / `Nadie te rechazó.`
  (white) / `Nadie te leyó.` (lime) / muted kicker.
- Hero: the wave cluster drawing in + the glowing numerals. Life: glow breathe + wave drift.

### Scene 2 — Villain · KEEP DENSE (intentional) · red HUD
The dense red dashboard is correct — it's the machine drowning the candidate, and `DESCARTADO` lands
over it. Reuse v5's mechanics (scan, score ring, stamp), restyle to the red HUD chrome (header
`ASÍ TE LEE EL FILTRO` + `RECHAZADO` badge, white CV card, red keyword highlights, bottom analysis +
score `23 BAJO`). Stamp via existing `stamp()` + `caFlash`. Vignette deepens and holds. Red radar
`repeat:-1`, killed at scene end. No glow here — flat/bureaucratic/cold is the point.

### Scene 3 — Turn · REBUILD (cleaner green-world) · warming
Sparse green-world (grid only, no wave cluster — the emptiness creates focus). Corner brackets, lime
**target icon** (concentric circles + crosshair + person, drawn in layers), white headline →
lime headline (`blurInChars`/splitWords), check + **hand-drawn lime underline** (`draw()`), all with
glow. First warmth (bloom pulse, vignette release). Life: target pulse.

### Scenes 4–6 — Tailor · REDUCE (keep rev-1 cut) · warm
The references show a full résumé dashboard. **On a 1080×1920 phone for ~6s that cannot be read** —
Kimi itself calls the tailor mockup "a desktop-density artifact." So keep the rev-1 reduction, but
**dress it in the reference's premium skin** (lime glow border, dark-on-navy, the score as hero):
- Keep visible: identity row (name + changing vacante line), **2 keyword lines** flipping red→lime,
  **one large score number** (~140px, lime, glow) climbing 23→92 / 92→94 / 94→[68 hold]→93.
- Cut: résumé paragraph, 3 job blocks + bullets, in-card skills row, warn flags, in-card CTA, radar.
- ~4 visible elements + 3 morph targets; card ~60% empty. Type ~1.6×.
- ⚠️ **Tension flag:** references say "full dashboard," user says "overcharged," phone+6s says "reduce."
  I'm siding with reduce + legibility. If the Scene-1 pilot proves the glow/decoration makes density
  readable, revisit — but default is reduced.

### Scene 7 — Caption pill · success banner
Dark rounded pill (FAKE glass, not backdrop-filter), lime circle-check that draws (circle→tick),
`Esto es lo que hacen los que sí consiguen entrevista`, `sí` lime + glow, blur-in last. Calm.

### Scene 8 — Human/close · REBUILD · warmest pre-climax
Left manifesto (glowing lime/white lines) + right vertical flow diagram (building → bot → ✗ → profile
→ WorqAI checklist), connected by glowing lime flow path with glow-dot nodes (`draw()` + node pops).
**Add the wave cluster back** (bottom, repositioned) + glow — v5's Scene 8 lacked it. Cards = fake
glass. Life: X-node pulse + breathing bloom (killed at CTA). Hero: flow path draw + hero line.

### Scene 9 — CTA · port unchanged
The reference peak. Confirm tokens match (same lime, same glow recipe) so it reads as one video.

---

## 4. Beat-timed choreography (absolute offsets, CTA-style)

Scene-relative offsets (`sN + x`), CTA cadence (beats 0.3–0.6s apart, eases vary, something always
moving). Map "DrawSVG" → `draw()`. The three models' beat lists agree closely; this is the merge.

### Scene 1 (start s1)
```
s1+0.0  grid + dots      fade/scale-in stagger              0.6  luxe        [entry]
s1+0.0  radial glow      breathe                            6.0  sine repeat:-1   [LIFE]
s1+0.1  anchor line      draw() downward + glow dot pop     0.8  luxe        [HERO build]
s1+0.0  wave cluster     draw() 6-8 paths, stagger 0.08, end glow pulse  1.2  luxe  [HERO/signature]
s1+0.3  "40"/"0"         x-30→0 + scale .95→1 + glow        0.4  settle (snap on numerals)
s1+0.45 white words      x-20→0                             0.4  luxe
s1+0.8  "?" bubble       scale 0→1 overshoot; body reveal   0.5  settle
s1+0.3  dots/squares     gentle float                       repeat:-1   [LIFE]
```
### Scene 1b (start s1b)
```
s1b+0.0  Scene-1 text     out y-24, opacity 0, blur          0.4  verdict
s1b+0.1  "Nada."          y30→0 + scale .9→1 + glow          0.4  verdict (impact)  [HERO]
s1b+0.25 "Nadie te rechazó" x-25→0                           0.4  luxe
s1b+0.40 "Nadie te leyó."  x-25→0 (lime)                      0.4  luxe
s1b+0.55 kicker            y10→0 muted + vignette pulse       0.4  luxe
s1b+end  KILL grid/wave/glow loops before Scene 2
```
Scenes 2/3/7/8 choreography: reuse v5's timeline cadence where the scene is structurally similar
(2 keeps v5's scan→stamp→score; 3/8 re-author per the new decoration — target/brackets draw, then
headlines, then underline/flow). Tailor choreography = rev-1's reduced version (2 keyword morphs +
score climb, NOT 9 morphs). CTA = ported verbatim.

---

## 5. The two bug fixes (verified causes — keep from rev 1)
- **Stray cursor** (Scenes 1/3/1b): `#cursor` is never `gsap.set` to `opacity:0` at init; CSS parks it
  bottom-right. Visible from t=0 until the first tailor click. **Fix:** `gsap.set("#cursor",{opacity:0})`
  in the init block. `cursorPress` already fades it in/out. (Confirmed: line 803/810 region of v5.)
- **Text-reveal glitch** ("haci…do", "Nadi  te rechazó"): `blurInChars` splits `#intro-l3` into
  SplitText char spans, then `morphSection` does `textContent="Nada."` on the same element → collision
  under `seek()`; adjacent `#intro-l4` reveal overlaps. **Fix:** reveal "Nada." as a separate clean
  `#intro-nada` node (never split, never morphed); fully fade `#intro-l3` out first; separate timeline
  positions so no two reveals overlap at 3.0s/6.0s. Verify at those exact frames in the `?dev=1` scrubber.

---

## 6. Determinism + safe-zone checklist (per scene, before commit)
- [ ] No live `backdrop-filter` (fake glass only).
- [ ] Glow = static `text-shadow` + static `feGaussianBlur` filter (computed once); golden-frame it.
- [ ] `DrawSVG` mapped to `draw()`/strokeDashoffset.
- [ ] Stamp filter static or pre-baked PNG (no animated `feTurbulence`).
- [ ] Every `repeat:-1` loop killed at its scene boundary (Lock 9).
- [ ] All randomness (dots, squares, particles) seeded per-scene (Lock 8/10).
- [ ] All `[data-copy]` text within top 120 / bottom 200 / x 56 (Lock 6 FAIL otherwise).
- [ ] Score number via `makeScoreRing` proxy tween (Lock 4).
- [ ] No CSS `@keyframes`/SMIL in video mode (Lock 7); `lagSmoothing(0)` + paused timeline (Lock 1/2).
- [ ] `gsap.set("#cursor",{opacity:0})` present.
- [ ] Vendor-only, no CDN.

---

## 7. Reference fidelity vs AI artifacts (what to ignore)
The models agree: **ignore** warped microtext, inconsistent job titles, imperfect icons, rough stamp
distortion, geometry wobble. The intended design is **clean vector HUD + crisp editorial type +
deterministic scan/reveal motion + glow.** Capture the system (decoration + glow + hierarchy), not the
raster's flaws. Keep the current narrative/voiceover copy (matches the existing VO track).

---

## 8. Open decisions (defaults set)
- **Lime hue:** `#C8FF2A` (consensus center). Tune in pilot. *(low stakes — glow matters more than hue.)*
- **Tailor:** reduced (legibility wins over reference density). Revisit only if the pilot disproves it.
- **Copy:** keep current narrative; mockup labels only as chrome.
- **Glass:** faked everywhere.

---

## 9. Staging — pilot Scene 1 FIRST (the thing that's "terrible")

v5 built all 9 in one shot. v6 gates twice, cheapest first.

1. **Scaffold** `scene-launch-villain-v6.html` from v5; apply both bug fixes (§5) now.
2. **PILOT A — Scene 1 green-world system** (the decoration system §2 + glow §1 + Scene 1 choreography).
   This is the scene the user hates AND it builds the reusable decoration layer for 1b/3/8 AND the wave
   cluster is the hardest element. Render Scene 1 only.
   - **Contact-sheet it next to `Scene 1.png`.** GATE: reads as premium (glow + wave cluster + decoration
     density present, not the sparse v5 version); deterministic (golden frames stable, incl. the glow
     filter); cursor gone; no text glitch at 3.0s/6.0s.
3. If Pilot A holds → build 1b, 3, 8 (they reuse the decoration system) → Scene 2 (red) → Scene 7.
4. **PILOT B — reduced tailor** (rev-1 spec, premium skin). Contact-sheet vs `Scne(4-6)tailors.png`.
   GATE: vacante + 2 keyword flips + score legible in ~6s; doesn't out-shout CTA.
5. If both hold → port CTA → `films/launch-villain-v6.json` (reuse `vo_villain_v3`/sounds/music) →
   full render → fresh v6 golden baseline.

## 10. Ship as a hypothesis
**Falsifier — v6 is worse if:** (1) the wave cluster + glow still render flat/sparse vs the reference
(→ Pilot A settles it before anything else); (2) the glow filter breaks determinism (→ golden-frame
the pilot); (3) the reduced tailor reads as unfinished (→ Pilot B; add one decorative breather, not
content); (4) it stops feeling like one video (→ same tokens/glow as CTA).
**Cheapest test first:** Pilot A — Scene 1 with the full decoration system + glow, contact-sheeted
against `Scene 1.png`. If that doesn't look premium, nothing downstream will.
