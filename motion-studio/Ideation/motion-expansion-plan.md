# Motion Studio — Expansion Plan: The Expensive Layer

Goal: raise output quality from "clean motion graphics" to "premium studio film" while keeping
every frame deterministic under the frame-stepper. Every new capability enters through the
same door the recorder did: **a 2-second spike, exported twice, hashes compared.** No spike,
no entry.

Written for phased execution by a cheaper model (Sonnet). Phases 0–2 are mechanical given
this spec. Phases 3–5 each start with a spike whose PASS/FAIL gate is binary.

---

## The one law that governs everything here (extends Lock 3)

> Every new effect — particle, Lottie, shader, 3D — must be a **pure function of `(t, seed)`**.
> Given the same timeline position and the same seed, it produces the same pixels. If a
> library owns its own clock (rAF loop, autoplay, wall-time), it is driven manually per
> stepped frame or it does not enter the pipeline.

Add this to `.claude/rules/motion-determinism.md` as **Lock 10** when Phase 0 lands.

---

## Phase 0 — Vendor infrastructure (no behavior change)

Local, pinned, offline. No CDN at render time — CDN flakiness breaks determinism and
offline renders, and an unpinned version bump silently invalidates every golden hash.

1. Create `vendor/` at repo root:
   ```
   vendor/
     gsap/            gsap.min.js + SplitText, MorphSVGPlugin, DrawSVGPlugin,
                      MotionPathPlugin, CustomEase, CustomWiggle, CustomBounce,
                      ScrambleTextPlugin, Physics2DPlugin  (all free since GSAP 3.13)
     lottie/          lottie.min.js          (Phase 3)
     three/           three.module.min.js    (Phase 5, only if spike passes)
     VERSIONS.md      exact version + source URL + sha256 of every file
   ```
2. Source: `npm pack gsap@3.13` (or direct dist downloads), `lottie-web` (MIT),
   `three` (MIT). Record versions in `VERSIONS.md`.
3. Switch scene templates from CDN `<script>` tags to `vendor/` paths. One scene first
   (villain-v3), confirm golden hashes still match, then the rest.
4. Add a preflight WARN: scene references a CDN URL → flag it.

**Gate:** villain-v3 re-exports with unchanged golden hashes after the vendor switch.

---

## Phase 1 — The Expensive Pass (taste, not tech — biggest visual ROI)

No new runtime concepts; everything is a GSAP tween. This phase alone closes ~60% of the
gap to "premium studio."

### 1a. Signature easing (CustomEase / CustomWiggle / CustomBounce)
- Define a named house ease set in `motion/tokens/motion-tokens.json` and register in
  `motion-lib.js`:
  - `worq-luxe` — slow-out with a 2% overshoot and settle (replaces stock `power3.out` on hero text)
  - `worq-snap` — hard mechanical in (UI elements, stamps)
  - `worq-settle` — CustomBounce, tiny amplitude, for anything that "lands" (badges, score ring)
  - `worq-breathe` — CustomWiggle, micro oscillation for held elements (the score during hesitation)
- Rule: stock eases (`power3.out` etc.) become fallbacks; hero moments use house eases.

### 1b. Secondary motion (the "alive" tell)
- Nothing stops dead. Every entrance gets a settle; every exit gets a 0.04–0.08s anticipation.
- Concretely: score badge lands with `worq-settle`; job chips overshoot 4px and return;
  the RECHAZADO stamp adds 1 degree of post-impact rotation decay.
- Implement as `motion-lib.js` helpers: `landWith(tl, sel, t, props)` wraps the main tween + settle.

### 1c. Variable-font animation
- Swap headline font to a variable axis font (Archivo Expanded variable or Inter var — both free).
- New helper `weightShift(tl, sel, t, from, to, dur)` tweening `font-variation-settings`.
- Hero use: "No eres tú." arrives at weight 500 and *thickens* to 900 over 0.5s as it turns lime.
  Weight as emotional intensity — almost nobody does this; it reads as bespoke typography.

### 1d. Post-processing layer (the film look)
- New fixed full-frame layer in the shell, above content, below grain:
  - **Vignette** — static radial gradient, opacity tweened up 0.06→0.12 during emotional beats
  - **Chromatic aberration on cuts** — SVG filter (`feOffset` ×2 color channels), intensity
    tweened 0→2px→0 across scene transitions only (60–120ms). The "expensive transition" tell.
  - **Bloom on lime** — `feGaussianBlur`-based glow layer behind lime elements, pulsing
    ±10% with score events.
- All driven by tweens — zero wall-clock anything (Lock 3/10 compliant).

### 1e. Curved cursor (MotionPathPlugin)
- Replace the straight-line cursor move in `cursorPress` with a slight bezier arc + a 2-frame
  deceleration hover before the click. Straight-line cursors read as robotic; arcs read as human.

### 1f. SplitText upgrade
- Replace hand-rolled `splitWords` with SplitText (chars + words + lines, proper masking).
- Unlocks per-char blur-in for the wound lines (char arrives blurred 4px → sharp).

**Gate:** re-render one existing scene (text-poster or stat-reveal) with the full expensive
pass. Side-by-side contact sheets, old vs new. The new one must be *obviously* richer —
if the difference needs explaining, iterate before rolling to villain-v3.

---

## Phase 2 — The Particle Layer

**What particles are:** dozens-to-thousands of tiny elements (dust motes, sparks, embers,
floating dots) animated as a field. They are the single biggest "expensive atmosphere"
multiplier — they add depth (foreground/background separation), life (nothing is static),
and texture (light has something to catch). Every high-end title sequence has them; almost
no startup ad does.

Two deterministic implementations, by particle count:

### 2a. DOM particles (≤ ~120 particles) — zero new tech
- N absolutely-positioned divs, positions/sizes/delays generated from the **existing seeded
  PRNG** (the shell already has one — this is why it's there).
- Animated by plain GSAP tweens (drift, opacity flicker, scale). Fully timeline-native.
- Helper: `particleField(tl, layerSel, t, { count, seed, area, drift, size, color })`.

### 2b. Canvas particles (hundreds–thousands) — one new helper, still no library
- One `<canvas>` layer. A pure function: `drawParticles(ctx, t, seed, preset)` — computes
  every particle's position *analytically from t* (position = f(seed, t), not incremental
  simulation), clears, redraws.
- Driven by a single proxy tween (Lock 4 pattern): `gsap.to(proxy, {t: DUR, onUpdate: draw})`.
- Because position is computed from t (not accumulated frame-to-frame), seeking to frame 173
  cold gives identical pixels. No simulation state = no drift = deterministic.

### Particle presets (build these four, in order)
| Preset | What | Where it serves |
|---|---|---|
| `ambient-dust` | 40–80 slow drifting motes, depth-blurred, 3 size classes | Scenes 1, 3, 8 — atmosphere behind text |
| `scan-sparks` | short-lived sparks emitted along the scan bar's current y | The lime scan — the rewrite literally throws sparks |
| `score-burst` | one-shot radial burst, 120–200 particles, lime | Score landing on 92/93/94 |
| `ember-rise` | slow rising embers, fade with height | CTA background — warmth under the logo |

**Spike (entry gate):** `spikes/particle-spike/` — 2s, `ambient-dust` + one `score-burst`,
exported twice, `golden_frames.py` hash-identical. Canvas determinism on 2D context is
solid, but prove it before any scene uses it.

**Restraint rule:** particles are seasoning. Default opacity ≤ 0.35, never over text,
ambient presets pause (fade to 0.15) during copy-heavy beats. The expensive look is
*restrained* particles; visible particle soup is the cheap look.

---

## Phase 3 — Lottie lane (the After Effects ecosystem)

- Vendor `lottie-web`. Adapter in `motion-lib.js` (~12 lines, Lock-4 pattern):
  ```javascript
  function lottieSeek(tl, anim, t, dur, fromFrame, toFrame) {
    const proxy = { f: fromFrame };
    tl.to(proxy, { f: toFrame, duration: dur, ease: "none",
      onUpdate: () => anim.goToAndStop(proxy.f, true) }, t);
  }
  ```
  `goToAndStop(frame, true)` is a pure frame-seek → deterministic by construction.
- Init rule: load with `autoplay: false, loop: false`; preflight FAIL if a Lottie instance
  has autoplay on (extends the "running CSS animation" check).
- Sourcing workflow: LottieFiles → download JSON → **license check (record in
  `motion/lottie/CREDITS.md`)** → drop in `motion/lottie/` → preview in dev scrubber.
- First use cases: a liquid transition wipe, an abstract accent behind the CTA logo,
  a checkmark micro-animation for the score badge.

**Spike:** one downloaded Lottie JSON seeked across 2s, double-export, hashes match.
(Risk is low — lottie-web renders to SVG/canvas synchronously — but the gate is the gate.)

---

## Phase 4 — Shader post-processing (Shadertoy-class effects)

- One fullscreen WebGL canvas, one quad, fragment shader with `uTime` fed **from the
  timeline proxy**, never `performance.now()`.
- Target effects: heat-haze distortion behind the RECHAZADO stamp, holographic sheen
  sweeping the lime scan, refraction ripple on scene cuts.
- **Determinism risk is real here (GPU float behavior).** Spike protocol:
  1. 2s shader spike, export twice on the default GPU path → compare hashes.
  2. If mismatch: relaunch Playwright Chromium with SwiftShader (CPU GL — bit-deterministic,
     slower) and re-test.
  3. If SwiftShader passes but is too slow for full films: shaders render only on scenes
     that need them, or adopt a perceptual-diff mode in `golden_frames.py`
     (SSIM ≥ 0.999 threshold) for shader scenes only — exact hashes stay law everywhere else.
- If both paths fail the gate: Canvas2D fallbacks (cheaper versions of haze/sheen) and the
  WebGL lane closes. The gate decides, not enthusiasm.

---

## Phase 5 — three.js depth lane (the Blender-look, gated hardest)

Enters **only if Phase 4's spike resolved the GPU determinism question** (same renderer,
same risk). Then:

- All scene values (camera, lights, materials, transforms) driven by GSAP tweens;
  `renderer.render()` called once per stepped frame from the proxy `onUpdate`.
- First constructs: the CV card as a lit 3D plane (specular highlight moving as it tilts),
  true-depth ghost-card fan-out, depth-of-field focus pull from card to caption.
- Postprocessing via three's EffectComposer (bloom, DOF) — same uTime discipline.
- Blender itself (headless `bpy` → transparent PNG sequence → ffmpeg overlay) stays
  **parked** unless a concept needs raytraced quality three.js can't fake on a phone screen.
  It's a second pipeline; the trigger condition is a named concept, not ambition.

---

## Pipeline & docs updates (lands with whichever phase ships first)

1. `.claude/rules/motion-determinism.md` → add Lock 10 (pure function of `(t, seed)`).
2. `.claude/skills/motion-builder/SKILL.md` → new "Expensive Layer" section: house eases,
   particle presets, post-processing constructs, the lottieSeek pattern, with "crib from"
   pointers — same format as the existing production effect table.
3. `motion_preflight.py` → new checks: CDN reference (WARN), Lottie autoplay (FAIL),
   vendor version mismatch vs VERSIONS.md (WARN).
4. Each spike lives in `spikes/{name}-spike/` with a README stating PASS criteria —
   the recorder-spike pattern, repeated.

## Order of operations

```
Phase 0 (vendor)            → 1 session, mechanical
Phase 1 (expensive pass)    → 2–3 sessions, the visible leap
Phase 2 (particles)         → spike + 1–2 sessions
   ── ship a film here: villain-v3.1 with Phases 1–2 applied ──
Phase 3 (Lottie)            → spike + 1 session
Phase 4 (shaders)           → spike decides
Phase 5 (three.js)          → only through Phase 4's gate
```

Ship after Phase 2, not after Phase 5. Phases 1–2 are where viewers feel the difference;
3–5 are where capability compounds. Don't hold a better film hostage to a 3D lane.

## Calibration note

The claim "this reads as premium" is testable the same way the villain frame is: contact
sheets old-vs-new in front of 5 real eyes, plus retention on the next posted cut. If
Phase 1+2 don't move perceived quality, stop and re-diagnose before buying complexity in
Phases 3–5. Surety brings ruin; spikes bring receipts.
