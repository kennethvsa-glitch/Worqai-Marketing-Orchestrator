# Plan: villain-v4 tweaks (post-build round 1)

Five edits to the **existing** `scene-launch-villain-v4.html` + `.css`. This is a tweak pass on a
shipped build — not a rebuild. The film exports today; these changes refine copy, pacing, one
visual bug, and the CTA logo.

**Files touched:**
- `templates/scenes/scene-launch-villain-v4.html` (copy + timeline + CTA logo)
- `templates/scenes/scene-launch-villain-v4.css` (notif sizing + CTA logo badge)
- `templates/assets/worqai_logo.png` (NEW — copied from `Ideation/worqai_logo.png`)

**No spec/manifest edits needed.** SFX, VO, captions, music ducking and cutdowns are all
**label-anchored**. The timeline shifts below move the labels; everything downstream re-resolves
automatically at `make_film` time. Do **not** touch `sounds_villain_v4.json`, `vo_villain_v4.json`,
or `films/launch-villain-v4.json`.

**Hard rule:** every animated property stays a GSAP tween (Lock 3). The timeline is paused +
`.time(t)` stepped — no CSS transitions. After edits, re-baseline goldens and re-export (the scene
changed, so `--skip-export` is **not** valid this round).

---

## Change 1 — Bigger, readable rejection notifications + copy fix

### 1a. Notifications bigger (CSS)

`scene-launch-villain-v4.css`, the notification stack block (currently ~lines 38–55).

```css
/* ── Notification stack (Scene 1 — three identical rejections) ── */
#notif-stack {
  position: absolute; top: 120px; left: var(--safe-x); right: var(--safe-x);   /* was top: 100px */
  display: flex; flex-direction: column; gap: 12px;                            /* was gap: 8px */
  z-index: 3; pointer-events: none;
}
.v4-notif {
  background: rgba(18,21,28,0.94); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 18px 22px;                                     /* was 14px 18px */
  display: flex; flex-direction: column; gap: 5px;                            /* was gap: 4px */
}
.v4-notif-sender {
  font-family: var(--font-mono); font-size: 14px; font-weight: 500;           /* was 12px */
  color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase;
}
.v4-notif-msg {
  font-family: var(--font-body); font-size: 23px; color: var(--ink); line-height: 1.5;  /* was 15px */
}
```

Rationale for `top: 120px`: the `.v4-notif-msg` elements carry `data-copy`, so the exporter's
safe-zone gate (Lock 6) checks `r.top < 120`. At `top: 120` + padding + sender line the first
message lands ~165px — clears the gate. **Verify on the draft contact sheet** that all three cards
are readable and the stack (ends ~560px) does not collide with the intro text (centered ~900px).
If 23px feels tight, 22px is the floor; do not go below the current 15px intent.

### 1b. "copy-paste" → "mensaje automatizado" (HTML)

`scene-launch-villain-v4.html` line 47 (`#intro-l1`). Change **both** the `data-copy` attribute
and the text node (they must match):

```html
<div class="intro-line" id="intro-l1" data-copy="Tres empresas. El mismo mensaje automatizado.">Tres empresas. El mismo mensaje automatizado.</div>
```

`splitWords("#intro-l1")` re-splits at render — more words is fine. No JS change.

---

## Change 2 — Hold "No eres tú." and "WorqAI lo hace en segundos." longer

Both holds extend Scene 1 / Scene 3, which pushes the **absolute-timed** Scenes 2 & 3 downstream.
Everything from the tailors onward is relative (`t1end → t2end → t3end → fanT → humanT → ctaT`) and
flows automatically once the first tailor start shifts.

### 2a. Add two hold constants

Inside the `document.fonts.ready.then(() => {` callback, near the top (before `SCAN_START` at
line 341), add:

```javascript
const W = 1.2;   // extra hold on "No eres tú."   (Scene 1 wound turn)
const C = 1.3;   // extra hold on "WorqAI lo hace en segundos."  (Scene 3 cheat code)
```

### 2b. SCAN_START picks up the Scene-1 shift

Line 341:

```javascript
const SCAN_START = 10.4 + W;   // was 10.4
```

`scanSweep` and the red spark `canvasParticles` both reference `SCAN_START` — no further edit there.

### 2c. Shift every absolute time in Scene 1 tail + Scene 2 + Scene 3

Apply `+ W` to the Scene-1 tail (l4 onward) and all of Scene 2 + the Scene-3 **entrance**.
Apply `+ W + C` to the Scene-3 **lift block** (resetUnderCover onward) and the first tailor start.

This is the complete list. Each entry is the position argument (last arg) of its tween/call.

| Line | What | Old position | New position |
|---|---|---|---|
| 546 | l4 reveal | `7.2` | `7.2 + W` |
| 547 | l5 reveal | `7.8` | `7.8 + W` |
| 550 | l4 exit | `8.6` | `8.6 + W` |
| 551 | l5 exit | `8.6` | `8.6 + W` |
| 552 | l3 fade | `8.6` | `8.6 + W` |
| 553 | intro-group hide | `8.85` | `8.85 + W` |
| 554 | dust → 0.15 | `8.6` | `8.6 + W` |
| 560 | demo-group set | `9.0` | `9.0 + W` |
| 561 | demo-group scale | `9.0` | `9.0 + W` |
| 565 | cv-card clip | `9.0` | `9.0 + W` |
| 566 | banner-generic | `9.2` | `9.2 + W` |
| 567 | bottom-panel | `9.8` | `9.8 + W` |
| 570 | vignette → 0.12 | `9.0` | `9.0 + W` |
| 583 | label `score_low` | `12.0` | `12.0 + W` |
| 584 | denom/score add | `12.0` | `12.0 + W` |
| 593 | pATS fromTo | `12.0` | `12.0 + W` |
| 594 | state "Bajo" add | `12.0` | `12.0 + W` |
| 596 | label `stamp` | `12.5` | `12.5 + W` |
| 597 | `stamp(...)` | `12.5` | `12.5 + W` |
| 598 | `caFlash(...)` | `12.5 + 0.16` | `12.5 + W + 0.16` |
| 600 | resumen-flag | `13.2` | `13.2 + W` |
| 601 | resumen-warn | `13.3` | `13.3 + W` |
| 602 | habilidades-flag | `13.5` | `13.5 + W` |
| 603 | habilidades-warn | `13.6` | `13.6 + W` |
| 604 | experiencia-flag | `13.8` | `13.8 + W` |
| 605 | flags 1-3 | `13.9` | `13.9 + W` |
| 607 | verify-btn | `14.2` | `14.2 + W` |
| 613 | label `cheat_code` | `16.9` | `16.9 + W` |
| 615 | turn-scene on | `16.2` | `16.2 + W` |
| 617 | turn-l1 | `16.9` | `16.9 + W` |
| 618 | turn-l2 | `18.2` | `18.2 + W` |
| 619 | turn-l3 | `19.1` | `19.1 + W` |
| 622 | dust → 0.30 | `16.9` | `16.9 + W` |
| 624 | `resetUnderCover(tl, 19.8)` | `19.8` | `19.8 + W + C` |
| 625 | stamp opacity 0 | `19.8` | `19.8 + W + C` |
| 626 | verify-btn 0 | `19.8` | `19.8 + W + C` |
| 627 | demo-group scale 1 | `19.8` | `19.8 + W + C` |
| 628 | banner-stat flex | `19.82` | `19.82 + W + C` |
| 631 | turn-scene off | `20.1` | `20.1 + W + C` |
| 632 | optimize-btn | `20.1` | `20.1 + W + C` |
| 633 | vignette → 0.06 | `20.5` | `20.5 + W + C` |
| 639 | `runTailor(tl, 21.0, 0, "slow")` | `21.0` | `21.0 + W + C` |

Lines 640–641 (`runTailor(tl, t1end, …)`, `runTailor(tl, t2end, …)`) are already relative — **leave them**.
Scene 7/8/9 (`fanT`, `humanT`, `ctaT`) are relative to `t3end` — **leave them** (Change 3 edits them separately).

> Net effect: "No eres tú." now holds ~1.2s longer before "Es el filtro." arrives; "WorqAI lo hace
> en segundos." holds ~2.0s before the overlay lifts. Verify both reads on the contact sheet.

---

## Change 3 — Fully clear the ghost CV during the human beat + rewrite human-l1

### 3a. CV must vanish completely (timeline)

Bug: during Scene 8 the demo group sits at ghost `opacity: 0.22` until `ctaT - 0.3`, so the old CV
is visible behind the "human" lines. The user wants it gone for that beat.

`scene-launch-villain-v4.html` line 662. The full fade currently fires at `humanT + 5.0 - 0.3`
(≈ `ctaT - 0.3`). Move it to **during the callback-notif entrance**, before the human lines appear:

```javascript
// Full fade — clear the CV before the human close lines (was: humanT + 5.0 - 0.3)
tl.to("#demo-group", { opacity: 0, duration: 0.6, ease: "none" }, humanT + 0.8);
```

Keep line 660 (ghost → 0.22 at `demoFadeT`) as-is: the CV dims to a ghost, then this fully clears it
by ~`humanT + 1.4`, before `#human-l1` reveals at `humanT + 1.5`. `#notif-callback` and `#human-close`
are independent elements (z-index 8, outside `#demo-group`), so fully fading the demo group does not
touch them.

### 3b. Rewrite the disliked line (HTML)

`scene-launch-villain-v4.html` line 69 (`#human-l1`). Replace text **and** `data-copy`:

```html
<div class="human-line" id="human-l1" data-copy="El problema nunca fue tu experiencia. Ni que no fueras suficiente.">El problema nunca fue tu experiencia. Ni que no fueras suficiente.</div>
```

Past-tense, consistent with "No eras tú. Era el filtro." and sets up the lime resolution
`#human-l2` ("Solo dejaste de ser invisible."). No VO change — `#human-l1` has no VO label (the VO
`human_close` line maps to `#human-l2`'s content). At 54px across the 968px column this wraps to ~3
lines; `#human-close` is bottom-aligned (`justify-content: flex-end; padding-bottom: 80px`), so it
grows upward — **confirm the top stays below safe-top (120px) on the contact sheet.** If it overflows,
shorten to: `"El problema nunca fue tu experiencia. Ni tu valor."`

---

## Change 4 — Real worqai logo on the CTA (replace the "W" square)

### Why a white plate is mandatory

`Ideation/worqai_logo.png` is RGBA, transparent background, **"worq" in black + "ai" in lime**. On
the dark CTA background (`#0C0E16`) the black half is nearly invisible. The logo must sit on a light
plate (standard brand treatment) so both halves read. Do **not** `filter: invert()` — it would turn
the lime "ai" magenta.

### 4a. Vendor the asset

Create `templates/assets/` and copy the logo in:

```
templates/assets/worqai_logo.png   ← copy of Ideation/worqai_logo.png
```

Reference path from `templates/scenes/` is `../assets/worqai_logo.png`. (Kept out of `vendor/` so
preflight's "vendor file not in VERSIONS.md" WARN doesn't fire.)

### 4b. HTML — swap the logo node, drop the separate wordmark

`scene-launch-villain-v4.html` lines 76–77. Replace:

```html
<div id="cta-logo">W</div>
<div id="cta-wordmark">worqai</div>
```

with (the image **is** the wordmark, so the text wordmark is removed):

```html
<div id="cta-logo"><img src="../assets/worqai_logo.png" alt="worqai" width="300"></div>
```

### 4c. CSS — white badge

`scene-launch-villain-v4.css` lines 268–269. Replace the `#cta-logo` / `#cta-wordmark` rules with:

```css
#cta-logo {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--paper);            /* white plate so black "worq" reads on the dark bg */
  border-radius: 22px; padding: 22px 30px;
  margin-bottom: 56px;                 /* preserves the spacing #cta-wordmark used to hold */
  position: relative; z-index: 1;
}
#cta-logo img { display: block; width: 300px; height: auto; }
```

(The logo PNG is 1258×895 with ~90% transparent margin, so the visible wordmark inside a 300px-wide
img is ~62px tall. Adjust `width` on the contact sheet if it reads too small/large.)

### 4d. JS — remove the wordmark/watermark-travel dependency

The watermark travel currently measures and targets `#cta-wordmark`, which no longer exists.
Simplest robust path: **keep the persistent top-left watermark, fade it out at the CTA**, and let the
image badge be the hero (no travel).

1. **Delete the travel measurement block** (lines 356–363, the `wmEl`/`wdEl`/`wmTX`/`wmTY`/`wmTScale`
   block) — it referenced `#cta-wordmark`.
2. **Init set** line 299 — remove `"#cta-wordmark"` from the array:
   ```javascript
   gsap.set(["#cta-logo","#cta-headline","#cta-promise","#cta-subline","#cta-btn","#cta-domain","#cta-origin"], { opacity: 0 });
   ```
3. **Replace the watermark travel** (lines 693–698 `tl.fromTo("#watermark", …)`) with a simple fade:
   ```javascript
   // Persistent watermark hands off to the hero logo — fade out as the badge appears
   tl.to("#watermark", { opacity: 0, duration: 0.4, ease: "none" }, ctaT + 0.2);
   ```
4. Line 691 (`#cta-logo` reveal at `ctaT`) stays — the white badge + image scale-pops in. Leave the
   `#cta-logo` scale `0.88` init (line 300).

> Optional polish (only if there's appetite, **not required**): retarget the travel to the badge
> centre and crossfade the mono "worqai" into the image. Higher risk (text→image size mismatch);
> skip for this pass.

---

## Change 5 — Bump `data-duration`

`W + C = 2.5s` added. Current real end ~49.5s → ~52s. Set a safe ceiling on line 2:

```html
<html data-duration="53" data-fps="60" data-name="villain-v4">
```

Verify the true end after edits (headless: read `gsap.globalTimeline` end time, or watch the tail of
the contact sheet) and trim `data-duration` to `ceil(end)` if you want it tight. The CTA tail
(`signalReady` + ember 4.5s window from `ctaT+0.2`) must fully fit before `data-duration`.

---

## QA gates (run in order — the law)

1. **Orthography** — `py scripts/orthography_check.py templates/scenes/scene-launch-villain-v4.html`
   → clean. (New copy has no diacritics, but confirm nothing else regressed.)
2. **Draft export + safe-zone gate** —
   `py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v4.html --name villain_v4 --draft --output export-video/`
   Must pass the safe-zone FAIL gate (catches bigger notifs, new human-l1, logo badge) and the
   running-CSS-animation scan. **Watch the draft contact sheet** — readable notif stack, "No eres tú."
   hold, "WorqAI lo hace en segundos." hold, CV fully gone behind the human lines, white logo badge
   with both halves visible, headline in safe zone.
3. **Golden re-baseline** (timeline changed) —
   `py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v4.html --write`
   then `--check --strict` → 15/15 match. If a label now lands on a tween boundary and a frame
   flickers, nudge that **label** ±0.3–0.5s (not the tween).
4. **Full export** —
   `py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v4.html --name villain_v4 --output export-video/`
   (Full quality, not `--draft`. Scene changed → no `--skip-export`.)
5. **Full film build** — `py scripts/make_film.py --film films/launch-villain-v4.json`
   SFX + music re-place against the shifted labels automatically; VO/captions still WARN-skip until
   `export-video/vo_villain_v4.mp3` exists. Confirm cutdowns (`hook-6s`, `15s-cut`) regenerate.
6. **CHANGELOG** — add a "villain-v4 tweaks round 1" entry summarising the five changes.

## Out of scope / unchanged

- VO take (`export-video/vo_villain_v4.mp3`) — still Kenneth's to generate; re-run with
  `--skip-export` after the asset exists.
- SFX / VO / manifest specs — untouched (label-anchored).
- v3 goldens — unaffected (different scene).
