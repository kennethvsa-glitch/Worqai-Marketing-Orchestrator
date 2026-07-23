# villain-v3 — CTA Redesign Plan (Scene 9)

Rebuilds Scene 9 (CTA) of `scene-launch-villain-v3.html` to match the supplied design mockup:
logo → badge → subtext → title (two-line, lime + white-with-underline) → description →
glowing button (icon + arrow) → features row (Rápido/Seguro/Preciso) → footer, over a
decorative lime "magic trail" (curved SVG path + twinkling star) with rising lime particles.

Base: current rev3 (54s, 60fps), CTA at `ctaT = humanT + 5.2`.

**Files in play:**
- `templates/scenes/scene-launch-villain-v3.html` — DOM + init + timeline (CTA block only)
- `templates/scenes/scene-launch-villain-v3.css` — CTA styles only
- `templates/motion-lib.js` — **read-only**; reuse `draw`, `particleField`, `seededRandom`
- `export-video/golden/scene-launch-villain-v3.json` — re-capture at end

**Read before touching anything:**
- `.claude/rules/motion-determinism.md` (Locks 3, 6, 7, 9, 10 all apply here)
- `.claude/rules/anti-slop.md`
- `.claude/rules/output-conventions.md`

---

## Decisions (locked)

| Topic | Decision | Consequence |
|-------|----------|-------------|
| Logo | **Keep lime PNG** (`worqai_logo.png`, current filter chain) | No new font; no rounded-font vendoring |
| Decoration | **Full trail + particles** | New `#cta-decor` SVG (curve + star) + `particleField` lime layer |
| Pacing | **Extend CTA ~2–3s** | Each element its own beat; film grows to ~57s; re-measure duration |
| Color/bg | **Keep film tokens** (`--lime #C9F24D`, `--bg #0C0E16`) | Ignore mockup's `#C6F43A`/`#0B0F14` so CTA matches the prior 50s |
| Fonts | **Archivo (body) + JetBrains Mono (footer)** | Inter is vendored but the film is Archivo-native; stay consistent |

---

## Copy (final — all reused from current CTA, re-laid-out)

| Slot | Text | Color | Notes |
|------|------|-------|-------|
| Logo | (worqai_logo.png) | lime | unchanged |
| Badge | `TE DESCARTARON EN SEGUNDOS.` | lime | ⚡ icon + uppercase via `text-transform` |
| Subtext | `Sin siquiera llegar a un humano.` | muted | was `#cta-promise` |
| Title L1 | `Así que les copiamos el filtro y` | lime | needs `Así` (í) |
| Title L2 | `lo pusimos de tu lado.` | ink (white) | lime SVG underline beneath |
| Description | `Con WorqAI podés adaptar tu CV a cualquier vacante en segundos.` | muted, `en segundos.` lime | needs `podés` (é) |
| Button | `Analiza mi CV gratis` | on-lime | icon left + `→` right + glow |
| Features | `Rápido` · `Seguro` · `Preciso` | muted | needs `Rápido` (á); icons lightning/shield/target |
| Footer | `worqai.io · español e inglés` | muted | unchanged |

`data-copy` lives on visible single-line elements only (badge text, subtext, description,
features labels, footer). The title is two spans + underline — put `data-copy` on each span,
not the wrapper. Orthography check runs on the file (verification step 4).

---

## Vertical budget (Lock 6 — the hard constraint)

`#cta-group` is `inset: 0`, flex-centered, with its own `--bg`. The overflow gate (FAIL)
flags any `[data-copy]` whose `bottom > 1720px` or `right > 1024px`. The stack must stay
short enough that, centered, nothing crosses 1720. Target total column height **≤ 1380px**
(centered → bottom ≈ 960 + 690 = 1650 < 1720, with margin).

Approx heights (incl. margin-bottom):
```
logo        130 (img 90 + mb 40)
badge        78 (pill ~46 + mb 32)
subtext      52 (28 + mb 24)
title       190 (2 lines @ ~62px + underline + mb 28)
description  76 (44 + mb 32)
button       96 (pad+text ~72 + mb 40)
features     60 (icons+label ~30 + mb 28)
footer       24
────────────────
total       ~706   ✓ well under budget
```
Generous. The risk is **horizontal**: title L1 at large size must not exceed `max-width`
and the badge/features must not exceed 1024px right edge. Cap `max-width` on title/desc and
confirm on the draft contact sheet.

---

## New DOM — replace the entire `#cta-group` block

Current block (HTML lines ~46–55, the `#cta-group` div with logo-wrap, headline, promise,
subline, tagline, btn, domain) → replace with:

```html
<!-- Scene 9: CTA -->
<div id="cta-group">
  <!-- Decorative layer (behind text) -->
  <div id="cta-particles-layer"></div>
  <svg id="cta-decor" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="cta-trail-grad" x1="0" y1="1" x2="0" y2="0">
        <stop offset="0%"  stop-color="rgba(201,242,77,0)"/>
        <stop offset="60%" stop-color="rgba(201,242,77,0.35)"/>
        <stop offset="100%" stop-color="rgba(201,242,77,0.9)"/>
      </linearGradient>
    </defs>
    <path id="cta-trail" d="M540 1920 C 460 1740, 640 1560, 540 1400 S 460 1240, 560 1150"
          fill="none" stroke="url(#cta-trail-grad)" stroke-width="3" stroke-linecap="round"/>
    <g id="cta-star" transform="translate(560 1150)">
      <path d="M0 -22 L6 -6 L22 0 L6 6 L0 22 L-6 6 L-22 0 L-6 -6 Z"
            fill="var(--lime)"/>
    </g>
  </svg>

  <!-- Content -->
  <div id="cta-logo-wrap"><img id="cta-logo-img" src="../../Ideation/worqai_logo.png" alt="WorqAI"></div>

  <div id="cta-badge">
    <svg class="cta-badge-icon" viewBox="0 0 24 24" fill="none">
      <path d="M13 2L4.5 13.5H11l-1 8.5L19.5 10H13z" fill="currentColor"/>
    </svg>
    <span id="cta-badge-text" data-copy="TE DESCARTARON EN SEGUNDOS.">TE DESCARTARON EN SEGUNDOS.</span>
  </div>

  <div id="cta-subtext" data-copy="Sin siquiera llegar a un humano.">Sin siquiera llegar a un humano.</div>

  <div id="cta-headline">
    <span class="cta-h-line cta-h-lime" data-copy="Así que les copiamos el filtro y">Así que les copiamos el filtro y</span>
    <span class="cta-h-line cta-h-ink"  data-copy="lo pusimos de tu lado.">lo pusimos de tu lado.</span>
    <svg id="cta-underline" viewBox="0 0 320 14" preserveAspectRatio="none" aria-hidden="true">
      <path id="cta-underline-path" d="M4 9 C 90 2, 230 2, 316 7" fill="none"
            stroke="var(--lime)" stroke-width="6" stroke-linecap="round"/>
    </svg>
  </div>

  <div id="cta-desc" data-copy="Con WorqAI podés adaptar tu CV a cualquier vacante en segundos.">Con WorqAI podés adaptar tu CV a cualquier vacante <span class="cta-accent">en segundos.</span></div>

  <div id="cta-btn">
    <svg class="cta-btn-icon" viewBox="0 0 24 24" fill="none">
      <path d="M12 2v6m0 8v6m10-10h-6M8 12H2m15.07-7.07l-4.24 4.24M11.17 12.83l-4.24 4.24m12.14 0l-4.24-4.24M11.17 11.17L6.93 6.93" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg>
    <span id="cta-btn-text">Analiza mi CV gratis</span>
    <span id="cta-btn-arrow" aria-hidden="true">&#8594;</span>
  </div>

  <div id="cta-features">
    <div class="cta-feat">
      <svg class="cta-feat-icon" viewBox="0 0 24 24" fill="none"><path d="M13 2L4.5 13.5H11l-1 8.5L19.5 10H13z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>
      <span data-copy="Rápido">Rápido</span>
    </div>
    <span class="cta-feat-sep">·</span>
    <div class="cta-feat">
      <svg class="cta-feat-icon" viewBox="0 0 24 24" fill="none"><path d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>
      <span data-copy="Seguro">Seguro</span>
    </div>
    <span class="cta-feat-sep">·</span>
    <div class="cta-feat">
      <svg class="cta-feat-icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="3.5" stroke="currentColor" stroke-width="1.5"/></svg>
      <span data-copy="Preciso">Preciso</span>
    </div>
  </div>

  <div id="cta-domain" data-copy="worqai.io · español e inglés">worqai.io · español e inglés</div>
</div>
```

**Watch-out:** the bolt path uses `var(--lime)` only where `fill="currentColor"` resolves
from the parent's `color`. Verify the badge icon fills lime (badge `color: var(--lime)`).

---

## New CSS — replace the `── CTA ──` block

Remove all current `#cta-*` rules (lines ~235–243) and replace with:

```css
/* ── CTA ──────────────────────────────────────────────────────── */
#cta-group { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; background: var(--bg); overflow: hidden; }

/* Decorative layer (behind content) */
#cta-particles-layer { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
#cta-decor { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
#cta-star  { filter: drop-shadow(0 0 14px rgba(201,242,77,0.65)); }

/* Logo */
#cta-logo-wrap { background: transparent; margin-bottom: 40px; z-index: 1; }
#cta-logo-img  { width: 240px; display: block; filter: brightness(0) invert(1) sepia(1) saturate(1150%) hue-rotate(15deg) brightness(95%); }

/* Badge */
#cta-badge { z-index: 1; display: inline-flex; align-items: center; gap: 10px; color: var(--lime); border: 1.5px solid rgba(201,242,77,0.55); border-radius: 999px; padding: 12px 24px; margin-bottom: 30px; }
.cta-badge-icon { width: 20px; height: 20px; flex: 0 0 auto; }
#cta-badge-text { font-family: var(--font-body); font-size: 22px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }

/* Subtext */
#cta-subtext { z-index: 1; font-family: var(--font-body); font-size: 28px; color: var(--muted); text-align: center; margin-bottom: 26px; }

/* Title (two lines + underline) */
#cta-headline { z-index: 1; position: relative; text-align: center; max-width: 880px; margin-bottom: 30px; }
.cta-h-line { display: block; font-family: var(--font-body); font-size: 62px; font-weight: 700; line-height: 1.08; }
.cta-h-lime { color: var(--lime); }
.cta-h-ink  { color: var(--ink); }
#cta-underline { display: block; width: 420px; height: 16px; margin: 6px auto 0; }

/* Description */
#cta-desc { z-index: 1; font-family: var(--font-body); font-size: 26px; color: var(--muted); text-align: center; max-width: 760px; line-height: 1.35; margin-bottom: 36px; }
.cta-accent { color: var(--lime); font-weight: 600; }

/* Button */
#cta-btn { z-index: 1; display: inline-flex; align-items: center; gap: 14px; background: var(--lime); color: var(--on-lime); border-radius: 999px; padding: 24px 52px; font-family: var(--font-body); font-size: 25px; font-weight: 700; box-shadow: 0 0 0 1px rgba(201,242,77,0.35), 0 10px 44px rgba(201,242,77,0.42); margin-bottom: 30px; }
.cta-btn-icon { width: 22px; height: 22px; flex: 0 0 auto; }
#cta-btn-arrow { font-size: 26px; line-height: 1; }

/* Features row */
#cta-features { z-index: 1; display: inline-flex; align-items: center; gap: 18px; color: var(--muted); margin-bottom: 28px; }
.cta-feat { display: inline-flex; align-items: center; gap: 8px; font-family: var(--font-body); font-size: 18px; font-weight: 500; }
.cta-feat-icon { width: 18px; height: 18px; color: var(--lime); }
.cta-feat-sep { color: rgba(255,255,255,0.25); font-size: 18px; }

/* Footer */
#cta-domain { z-index: 1; font-family: var(--font-mono); font-size: 18px; color: var(--muted); letter-spacing: 0.04em; }
```

**No `@keyframes` anywhere** — the star twinkle is GSAP-owned (Lock 3/7). The button glow
is a static `box-shadow` (deterministic). Do not animate it via CSS.

---

## Init JS — gsap.set additions

Replace the current CTA init lines:
```javascript
gsap.set(["#cta-logo-wrap","#cta-headline","#cta-promise","#cta-subline","#cta-tagline","#cta-btn","#cta-domain"], { opacity: 0 });
gsap.set(["#cta-logo-wrap","#cta-headline"], { scale: 0.88 });
gsap.set("#cta-headline",     { y: 20 });
```
with:
```javascript
gsap.set(["#cta-logo-wrap","#cta-badge","#cta-subtext","#cta-headline","#cta-desc","#cta-btn","#cta-features","#cta-domain"], { opacity: 0 });
gsap.set(["#cta-logo-wrap","#cta-btn"], { scale: 0.88 });
gsap.set("#cta-headline", { y: 20 });
// Decor initial states
gsap.set("#cta-particles-layer", { opacity: 0 });
gsap.set("#cta-star", { scale: 0, transformOrigin: "center center", opacity: 0 });
// Underline: hide via stroke offset (draw-in later). Length measured at build.
```
(The `#cta-trail` and `#cta-underline-path` initial dash states are set in the timeline
build via `draw()`/inline `gsap.set` — see below — because they need `getTotalLength()`.)

---

## Timeline — replace the entire Scene 9 block

Current Scene 9 block (the `const ctaT = humanT + 5.2;` … `signalReady(tl);` section) →
replace with:

```javascript
// ════════════════════════════════════════════════════════════════════════════
// Scene 9 — CTA (redesigned)
// ════════════════════════════════════════════════════════════════════════════

const ctaT = humanT + 5.2;
tl.addLabel("cta", ctaT);

tl.set("#cta-group", { opacity: 1 }, ctaT);

// ── Decorative layer (starts with the scene, runs through) ──
// Trail draw-in (Lock 3: strokeDashoffset via GSAP, measured length)
const trailEl  = document.getElementById("cta-trail");
const trailLen = trailEl.getTotalLength();
gsap.set(trailEl, { strokeDasharray: trailLen, strokeDashoffset: trailLen });
tl.to(trailEl, { strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }, ctaT + 0.1);

// Star pops at the trail head, then a gentle GSAP twinkle (NOT CSS — Lock 7)
tl.to("#cta-star", { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, ctaT + 1.3);
tl.to("#cta-star", { scale: 1.12, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: -1 }, ctaT + 1.8);

// Rising lime particles (seeded, Lock 10) — full-frame subtle ambient
tl.to("#cta-particles-layer", { opacity: 1, duration: 0.6, ease: "none" }, ctaT + 0.2);
particleField(tl, "#cta-particles-layer", ctaT + 0.2, {
  count: 46, seed: "v3-cta", color: "201,242,77",
  drift: 48, sizeMin: 2, sizeMax: 5, opacityMax: 0.26, duration: 6.0
});

// ── Content reveals (each its own beat) ──
tl.to("#cta-logo-wrap", { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, ctaT + 0.2);
tl.to("#cta-badge",     { opacity: 1, duration: 0.4, ease: "settle" }, ctaT + 0.7);
tl.to("#cta-subtext",   { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 1.1);

// Title: two lines stagger, then underline draws under L2
tl.to("#cta-headline", { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, ctaT + 1.5);
const ulEl  = document.getElementById("cta-underline-path");
const ulLen = ulEl.getTotalLength();
gsap.set(ulEl, { strokeDasharray: ulLen, strokeDashoffset: ulLen });
tl.to(ulEl, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, ctaT + 2.1);

tl.to("#cta-desc",     { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 2.6);
tl.to("#cta-btn",      { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, ctaT + 3.1);
tl.to("#cta-features", { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 3.7);
tl.to("#cta-domain",   { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 4.2);

signalReady(tl);
```

**Notes:**
- `particleField` appends DOM children to `#cta-particles-layer` and tweens each on `tl`;
  it fades them out at `startT + duration - 0.8`. Set `duration: 6.0` so they live through
  the held end card (last reveal at `ctaT + 4.2`, film ends ~`ctaT + 6`).
- `getTotalLength()` runs inside `document.fonts.ready` (timeline build) — both SVG paths
  exist in the DOM by then. Safe.
- The star twinkle `repeat: -1` is excluded from the Lock 9 duration check and is GSAP-driven
  (not a CSS animation), so it passes the Lock 7 exporter gate. Do not convert it to CSS.

---

## Duration

Last reveal at `ctaT + 4.2` + ~1.8s hold → film end ≈ `ctaT + 6.0`.
Current film ends at 54.0 with reveals ending ~`ctaT + 3.05`, so `ctaT ≈ 48–49`.
New end ≈ **~57s**. Set `data-duration="57"` provisionally, then **re-measure** (verification 2).

---

## Order of operations

1. Replace `#cta-group` DOM block (logo kept; badge, subtext, two-line title + underline,
   desc, button w/ icon+arrow, features row, footer; decor svg + particles layer).
2. Replace the `── CTA ──` CSS block. Confirm no `@keyframes`.
3. Update init `gsap.set` lists (new IDs; star + particles initial states).
4. Replace the Scene 9 timeline block (decor draw/star/particles + staggered reveals).
5. Set `data-duration="57"` provisionally.

---

## Verification

1. **Draft export:**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --draft --name villain_v3_cta_draft --output export-video/
   ```
   Confirm on the contact sheet (100% frame):
   - Logo (lime), badge pill with ⚡, subtext, two-line title (L1 lime / L2 white + lime
     underline), description with lime "en segundos.", glowing button with icon + arrow,
     features row (Rápido · Seguro · Preciso), footer — all present, centered, legible.
   - Curved lime trail + twinkling star visible behind; subtle lime particles rising.
   - **No OVERFLOW FAIL**, **no CSS ANIMATION RUNNING** gate. If either fails: for overflow,
     reduce title `font-size`/`max-width`; for CSS-animation, you left a `@keyframes` in.

2. **Measure true duration** (Playwright: wait `motionReady`, read max finite `endTime`),
   set `data-duration` to `ceil`. Expected ~56–58s.

3. **Re-capture golden frames** (CTA appearance changed — required):
   ```
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --write
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --check --strict
   ```
   All frames must print "match golden."

4. **Orthography:**
   ```
   py scripts/orthography_check.py templates/scenes/scene-launch-villain-v3.html
   ```
   Clean — watch `Así`, `podés`, `Rápido`, `español`, `inglés`.

5. **Full quality export:**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --name villain_v3 --output export-video/
   ```
   Watch the contact sheet. Move the draft + superseded full export to `export-video/archive/`.

---

## Determinism checklist (Lock-by-Lock for this change)

- [ ] Trail + underline draw via GSAP `strokeDashoffset` on measured `getTotalLength()` — not SMIL, not CSS (Lock 3).
- [ ] Star twinkle is a GSAP `repeat: -1` tween — no CSS `@keyframes` (Lock 3/7).
- [ ] Button glow is static `box-shadow` — not animated in CSS (Lock 3).
- [ ] `particleField` uses `seededRandom("v3-cta:field")` — same positions every render (Lock 10).
- [ ] `repeat: -1` star tween excluded from duration check automatically (Lock 9).
- [ ] All `[data-copy]` elements fit inside safe zone — exporter overflow gate passes (Lock 6).
- [ ] No CDN scripts; reuses vendored GSAP + motion-lib only.
```