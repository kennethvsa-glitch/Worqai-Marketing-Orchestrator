# Motion Builder Skill

Builds branded motion graphics as MP4 videos. Output is a self-contained animated HTML file rendered to video via Playwright frame-stepping + ffmpeg.

**Read before every build session:**
- `.claude/rules/motion-determinism.md` — 9 implementation locks (non-negotiable)
- `.claude/rules/anti-slop.md` — copy rules
- `plan.md` — Phase 1 scope and build order

---

## Spec Format (copy only — no timing)

```json
{
  "meta": {
    "system": "s01",
    "aspect": "9:16",
    "duration": 8,
    "fps": 30,
    "seed": "worqai-stat-73pct",
    "video_mode": true
  },
  "scene": "stat-reveal",
  "copy": {
    "kicker": "CV rechazado por ATS",
    "stat": 73,
    "stat_suffix": "%",
    "context": "de CVs latinos no pasan el filtro",
    "source": "Dato interno WorqAI · 2025"
  }
}
```

**Rules:**
- `meta.seed` is required — used to seed PRNG for deterministic geo layer positions
- `copy.stat` must be numeric (integer or float) when used with the `counter` effect
- `meta.video_mode: true` triggers CSS animation freeze and seeded PRNG in the rendered HTML
- No timing, no easing, no sequence — the scene template owns all of that
- No `layers`, no `decoratives` in Phase 1 specs — the scene template handles those

---

## Effect Library (Phase 1 — 7 effects)

Each effect is a JavaScript function in `templates/motion-shell.html`.

| ID | What it does | Properties animated | Direction param |
|---|---|---|---|
| `fade` | opacity 0 → 1 | `opacity` | `in` / `out` |
| `slide` | translateY + fade | `y`, `opacity` | `in` / `out` |
| `text-reveal` | clip-path word/line reveal | `clipPath` | `in` / `out` |
| `counter` | number counts up via proxy | proxy `val` + `onUpdate` | `in` |
| `scale` | scale(0.85) → 1 + fade | `scale`, `opacity` | `in` / `out` |
| `reveal` | clip-path mask (generic, any element) | `clipPath` | `in` / `out` |
| `blur` | filter blur → sharp | `filter` | `in` / `out` |

**Implementation rule (Lock 3):** Every effect animates properties directly via `gsap.to()` — never via CSS class toggle + CSS transition. CSS transitions run in wall-clock time and will produce garbage frames under `seek()`.

**counter rule (Lock 4):** Must be a GSAP tween of a proxy `{ val: 0 }` with `onUpdate` writing `innerText`. Never `setInterval` or `requestAnimationFrame`.

**direction parameter:** Even if Phase 1 only uses `in`, every effect is built with a `direction` parameter so exit counterparts don't require a rewrite later.

---

## Production Effect Library (what actually shipped — reuse before reinventing)

The 7 effects above are the Phase 1 primitives. The launch video
(`templates/scenes/scene-launch-honest.html`) is the **reference implementation** and
proves a richer set of compound effects, all hand-authored on an absolute-timed GSAP
timeline. Read that file before building a new narrative video — these are proven and
deterministic-safe:

| Construct | What it does | Where to crib it |
|---|---|---|
| `morphSection(tl, t, sel, html, dur, asHTML)` | blur-out → swap text → blur-in. The "rewrite" effect. Works with `<span class='kw'>` lime highlights via `asHTML` | scene-launch-honest.html ~L246 |
| score-ring | SVG circle `stroke-dashoffset` + color ramp via proxy `{val,offset,r,g,b}` + `onUpdate` (Lock 4) | ~L230, L349 |
| scan-bar sweep | `clipPath inset()` top→bottom. **Recolor it: red = the filter rejecting, lime = WorqAI rewriting** | ~L318 |
| cursor click | move to measured button center → scale 0.76 bounce + button compress + ripple | `makeRunTailor` ~L304 |
| badge / stamp | scale-spring + `back.out`. Recolor red + add `rotate` for a RECHAZADO stamp | ~L363 |
| ghost-card fan-out | stacked → fanned via x/y/rotate/scale/opacity. Reads as superposition (one person, N branches) | ~L538 |
| overlay reset-under-cover | full-screen overlay hides the card while you mutate DOM state, then lifts to reveal in one cut — no visible pop-in | Scene 4 / `turn-scene` ~L504 |
| kw highlight toggle | `cv-clean-mode` body class toggles red (`kw-bad`) / lime (`kw`) spans | ~L474 |
| banner swap | swap `display` between two stacked banners under cover | ~L511 |

**Rule:** a new narrative video is a copy of `scene-launch-honest.html` with new copy,
re-sequenced beats, and recolored primitives — not a from-scratch build. The Phase 1
spec→render pipeline does not generate these scenes; they are authored directly.

---

## Expensive Layer (Phases 1–3 additions — crib from motion-lib.js)

These are the taste-level upgrades that separate "clean motion graphics" from "premium studio."
All live in `templates/motion-lib.js`. All are Lock 3/10 compliant.

### House Eases (motion-lib.js, top of file)

| Name | Type | Use |
|---|---|---|
| `worq-settle` | CustomBounce strength:0.3 | Preferred landing ease — badges, score ring, chips. Replaces `settle` in Phase 1+ scenes |
| `worq-breathe` | CustomWiggle wiggles:4 | Score ring during hesitation beat — held micro oscillation |
| `snap` | CustomEase 0.85,0,0.15,1 | UI events: clicks, stamps — fast, hard stop |
| `luxe` | CustomEase 0.22,1,0.36,1 | Hero text, card reveals — slow out, long tail |
| `mech` | CustomEase 0.7,0,0.84,0 | Villain/filter: accelerating in, no mercy |
| `verdict` | CustomEase 0.9,0,1,1 | Stamp: hard arrival, zero bounce |

Requires: `CustomBounce-3.15.0.min.js`, `CustomWiggle-3.15.0.min.js` loaded before `motion-lib.js`.

### Secondary Motion (Phase 1b)

Nothing stops dead. Entrances get a settle; exits get a 0.04–0.08s anticipation.

```javascript
// landWith — entrance + worq-settle micro-bounce. Nothing stops dead.
landWith(tl, "#badge", t, { y: 20, opacity: 0, duration: 0.55 });

// stamp — now includes 1-degree post-impact rotation decay (Phase 1b)
stamp(tl, "#rechazado-stamp", "#cv-card", 10.5);
```

### Variable Font — weightShift (Phase 1c)

```javascript
// Requires Inter Variable font (vendor/fonts/InterVariable-latin.woff2)
// and font-family: 'Inter Variable' on the element.
// Hero use: "No eres tú." arrives weight 500, thickens to 900 as it turns lime.
weightShift(tl, "#intro-l3", t, 500, 900, 0.5);
```

CSS on the element: `font-family: 'Inter Variable', sans-serif;`
The @font-face is auto-injected by motion-lib.js on load.

### Post-Processing Layer (Phase 1d)

Fixed full-frame layer above content, below grain. All tweens — zero wall-clock.

```javascript
// Call once before building the timeline:
const { vignetteEl, caEl, bloomEl } = initPostLayer();

// Vignette deepens on emotional beats:
vignetteUp(tl, t, 0.06, 0.12, 0.4);   // 0.06→0.12→0.06 over 0.8s

// Chromatic aberration on cuts (60–120ms):
caFlash(tl, t, 2);   // peak 2px offset, 120ms total

// Lime bloom pulses with score events:
bloomPulse(tl, t, 0.7, 0.1, 0.35);   // center 0.7 opacity ±10% over 0.35s
```

### Curved Cursor (Phase 1e)

`cursorPress` now uses MotionPathPlugin for a slight bezier arc approach + 2-frame hover
deceleration before the click. Requires `MotionPathPlugin-3.15.0.min.js`.

```javascript
// Same call signature as before — arc is automatic when MotionPathPlugin is loaded:
cursorPress(tl, oCX, oCY, clickT, "#optimize-btn", "#btn-ripple");
```

### SplitText — per-char blur-in (Phase 1f)

```javascript
// Per-char blur 4px→sharp on wound lines:
blurInChars(tl, "#intro-l3", t, { duration: 0.55, stagger: 0.03 });

// For manual access:
const split = splitChars("#headline");
tl.from(split.chars, { filter: "blur(4px)", opacity: 0, stagger: 0.02 }, t);
```

Requires `SplitText-3.15.0.min.js`.

### Particles (Phase 2)

**DOM particles (≤120, timeline-native):**
```javascript
// ambient-dust: 70 slow drifting motes behind text (opacity ≤ 0.35)
particleField(tl, "#particle-layer", 0, {
  count: 70, seed: "scene-001", color: "255,255,255", opacityMax: 0.28, duration: 8,
});
```

**Canvas particles (hundreds, proxy-tween driven — Lock 10):**
```javascript
// score-burst: one-shot radial burst when score lands
canvasParticles(tl, "#burst-canvas", scoreT, 1.2, "scene-001", "score-burst", {
  cx: 540, cy: 1390, count: 160,
});

// Presets: "ambient-dust" | "scan-sparks" | "score-burst" | "ember-rise"
```

**Restraint rule:** particles are seasoning. Opacity ≤ 0.35. Never over text. Ambient
presets fade to 0.15 during copy-heavy beats. Soup is the cheap look.

**Gate:** run `spikes/particle-spike/spike_render.py` first. PASS before any scene uses particles.

### Lottie (Phase 3)

```javascript
// goToAndStop is a pure frame-seek — deterministic by construction (Lock 10).
// Init: ALWAYS autoplay: false, loop: false.
const anim = lottie.loadAnimation({
  container: el, renderer: "svg", loop: false, autoplay: false, path: "../../motion/lottie/file.json",
});
anim.addEventListener("DOMLoaded", () => {
  lottieSeek(tl, anim, startT, dur, 0, anim.totalFrames - 1);
});
```

Requires `vendor/lottie/lottie-5.12.2.min.js`. License must be recorded in `motion/lottie/CREDITS.md`.
**Gate:** run `spikes/lottie-spike/spike_render.py` first. PASS before any scene uses Lottie.

---

## Motion Tokens — s01 (Phase 1 only)

```json
{
  "s01": {
    "duration_unit": 0.55,
    "ease_default": "power3.out",
    "ease_snap": "power4.out",
    "blur_start": "14px",
    "stagger_chars": 0.03,
    "stagger_lines": 0.12,
    "stagger_elements": 0.15
  }
}
```

`duration_unit` is the base beat. Multiply it for longer animations:
- Fast entrance: `duration_unit × 1` = 0.55s
- Stat counter: `duration_unit × 3` = 1.65s
- Slow reveal: `duration_unit × 2.5` = 1.375s

Only s01 is defined in Phase 1. Do not build scene templates that work across all 48 systems — prove the motion language on s01 first.

---

## Scene Template Spec

A scene template (`templates/scenes/scene-*.html`) is a complete animated HTML file that:

1. References `motion-shell.html` design tokens (via CSS custom properties, inline or linked)
2. Has a GSAP timeline with **absolute per-element timing** — every element has an explicit `at` position and duration, not a computed stagger
3. Injects copy from template variables (populated by `render_motion.py`)
4. Signals completion via `window.motionReady = true` after `document.fonts.ready` and all assets load
5. Has `data-copy` attributes on every text element for the safe-zone check in the exporter

```html
<!-- example element in a scene template -->
<div class="stat-number" data-copy="stat">{{ copy.stat }}{{ copy.stat_suffix }}</div>
```

**Absolute timing means:** the GSAP timeline looks like this:
```javascript
const tl = gsap.timeline();
tl.add(fade("kicker", "in"), 0.3)       // kicker appears at 0.3s
  .add(counter("stat-number", 73), 1.2)  // counter starts at 1.2s, runs 1.65s
  .add(slide("context", "in"), 2.4)      // context slides in at 2.4s
  .add(fade("source", "in"), 3.0);       // source fades in at 3.0s
```

Not:
```javascript
tl.staggerFrom(".elements", 0.5, {}, 0.15);  // global stagger — never this
```

---

## Safe Zones

All content must sit within these bounds (enforced by exporter — FAIL if violated):

```
9:16 (1080×1920):
  top:    120px  (--safe-top)
  bottom: 200px from bottom  (--safe-bottom)
  left:   56px   (--safe-x)
  right:  56px   (--safe-x)
```

Content area: 968px wide × 1600px tall.

---

## Design Systems in Phase 1

**Phase 1 uses s01 only.** s01 tokens:

```css
--bg-base:       #080a10;
--bg-mid:        #0f1420;
--accent:        #d4af37;  /* gold */
--text-primary:  #ffffff;
--text-secondary: rgba(255,255,255,0.72);
--font-display:  'Archivo Black', sans-serif;  /* 900 weight */
--font-body:     'Inter', sans-serif;
--grain-opacity: 0.11;
```

Do not attempt to make scene templates work across multiple systems in Phase 1.

---

## Build Order (Phase 1)

1. `spikes/recorder-spike/` — prove the pipeline (see plan.md)
2. `templates/motion-shell.html` — shell with 7 effects, seeded PRNG, safe zone vars
3. `scripts/render_motion.py`
4. `scripts/motion_exporter.py`
5. `scripts/motion_contact_sheet.py` — before first real scene
6. `scripts/motion_preflight.py`
7. `templates/scenes/scene-stat-reveal.html`
8. `templates/scenes/scene-text-poster.html`

---

## Preflight Checks

| Check | Type | Gate |
|---|---|---|
| All copy fields populated | FAIL | pre-render |
| `copy.stat` is numeric (if scene uses counter) | FAIL | pre-render |
| Every effect name maps to a loaded function in shell | FAIL | pre-render |
| `meta.seed` is set | WARN | pre-render |
| Total timeline duration ≤ `meta.duration` (excludes repeat:-1) | FAIL | pre-render |
| System is s01 | WARN | pre-render (Phase 1 gate) |
| CDN script reference in scene HTML | WARN | pre-render (use vendor/ paths) |
| Lottie `autoplay:true` detected | FAIL | pre-render (breaks Lock 10) |
| Vendor file not listed in `vendor/VERSIONS.md` | WARN | pre-render |
| Safe-zone overflow | FAIL | in exporter, after page load |
| Running CSS animations in video mode | FAIL | in exporter, before frame loop |
