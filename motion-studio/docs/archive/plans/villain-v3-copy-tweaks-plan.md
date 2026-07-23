# villain-v3 — Tweaks Plan (rev 3)

Executes against the current `scene-launch-villain-v3.html` (rev 2, 48s, 60fps).
Base export: `export-video/video_villain_v3_2026-06-12.mp4`.

**Files in play:**
- `templates/scenes/scene-launch-villain-v3.html` — DOM + timeline
- `templates/scenes/scene-launch-villain-v3.css` — styling
- `templates/motion-lib.js` — **read-only, do not edit**
- `export-video/golden/scene-launch-villain-v3.json` — re-capture at end

**Read the determinism rules before touching anything:**
- `.claude/rules/motion-determinism.md`
- `.claude/rules/anti-slop.md`
- `.claude/rules/output-conventions.md`

---

## Summary of changes

| # | Scene | What changes |
|---|---|---|
| A | S1 | Remove wa-notif banner entirely |
| B | S1 | Hold the question longer before morph; add 7th beat "El filtro te descartó sin llegar a un humano."; extend exit dwell |
| C | S2/S3 | Cascade all absolute times +2.5s to absorb S1 extension |
| D | S3 | Leave cheat-code overlay on screen 2.5s longer |
| E | S7 | Banner stat: one line instead of stacked |
| F | S8 | Increase line spacing so text breathes |
| G | S9 | Remove dash from punchline; add tagline; replace W-square with real logo PNG |

---

## Cascade overview

S1 now exits at **~10.3s** (was 7.85s). Apply **+2.5s** to every S2/S3 absolute.
S3 dwell adds **+2.5s** (user request). Apply an additional +2.5s to reset/lift/tailor-1.

Net total addition: ~5s → provisional `data-duration="54"`.
Measure the actual end after draft and update before full export.

New absolute anchors:

| Beat | Rev2 | Rev3 |
|------|------|------|
| S2 demo-group / cv-card reveal | 8.0 | **10.5** |
| banner-generic | 8.2 | **10.7** |
| bottom-panel | 8.8 | **11.3** |
| `SCAN_START` | 9.4 | **11.9** |
| `score_low` | 11.0 | **13.5** |
| `stamp` | 11.5 | **14.0** |
| Flags start | 12.2–12.9 | **14.7–15.4** |
| `verify-btn` | 13.2 | **15.7** |
| overlay up | 15.2 | **17.7** |
| `cheat_code` label | 15.6 | **18.1** |
| `turn-l1` | 15.6 | **18.1** |
| `turn-l2` | 16.9 | **19.4** |
| `turn-l3` | 17.8 | **20.3** |
| reset / lift | 18.5 / 18.8 | **21.0 / 21.3** |
| reset / lift (after dwell +2.5) | — | **23.5 / 23.8** |
| optimize-btn | 18.8 | **23.8** |
| Tailor 1 start | 19.2 | **24.5** |

---

## Fix A — Remove wa-notif entirely

**DOM** (~lines 21–29): delete the entire `#wa-notif` block:
```html
<!-- WhatsApp notification ... -->
<div id="wa-notif">
  ...
</div>
```

**Init JS**: delete the line:
```javascript
gsap.set("#wa-notif", { opacity: 0, y: -8 });
```

**Timeline**: delete both `#wa-notif` tween lines in the old S1 block:
```javascript
tl.to("#wa-notif", { opacity: 1, y: 0, duration: 0.5, ease: "luxe" }, 0.1);
// ...
tl.to("#wa-notif", { opacity: 0, duration: 0.2, ease: "none" }, 7.4);
```

**CSS** (~lines 25–43): delete the entire `#wa-notif`, `#wa-icon`, `#wa-body`, `#wa-sender`, `#wa-msg`, `#wa-time` block.

---

## Fix B — Scene 1: extend hold + 7th beat

**New S1 copy (7 beats):**
```
40 postulaciones.                                          (l1, ink)
0 respuestas.                                              (l2, ink)
Y la pregunta que te persigue: "¿qué estoy haciendo mal?" (l3, muted)
   → Nada.                                                 (l3 morphs, lime)
Nadie te rechazó.                                          (l4, ink)
Nadie te leyó.                                             (l5, lime)
El filtro te descartó sin llegar a un humano.              (l6, muted, smaller)
```

**DOM** (`#intro-group`): add `#intro-l6` after `#intro-l5`:
```html
<div class="intro-line intro-kicker" id="intro-l6" data-copy="El filtro te descartó sin llegar a un humano.">El filtro te descartó sin llegar a un humano.</div>
```

**CSS** (`scene-launch-villain-v3.css`): add a style for the kicker:
```css
.intro-kicker { font-size: 34px; font-weight: 400; color: var(--muted); margin-bottom: 0; }
```

**Init JS** — `splitWords` block: add `splitWords("#intro-l6")` and add `"#intro-l6 .word-inner"` to the `gsap.set([...], { y: "100%" })` list.

**Timeline — replace the entire Scene 1 block** with:
```javascript
tl.addLabel("wound", 0.4);

tl.to("#bg-grid", { opacity: 1, duration: 0.6, ease: "none" }, 0.0);

tl.to("#intro-l1 .word-inner", { y: "0%", duration: 0.7, ease: "luxe", stagger: 0.05 }, 0.4);
tl.to("#intro-l2 .word-inner", { y: "0%", duration: 0.6, ease: "luxe", stagger: 0.05 }, 1.5);
tl.to("#intro-l3 .word-inner", { y: "0%", duration: 0.65, ease: "luxe", stagger: 0.05 }, 2.6);

// Longer hold on the question before clearing
tl.to(["#intro-l1 .word-inner", "#intro-l2 .word-inner"],
  { y: "100%", duration: 0.3, ease: "mech" }, 4.8);

// morph the question → "Nada." (lime via .turned)
morphSection(tl, 5.3, "#intro-l3", "Nada.", 0.4, false);
tl.add(() => {
  const el = document.getElementById("intro-l3");
  el.classList.remove("muted-intro"); el.classList.add("turned");
}, 5.3 + 0.4 + 0.02);

// three closing beats
tl.to("#intro-l4 .word-inner", { y: "0%", duration: 0.55, ease: "luxe", stagger: 0.05 }, 6.3);
tl.to("#intro-l5 .word-inner", { y: "0%", duration: 0.55, ease: "luxe", stagger: 0.05 }, 7.2);
tl.to("#intro-l6 .word-inner", { y: "0%", duration: 0.5,  ease: "luxe", stagger: 0.05 }, 8.3);

// hold 1.5s on all, then exit
tl.to(["#intro-l3", "#intro-l4"], { opacity: 0, duration: 0.22, ease: "mech" }, 10.0);
tl.to(["#intro-l5 .word-inner", "#intro-l6 .word-inner"],
  { y: "100%", duration: 0.22, ease: "mech" }, 10.0);
tl.set("#intro-group", { opacity: 0 }, 10.3);
```

**Watch-outs:**
- `#intro-l3` morph is textContent-based (not word-mask). After morph it's a plain lime line exited by opacity — keep that, don't mask it.
- l6 question line is long (38 chars at 34px) — confirm it fits on one line inside the safe zone.
- No `#wa-notif` tweens in this block (they've been removed in Fix A).

---

## Fix C — Cascade S2/S3 absolutes +2.5s

Apply +2.5s to every hardcoded number in Scene 2 and Scene 3. Using the anchor table above:

**Scene 2 block** — find and replace all these time values:
```javascript
// OLD → NEW
}, 8.0);   →   }, 10.5);   // demo-group set + cv-card reveal (two places)
}, 8.2);   →   }, 10.7);   // banner-generic
}, 8.8);   →   }, 11.3);   // bottom-panel
const SCAN_START = 9.4;  →  const SCAN_START = 11.9;
tl.addLabel("score_low", 11.0);  →  tl.addLabel("score_low", 13.5);
... 11.0);  →  ... 13.5);         // pATS fromTo + stateEl callback (two lines)
tl.addLabel("stamp", 11.5);  →   tl.addLabel("stamp", 14.0);
stamp(tl, "#rechazado-stamp", "#cv-card", 11.5);  →  stamp(..., 14.0);
}, 12.2);  →  }, 14.7);   // resumen-flag
}, 12.3);  →  }, 14.8);   // resumen-warn
}, 12.5);  →  }, 15.0);   // habilidades-flag
}, 12.6);  →  }, 15.1);   // habilidades-warn
}, 12.8);  →  }, 15.3);   // experiencia-flag
}, 12.9);  →  }, 15.4);   // flag-1/2/3
}, 13.2);  →  }, 15.7);   // verify-btn
```

**Scene 3 block (base shift only, before dwell):**
```javascript
tl.addLabel("cheat_code", 15.6);  →  tl.addLabel("cheat_code", 18.1);
}, 15.2);  →  }, 17.7);   // overlay up
}, 15.6);  →  }, 18.1);   // turn-l1
}, 16.9);  →  }, 19.4);   // turn-l2
}, 17.8);  →  }, 20.3);   // turn-l3
```

---

## Fix D — Scene 3 dwell +2.5s

The cheat-code lines now appear at 18.1/19.4/20.3. User wants them to linger. Push the reset and lift 2.5s later than Fix C's shifted values:

```javascript
// After Fix C the reset/lift were at 21.0/21.3 — push further to 23.5/23.8
resetUnderCover(tl, 23.5);
tl.set("#rechazado-stamp", { opacity: 0 }, 23.5);
tl.set("#verify-btn",      { opacity: 0 }, 23.5);
tl.set("#demo-group",      { scale: 1.0 }, 23.5);

tl.to("#turn-scene",  { opacity: 0, duration: 0.45, ease: "power2.out" }, 23.8);
tl.to("#optimize-btn",{ opacity: 1, duration: 0.4,  ease: "luxe" },       23.8);

// Tailor 1 start
const t1end = runTailor(tl, 24.5, 0, "slow");   // was 19.2 → now 24.5
```

---

## Fix E — Banner stat: single line

**DOM** (`#banner-stat-copy` block, ~line 74–79): replace the two-child structure with one span:
```html
<div class="cv-banner" id="banner-stat">
  <span id="banner-stat-text" data-copy="10.6× más entrevistas. Solo por adaptar el CV a cada vacante.">10.6× más entrevistas. Solo por adaptar el CV a cada vacante.</span>
  <div id="job-chip"><span id="job-chip-text">Analista de Seguridad</span></div>
</div>
```

**CSS** — remove the `#banner-stat-copy`, `#banner-stat-big`, `#banner-stat-sub` rules. Replace with:
```css
#banner-stat-text { flex: 1 1 auto; font-size: 19px; font-weight: 600; color: var(--ink); }
```

**Watch-out:** `#banner-stat` is `display: none` at the time of the overflow check, so `data-copy` on `#banner-stat-text` will trigger the false-left-overflow bug (r.left = 0 < 56). **Remove `data-copy` from `#banner-stat-text`** — the overflow check cannot validate hidden elements anyway. Keep `data-copy` on visible elements only.

---

## Fix F — Scene 8 line spacing

The four lines feel crowded at 54px. Give them more room:

**CSS** (`scene-launch-villain-v3.css`):
```css
/* Increase base line spacing */
.human-line { font-size: 48px; font-weight: 600; line-height: 1.2; color: var(--ink); margin-bottom: 36px; }
/* Hero line stays larger; add top breathing room */
#human-close .human-hero { font-size: 62px; line-height: 1.1; margin-top: 8px; margin-bottom: 0; }
```

No timeline change needed.

---

## Fix G — CTA: dash removal, tagline, real logo

### G1 — Remove dash from punchline

**DOM** `#cta-subline` (line ~61): change text and `data-copy`:
```html
<div id="cta-subline" data-copy="Así que les copiamos el filtro y lo pusimos de tu lado.">Así que les copiamos el filtro y lo pusimos de tu lado.</div>
```

### G2 — Add tagline below punchline

**DOM** — add `#cta-tagline` between `#cta-subline` and `#cta-btn`:
```html
<div id="cta-tagline" data-copy="con WorqAI podés adaptar tu CV a cualquier vacante en segundos.">con WorqAI podés adaptar tu CV a cualquier vacante en segundos.</div>
```

**CSS:**
```css
#cta-tagline { font-family: var(--font-body); font-size: 22px; color: var(--muted); text-align: center; max-width: 700px; margin-bottom: 44px; }
```

**Init JS** — add `#cta-tagline` to the opacity-0 gsap.set:
```javascript
gsap.set(["#cta-logo","#cta-wordmark","#cta-headline","#cta-promise","#cta-subline","#cta-tagline","#cta-btn","#cta-domain"], { opacity: 0 });
```

**Timeline** — insert `#cta-tagline` reveal and shift btn/domain:
```javascript
tl.to("#cta-subline",  { opacity: 1, duration: 0.4, ease: "none" },              ctaT + 1.45);
tl.to("#cta-tagline",  { opacity: 1, duration: 0.4, ease: "none" },              ctaT + 1.90);  // NEW
tl.to("#cta-btn",      { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, ctaT + 2.45);  // was 2.05
tl.to("#cta-domain",   { opacity: 1, duration: 0.4, ease: "none" },              ctaT + 3.05);  // was 2.65
```

### G3 — Replace W-square logo with real WorqAI PNG

The logo PNG is at `Ideation/worqai_logo.png` (white background, horizontal wordmark).
Relative path from `templates/scenes/` → `../../Ideation/worqai_logo.png`.

**DOM** — replace `#cta-logo` div and `#cta-wordmark` div with a single logo wrapper:
```html
<div id="cta-group">
  <div id="cta-logo-wrap">
    <img id="cta-logo-img" src="../../Ideation/worqai_logo.png" alt="WorqAI">
  </div>
  <!-- remove #cta-wordmark entirely — logo PNG already has the wordmark -->
  <div id="cta-headline" ...>...</div>
  ...
</div>
```

**CSS** — replace `#cta-logo` and `#cta-wordmark` rules with:
```css
#cta-logo-wrap {
  background: #ffffff; border-radius: 20px;
  padding: 22px 52px; margin-bottom: 44px;
}
#cta-logo-img { width: 260px; display: block; }
```

**Init JS** — update gsap.set references:
- Replace `"#cta-logo"` → `"#cta-logo-wrap"` everywhere it appears in `gsap.set`
- Remove `"#cta-wordmark"` from all gsap.set lists (element no longer exists)
- Keep `gsap.set(["#cta-logo-wrap","#cta-headline"], { scale: 0.88 })` — same pop reveal

**Timeline** — update CTA reveal block:
```javascript
tl.to("#cta-logo-wrap", { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, ctaT);
// DELETE the "#cta-wordmark" tween entirely — no wordmark div
tl.to("#cta-headline",  { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "power3.out" }, ctaT + 0.30);
tl.to("#cta-promise",   { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 0.75);
tl.to("#cta-subline",   { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 1.45);
tl.to("#cta-tagline",   { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 1.90);
tl.to("#cta-btn",       { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, ctaT + 2.45);
tl.to("#cta-domain",    { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 3.05);
```

**Watch-out:** `#cta-logo-wrap` has `data-copy` nowhere, so no overflow concern. `#cta-tagline` is inside `#cta-group` which is `opacity: 0` but NOT `display: none` — its bounding rect is valid. Verify it doesn't push `#cta-btn` into the safe-bottom zone.

---

## Order of operations

1. **Fix A** — Remove wa-notif (DOM, CSS, JS init, timeline)
2. **Fix B** — Rebuild S1 timeline + add l6 (DOM, CSS, JS init, timeline)
3. **Fix C** — Shift all S2/S3 absolutes +2.5s
4. **Fix D** — Push S3 reset/lift/tailor-1 further +2.5s for dwell
5. **Fix E** — Banner stat single line (DOM + CSS)
6. **Fix F** — S8 spacing (CSS only)
7. **Fix G** — CTA tweaks (DOM, CSS, init JS, timeline)
8. Set `data-duration="54"` provisionally

---

## Verification

1. **Draft export:**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --draft --name villain_v3_rev3_draft --output export-video/
   ```
   Read the contact sheet and confirm:
   - S1: 7 beats land; question holds; "Nada." morph reads; closing trio holds before exit; no wa-notif.
   - S2: CV appears at ~10.5s; banner, score, DESCARTADO stamp, ✗ flags all visible; timing feels right.
   - S3: Cheat-code lines hold long enough; all 3 lines readable.
   - S4–6: Tailors intact; job chip single-line banner shows correctly.
   - S7: Fan-out + caption.
   - S8: 4 lines with generous spacing; hero line reads clearly.
   - S9: No dash in punchline; tagline visible; real logo (white pill on dark bg) appears; no W square.
   - No OVERFLOW FAIL / CSS ANIMATION gates.

2. **Measure true duration** using Playwright snippet (wait for motionReady, read max finite endTime), set `data-duration` to ceil. Expected: ~53–55s.

3. **Re-capture golden frames:**
   ```
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --write
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --check --strict
   ```
   All N frames must print "match golden."

4. **Full quality export:**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --name villain_v3 --output export-video/
   ```
   Review contact sheet. Move draft files to `export-video/archive/`.
