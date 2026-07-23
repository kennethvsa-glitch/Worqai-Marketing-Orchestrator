# villain-v3 — Copy Rewrite Execution Plan (rev 2)

Executes `Ideation/2026-06-12-quantum-observer-villain-v3-copy-rewrite.md` against the
current `scene-launch-villain-v3.html`. This is a **copy + structural** rewrite across
6 scenes — not just text swaps. Scene 1 gains a beat, Scene 8 is fully replaced, several
elements need restyling and the timeline cascades longer (44s → ~48s).

**Base:** `export-video/video_villain_v3_2026-06-11.mp4` (44s · 60fps · 9:16).
CV demo internals (Scenes 4–6, the `tailors` array, `makeRunTailor`) are **untouched**.

## Files in play

- `templates/scenes/scene-launch-villain-v3.html` — DOM + timeline (main file)
- `templates/scenes/scene-launch-villain-v3.css` — styling
- `templates/motion-lib.js` — shared helpers (`morphSection`, `fanOut`,
  `resetUnderCover`, `splitWords`, `landWith`) — **read-only, do not edit**
- `export-video/golden/scene-launch-villain-v3.json` — golden hashes (re-capture at end)

## Determinism reminders (read `.claude/rules/motion-determinism.md`)

- Every animated property is a GSAP tween. No CSS transitions / class-toggle reveals.
- New text lines that use the masked word-reveal must be passed through `splitWords()`
  **before** the timeline is built and have their `.word-inner` pre-set to `y: "100%"`
  (see the existing `#intro-l1..l4` block at ~line 286–294).
- **Labels must sit ≥0.5s from any tween's start time** (the `signalReady` rounding bug).
  When you shift timings, nudge the label, not the tween.
- Line numbers below are approximate and **drift as you edit** — re-read the function/block
  before each change. Anchor on element IDs and helper names, not line numbers.
- Golden hashes will all change (timing moved) — that's expected. Re-capture at the end.

## Anti-slop (read `.claude/rules/anti-slop.md`)

All new copy is Spanish. None of it uses banned words. Keep it that way if you adjust
anything. The `data-copy` attribute must mirror the visible text exactly (the safe-zone
check in the exporter reads `[data-copy]`).

---

## DECISIONS TO CONFIRM (resolve before/while building — defaults chosen)

1. **Scene 8 length — condensed (4 lines) vs complete (5 lines).**
   → **Default: condensed (4 lines).** 5 lines in the available window is unreadable per
   the brief's own motion warning. Condensed still pushes the film to ~48s. If Kenneth
   wants the 5-line version, add the extra line and budget ~1s more.
2. **Scene 2 flags — scattered inline vs unified cold-log.**
   → **Default: reuse the 5 existing flag slots** (`#resumen-warn`, `#habilidades-warn`,
   `#flag-1/2/3`), restyle them to one consistent mono `✗ …` log style. Don't build a new
   log panel unless the contact sheet shows it reads as scattered noise.
3. **10.6× source line (Calibrator dissent).** Making the number bigger raises exposure.
   → **Default: add a small source sub-line** under the stat (e.g. `Fuente: dato interno
   WorqAI`) OR keep current size pending linkable data. Confirm with Kenneth before paid
   promotion. Don't ship a giant unsourced 10.6× to ads.
4. **Optional human beat in S8 (Calibrator).** CTA-B is colder; the brief suggests
   optionally returning one human line to S8. → **Default: follow the inversión copy
   as-written** (no extra line). Flag only if the cut feels cold on review.

---

## Cascade overview (the timing spine)

Two scenes get longer: **S1 (+~1.0s, new 6th beat)** and **S8 (+~2.2s, 2→4 lines)**.
Everything between cascades. Scenes 1–3 use **absolute** times (shift them by hand).
Scenes 4–9 are **relative** (`runTailor` returns `endT`; S7/8/9 derive from `t3end` +
offsets) so they cascade automatically once you move the tailor-1 start and widen the S8
offsets.

Recommended new absolute anchors (verify with `?dev=1` scrubber, adjust by eye):

| Beat | Was | New |
|---|---|---|
| S2 demo-group / cv-card reveal | 7.0 | **8.0** |
| `SCAN_START` (Scene 2 red scan) | 8.4 | **9.4** |
| `score_low` | 10.0 | **11.0** |
| `stamp` | 10.5 | **11.5** |
| Scene-2 flags | 11.2–11.9 | **12.2–12.9** |
| `verify-btn` | 12.2 | **13.2** |
| Scene-3 overlay up / `cheat_code` | 14.2 / 14.6 | **15.2 / 15.6** |
| turn lines | 14.6 / 15.9 / 16.8 | **15.6 / 16.9 / 17.8** |
| reset / overlay lift | 17.5 / 17.8 | **18.5 / 18.8** |
| Tailor 1 start | 18.2 | **19.2** |

Net: every Scene-2/3 absolute time **+1.0s**. Then S8 widening adds ~2.2s on top, landing
the film at **~48s**. Set `data-duration="48"` provisionally; trim to the measured end
after the draft (the prior round measured the true end with a Playwright snippet — reuse it).

---

## Fix 1 — Scene 1: rebuild as 6 beats, morph → "Nada."

**New copy (6 beats, morph is beats 3→4):**
```
40 postulaciones.                                          (l1)
0 respuestas.                                              (l2)
Y la pregunta que te persigue: "¿qué estoy haciendo mal?" (l3, muted)
   → Nada.                                                 (l3 morphs, lime, grande)
Nadie te rechazó.                                          (l4, ink)
Nadie te leyó.                                             (l5, lime, hold)
```

**DOM (`#intro-group`, ~lines 32–37):**
- `#intro-l1` text + `data-copy` → `40 postulaciones.`
- `#intro-l2` → `0 respuestas.`
- `#intro-l3` (keep `class="intro-line muted-intro"`) →
  `Y la pregunta que te persigue: "¿qué estoy haciendo mal?"`
- `#intro-l4` → `Nadie te rechazó.`
- **Add `#intro-l5`** after l4:
  ```html
  <div class="intro-line" id="intro-l5" data-copy="Nadie te leyó.">Nadie te leyó.</div>
  ```

**CSS (`scene-launch-villain-v3.css`):**
- `#intro-l3.turned` already styles the lime/large morph target ("Nada.") — keep it.
- Add a lime treatment for the held final line:
  ```css
  #intro-l5.turned-lime { color: var(--lime); }
  ```
  (Apply `.turned-lime` to `#intro-l5` via a `tl.add()` after its reveal, OR just give
  `#intro-l5` the lime color directly in CSS since it's lime from first paint — simpler.
  Pick one; if lime-from-paint, skip the class.)

**Timeline / init:**
- In the `document.fonts.ready` block, add `splitWords("#intro-l5");` next to the other
  four, and add `"#intro-l5 .word-inner"` to the `gsap.set(..., { y: "100%" })` list.
- Rebuild the Scene 1 block. Recommended timing (re-read the block first):
  ```javascript
  tl.to("#intro-l1 .word-inner", { y:"0%", duration:0.7, ease:"luxe", stagger:0.05 }, 0.4);
  tl.to("#intro-l2 .word-inner", { y:"0%", duration:0.6, ease:"luxe", stagger:0.05 }, 1.5);
  tl.to("#intro-l3 .word-inner", { y:"0%", duration:0.65, ease:"luxe", stagger:0.05 }, 2.6);

  // clear l1+l2 before the morph
  tl.to(["#intro-l1 .word-inner","#intro-l2 .word-inner"],
    { y:"100%", duration:0.3, ease:"mech" }, 3.5);

  // morph the question → "Nada." (lime via .turned)
  morphSection(tl, 4.0, "#intro-l3", "Nada.", 0.4, false);
  tl.add(() => {
    const el = document.getElementById("intro-l3");
    el.classList.remove("muted-intro"); el.classList.add("turned");
  }, 4.0 + 0.4 + 0.02);

  // two closing beats
  tl.to("#intro-l4 .word-inner", { y:"0%", duration:0.55, ease:"luxe", stagger:0.05 }, 5.0);
  tl.to("#intro-l5 .word-inner", { y:"0%", duration:0.55, ease:"luxe", stagger:0.05 }, 5.9);

  // hold, then exit ~7.6 (l1/l2 already gone)
  tl.to(["#intro-l3","#intro-l4"], { opacity:0, duration:0.22, ease:"mech" }, 7.6);
  tl.to("#intro-l5 .word-inner",   { y:"100%", duration:0.22, ease:"mech" }, 7.6);
  tl.to("#wa-notif", { opacity:0, duration:0.2, ease:"none" }, 7.4);
  tl.set("#intro-group", { opacity:0 }, 7.85);
  ```
- `wound` label can stay at 0.4.

**Watch-outs:**
- l3 question line is long — confirm it fits the safe zone on 9:16 and doesn't wrap to 3
  lines (`.intro-line` is 52px; the muted state is 38px). If it overflows, shrink
  `#intro-l3.muted-intro` font or shorten — but keep the quoted "¿qué estoy haciendo mal?".
- `#intro-l3` morph is `textContent`-based (not word-mask). After morph it's a plain lime
  line, exited by opacity (as today) — keep that, don't mask it.
- 6 beats in ~7s is tight (brief acknowledges). If it feels rushed on the draft, push the
  exit to ~8.0 and S2 start to ~8.5 — but then bump every downstream absolute by the same
  delta.

**Downstream:** Scene 2 start moves 7.0 → **8.0** (and the whole cascade in the table above).

---

## Fix 2 — Scene 2: dominant banner + cold log flags + DESCARTADO stamp

**Banner (`#banner-generic`, ~line 67):** make it the dominant line plus a smaller sub.
```html
<div class="cv-banner" id="banner-generic">
  <span id="banner-generic-head" data-copy="Así te lee el filtro.">Así te lee el filtro.</span>
  <span id="banner-generic-sub" data-copy="El software que las empresas usan para descartar candidatos — antes de que un humano vea tu CV.">El software que las empresas usan para descartar candidatos — antes de que un humano vea tu CV.</span>
</div>
```
CSS: make `#banner-generic-head` larger/bold (~24px, ink), `#banner-generic-sub` smaller
muted (~15px) on its own line (`display:block`). Confirm the sub doesn't overflow the
banner width / safe zone.

**Flags → cold sequential log.** Reuse the 5 existing slots; swap text + restyle to one
mono `✗` log style (Decision 2):
| Element | New text (`data-copy` must match) |
|---|---|
| `#resumen-warn` | `✗ palabras clave: 4 de 12` |
| `#habilidades-warn` | `✗ coincidencia con la vacante: baja` |
| `#flag-1` | `✗ formato: ilegible para el bot` |
| `#flag-2` | `✗ experiencia relevante: no detectada` |
| `#flag-3` | `✗ candidato no priorizado` |

CSS: `#flag-1/2/3` currently use the pill `.exp-flag` style — drop the pill for these and
match `.section-warn` (mono, ~12px, `--low`) so all five read as one cold log. Keep them
red. The existing reveal tweens (`11.2–11.9`, now `12.2–12.9`) already stagger them — good,
that's the "secuencial" feel. `resetUnderCover` already fades all five at reset — unchanged.

**Stamp:** `#rechazado-stamp` text + `data-copy` `RECHAZADO` → **`DESCARTADO`** (~line 83).
`DESCARTADO` is one char longer; `#rechazado-stamp` is mono 42px with `letter-spacing:0.12em`
— verify it still fits inside the card and doesn't trip the safe-zone check. Drop to 40px if
tight. (ID stays `#rechazado-stamp`; only the text changes.)

**Watch-out:** the "✗ formato: ilegible para el bot" claim is the Calibrator's flagged
compression — keep only if defensible. It's fine for organic; reconsider for paid.

---

## Fix 3 — Scene 3: cheat-code copy (locked, still 3 lines)

Text swaps only on `#turn-l1/l2/l3` (~lines 41–43), `data-copy` must match:
- `#turn-l1` → `Los que consiguen entrevistas no tienen mejor experiencia que tú.`
- `#turn-l2` (lime, unchanged style) → `Tienen un CV distinto para cada vacante.`
- `#turn-l3` (muted) → `Escrito en el idioma que el filtro entiende.`

**Watch-out:** `#turn-l1` is longer than before (`.turn-line` is 58px). Confirm it wraps to
at most 2 lines and clears the safe zone. No timeline change (just the +1.0 cascade shift
already in the table).

---

## Fix 4 — Scenes 4–6: no changes

`tailors` array, `makeRunTailor`, scores (92/94/93), the score-break on tailor 3 — all
untouched. Only the **start time** moves (18.2 → 19.2) as part of the cascade.

---

## Fix 5 — Scene 7: two-level stat banner

`#banner-stat` is the running header shown during the proof montage (revealed by
`resetUnderCover` at the new ~18.5, dismissed by `fanOut`). `#job-chip` is its fl/right
child — mind the alignment when the text grows taller.

**DOM (`#banner-stat`, ~lines 68–71):** split `#banner-stat-text` into two levels.
```html
<div id="banner-stat-copy">
  <span id="banner-stat-big" data-copy="10.6× más entrevistas.">10.6× más entrevistas.</span>
  <span id="banner-stat-sub" data-copy="Solo por adaptar el CV a cada vacante.">Solo por adaptar el CV a cada vacante.</span>
</div>
<div id="job-chip"><span id="job-chip-text">Analista de Seguridad</span></div>
```
CSS: `#banner-stat-big` large/bold (~28–32px, ink); `#banner-stat-sub` smaller muted
(~15px, block). Keep `#banner-stat` `display:flex; justify-content:space-between` so the
job-chip stays right-aligned; set `#banner-stat-copy` as the flex child holding both lines.
Per Decision 3, optionally add a tiny `#banner-stat-src` ("Fuente: …") under the sub.

**Caption (`#s7-caption`, ~line 149):** unchanged —
`Esto es lo que hacen los que sí consiguen entrevista.` Hold (~4s) already set by `fanOut`.

**Watch-out:** taller banner-stat must not push `#cv-panel` down into overflow during the
tailors. Check the tailor contact-sheet frames after this change.

---

## Fix 6 — Scene 8: replace "Human Consequence" with "La Inversión" (2 → 4 lines)

**New copy (condensed, Decision 1):**
```
Las empresas usan bots para descartarte.                  (l1, ink)
Nosotros invertimos el proceso.                           (l2, lime)
WorqAI reconstruye tu CV con todo lo que el bot busca.    (l3, ink)
Ellos tienen un algoritmo. Ahora tú también.              (l4, lime, grande)
```

**DOM (`#human-close`, ~lines 47–50):** keep the container; replace the two lines with four.
```html
<div id="human-close">
  <div class="human-line" id="human-l1" data-copy="Las empresas usan bots para descartarte.">Las empresas usan bots para descartarte.</div>
  <div class="human-line human-lime" id="human-l2" data-copy="Nosotros invertimos el proceso.">Nosotros invertimos el proceso.</div>
  <div class="human-line" id="human-l3" data-copy="WorqAI reconstruye tu CV con todo lo que el bot busca.">WorqAI reconstruye tu CV con todo lo que el bot busca.</div>
  <div class="human-line human-lime human-hero" id="human-l4" data-copy="Ellos tienen un algoritmo. Ahora tú también.">Ellos tienen un algoritmo. Ahora tú también.</div>
</div>
```

**CSS:** `.human-line` (54px) and `.human-lime` (lime) exist. Add a hero treatment for l4:
```css
#human-close .human-hero { font-size: 62px; line-height: 1.1; margin-bottom: 0; }
```
Confirm 4 lines + the 62px hero fit the safe zone (top 120 / bottom 200). If tight, drop
`.human-line` to ~48px for this scene or trim l3.

**Init:** add `#human-l3, #human-l4` to the init `gsap.set([...], { opacity:0, y:18 })`
list (the line currently sets `["#human-l1","#human-l2"]`, ~line 269).

**Timeline (replace the Scene 8 block, ~lines 574–579):**
```javascript
tl.addLabel("human_close", humanT + 0.5);
tl.to("#human-close", { opacity:1, duration:0.35, ease:"none" }, humanT);
tl.to("#human-l1", { opacity:1, y:0, duration:0.5, ease:"luxe" }, humanT + 0.2);
tl.to("#human-l2", { opacity:1, y:0, duration:0.5, ease:"luxe" }, humanT + 1.0);
tl.to("#human-l3", { opacity:1, y:0, duration:0.5, ease:"luxe" }, humanT + 1.8);
tl.to("#human-l4", { opacity:1, y:0, duration:0.55, ease:"luxe" }, humanT + 2.7);
tl.to("#human-close", { opacity:0, duration:0.4, ease:"power2.out" }, humanT + 4.8);
```
Keep `demoFadeT` fading `#demo-group` to opacity 0 (the 2026-06-11 fix — the CV must be
**fully** gone behind this scene; do not reintroduce the 0.22 ghost).

**Downstream:** widen the CTA offset. Change `const ctaT = humanT + 3.0;` → **`humanT + 5.2;`**
so the CTA starts after the longer S8. (`demoFadeT`/`humanT` keep their `fanT + 3.4`/`+4.2`
offsets — the brief's Fix-4 dwell stays.) Net S8 adds ~2.2s.

**Watch-out:** the `human_close` label at `humanT + 0.5` must not coincide with the
`humanT + 0.2`/`+1.0` reveals within 0.5s — `+0.5` sits between, OK, but re-check after any
nudge.

---

## Fix 7 — Scene 9: CTA Version B ("El número oculto")

**New copy (going with B):**
```
Te descartaron en segundos.                                       (line 1)
Sin siquiera llegar a un humano.                                  (line 2)
Así que les copiamos el filtro y lo pusimos de tu lado.         (line 3, lime, grande)
[ Analiza mi CV gratis ]                                          (button, unchanged)
worqai.io · español e inglés                                      (domain, unchanged)
```

The reveal order in the timeline is headline → promise → subline → btn → domain, which
matches lines 1→2→3→btn→domain. Map onto existing IDs and **invert the visual hierarchy**
(line 1 small, line 3 the lime hero):

**DOM (`#cta-group`, ~lines 56–59):**
- `#cta-headline` → `Te descartaron en segundos.`
- `#cta-promise` → `Sin siquiera llegar a un humano.`
- `#cta-subline` → `Así que les copiamos el filtro — y lo pusimos de tu lado.`
- `#cta-btn` (`Analiza mi CV gratis`) and `#cta-domain` (`worqai.io · español e inglés`) —
  unchanged.

**CSS swap (the tricky part):** today `#cta-headline` is the 62px hero and `#cta-subline`
is 28px muted. Version B wants **line 3 (`#cta-subline`) as the lime hero**:
- `#cta-headline` → ~38px, ink (lead-in, not hero). It also has an init `scale:0.88, y:20`
  and a "pop" reveal — fine to keep, or simplify to a plain fade to match the calmer lead-in.
- `#cta-promise` → ~30px, muted.
- `#cta-subline` → **~56px, lime, line-height 1.1, max-width ~860px** (the punchline).
  Add bottom spacing before the button.
- Keep the init `gsap.set` list and the staggered reveal times (`ctaT`, `+0.22`, `+0.30`,
  `+0.75`, `+1.45`, `+2.05`, `+2.65`) — they already read in order. If line 3 needs more
  emphasis, give `#cta-subline` a `scale` pop like the headline has now.

**Watch-out:** line 3 is long — at 56px confirm it wraps to ≤2 lines inside `max-width` and
clears the safe zone, and that the button still fits below. The `[ ]` brackets in the brief
are notation, not literal — the button label stays `Analiza mi CV gratis`.

---

## Verification (run after ALL fixes)

1. **Draft pass (fast, eyeball timing of every scene):**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --draft --name villain_v3_rev2_draft --output export-video/
   ```
   Read the contact sheet. Confirm:
   - S1: 6 beats land; "Nada." morph reads; "Nadie te rechazó. / Nadie te leyó." holds.
   - S2: dominant "Así te lee el filtro." + sub; 5 `✗` log flags sequential; **DESCARTADO** stamp fits.
   - S3: 3 lines, no overflow on the longer line 1.
   - S4–6: unchanged (scores 23→92→94→93, tailor-3 hesitation intact).
   - S7: two-level "10.6× más entrevistas." banner; job-chip still right-aligned.
   - S8: 4 lines readable, "Ellos tienen un algoritmo. Ahora tú también." as lime hero; CV fully gone behind.
   - S9: Version B; line 3 is the lime hero; button + domain intact.
   - No FAIL gates (safe-zone overflow / running CSS animation).

2. **Measure the true timeline end and set `data-duration`** (reuse the Playwright snippet
   from the prior round — wait on `window.motionReady`, read max finite `endTime()`), then
   set `data-duration` to the ceil (expected ~48). Re-run draft if you change it.

3. **Re-capture golden hashes** (timing changed — old baseline is stale, expected):
   ```
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --write
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --check --strict
   ```
   Must print "All N frames match golden." If a label flickers (landed on a tween
   boundary), nudge the **label** ±0.3–0.5s and re-write.

4. **Full quality export (60fps):**
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --name villain_v3 --output export-video/
   ```
   Review the final contact sheet before shipping. Move any intermediate drafts to
   `export-video/archive/` (final MP4 + contact sheet stay in `export-video/` root).

## Order of operations

Do the cascade-movers first so timing settles once, then the localized swaps:
1. **Fix 1** (S1 +1 beat, sets the +1.0 cascade) → shift all S2/S3 absolutes + tailor-1 start.
2. **Fix 6** (S8 expansion, sets `ctaT = humanT + 5.2`).
3. **Fix 2, 3, 5, 7** (localized copy + CSS; no further timing cascade).
4. Set `data-duration`, re-capture golden, full export.

Re-read each block before editing — earlier edits move the line numbers cited here.
Don't re-capture golden until all fixes are in.
```
