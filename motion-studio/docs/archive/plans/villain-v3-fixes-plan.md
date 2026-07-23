# Villain-v3 — Fixes Plan (round 2)

Six tweaks to `scene-launch-villain-v3.html` (46s film) after the first full export
(`export-video/video_villain_v3_2026-06-11.mp4`). All changes are timing/visual polish —
no new scenes. Apply in order; line numbers drift as you edit, so re-read the function
before each change.

## Files in play

- `templates/scenes/scene-launch-villain-v3.html` — timeline + DOM (the main file)
- `templates/scenes/scene-launch-villain-v3.css` — styling
- `templates/motion-lib.js` — shared helpers (`morphSection`, `scanSweep`, `fanOut`, etc.)
- `export-video/golden/scene-launch-villain-v3.json` — golden hashes (will need re-capture)

## Determinism reminders (read `.claude/rules/motion-determinism.md`)

- Every animated property is a GSAP tween. No CSS transitions / class-toggle reveals.
- **Labels must sit ≥0.5s away from any tween's start time.** A label placed exactly on a
  tween boundary is non-deterministic (the `signalReady` `Math.round(v*1000)` truncation bug
  we already hit on `human_close`). When timing shifts below move a label onto a boundary,
  nudge the label, not the tween.
- These edits shift downstream timing. **Golden hashes will all change — that's expected.**
  Re-capture at the end (see Verification).

---

## Fix 1 — Scene 1: clear the first lines before the "No eres tú / Es el filtro" punchline, hold it longer

**Symptom:** When `intro-l3` morphs to "No eres tú." (lime) and `intro-l4` "Es el filtro."
slides up, the opening lines `intro-l1` ("Mandaste el mismo CV a 40 vacantes.") and
`intro-l2` ("Cero respuestas.") are **still on screen**. The punchline should land alone, and
hold a beat longer before Scene 2.

**Where:** `scene-launch-villain-v3.html`, Scene 1 block, currently lines ~444–465.

**Current behavior:**
- 0.4 / 1.6 / 2.7 — l1, l2, l3 reveal (word masks)
- 4.0 — `morphSection` l3 → "No eres tú." then `.turned` (lime) at 4.42
- 4.7 — l4 "Es el filtro." reveals
- 5.8 — l1, l2, l4 masks snap shut + l3 fades (everything exits together)
- 6.05 — `#intro-group` opacity 0

**Change:**
1. **Clear l1 + l2 as the punchline forms.** Add a mask-close on `#intro-l1 .word-inner` and
   `#intro-l2 .word-inner` at **~3.7** (just before the l3 morph at 4.0), so by the time
   "No eres tú." resolves only the punchline pair (l3 + l4) is visible:
   ```javascript
   tl.to(["#intro-l1 .word-inner", "#intro-l2 .word-inner"],
     { y: "100%", duration: 0.3, ease: "mech" }, 3.7);
   ```
2. **Push the punchline reveal + hold later.** Shift the l3 morph and the `.turned` swap and
   the l4 reveal each by ~+0.4s (morph 4.0→4.4, turned 4.42→4.82, l4 4.7→5.1), and push the
   final exit from 5.8 to **~6.8**, with `#intro-group` opacity-0 at **~7.05**. That buys ~1s
   more dwell on "No eres tú. / Es el filtro."
3. **Remove l1/l2 from the 5.8 exit tween** (they're already gone) — leave only l4's mask and
   l3's fade in that exit step.

**Downstream:** Scene 2 currently starts at 6.0. Pushing the intro exit to ~6.8 means Scene 2
must start later too — see Fix 2, which already wants Scene 2 to breathe. Slide the entire
Scene 2 block start from 6.0 → **~7.0** (shift every absolute time in the Scene 2 block by
+1.0s: the `#demo-group` set/tween, `#cv-card` reveal, banners, `scanSweep` SCAN_START,
score, stamp, flags, verify-btn). Easiest: bump the `SCAN_START` constant (line ~299) and all
Scene-2 absolute times together. Keep `cheat_code` overlay (Scene 3) starting after the new
Scene 2 end.

> Note: `SCAN_START = 7.4` and `SCAN_DUR = 0.9` (line ~299) feed `kwSchedule`. If you shift
> Scene 2 by +1.0s, set `SCAN_START = 8.4`.

**Watch-out:** `intro-l3` is reused (muted → turned). Its exit at 5.8 is an opacity fade, not
a mask. Keep that.

---

## Fix 2 — Scene 2: let the "bad CV" hold longer at the end

**Symptom:** After the red flags + `RECHAZADO` stamp + "Verificar" button appear, the
cheat-code overlay (Scene 3) arrives too quickly. The villain (broken CV, score 23) should
sit a beat longer so the low score registers.

**Where:** end of Scene 2 / start of Scene 3 — `verify-btn` reveal (~line 505) and the
`#turn-scene` overlay (~line 514).

**Change:** Add **~1.2s** of hold between the verify-btn reveal and the cheat-code overlay.
After Fix 1's +1.0s shift, the verify-btn lands ~12.2. Push the Scene 3 overlay start and all
its child times by **+1.2** beyond that (overlay 12.0→~14.2 in pre-shift terms; compute from
the actual post-Fix-1 verify-btn time + ~1.0s dwell). Net effect: roughly +2.2s of extra time
before the cheat-code turn vs. the current cut.

**Downstream:** every absolute time from Scene 3 onward shifts by the same total. The tailors,
fan-out, human close, and CTA are all built from `runTailor`'s returned `endT` chain and
`fanT`/`humanT`/`ctaT` offsets, so they cascade automatically **once you move the Scene 3
overlay start and the `runTailor(tl, 16.0, …)` start**. Update that `16.0` literal (line ~536)
to the new Scene-4 start time.

**Update `data-duration`** (line 2) if the film runs past 46s — bump to e.g. `48` or `49`.
The exporter reads `data-duration`. Check the final timeline end via the dev scrubber
(`?dev=1`) and round up.

---

## Fix 3 — Tailors: morph the CV *as the lime scan passes*, not a waterfall (all 3 tailors)

**Symptom:** After "Optimizar con WorqAI" is clicked, the lime scan bar does a quick sweep,
then the 9 sections blur-swap top-to-bottom on a fixed stagger (`gap`) that's **disconnected**
from the bar. It reads as a waterfall. It should read as: *the bar passes a section → that
section rewrites under it.* This is the deferred "position-driven scan" refinement, now wanted
for all three tailors.

**Where:** `makeRunTailor` in `scene-launch-villain-v3.html`, lines ~314–428. Specifically the
lime scan (line ~339–345) and the 9 `morphSection`/`morphSkills` calls (lines ~353–363).

**Approach — tie each morph to the bar's vertical position (mirror the Scene 2 `kwSchedule`):**

1. **Measure section fractions once, after `fonts.ready`, before building the timeline**
   (near where `kwSchedule` / `cardRect` are computed, ~line 295). All tailors share the same
   card layout, so one pass covers all three:
   ```javascript
   const morphEls = ["#cv-role","#cv-resumen","#skills-row",
     "#bullet-1","#bullet-1b","#bullet-2","#bullet-2b","#bullet-3","#bullet-3b"];
   const morphFrac = morphEls.map(sel => {
     const r = document.querySelector(sel).getBoundingClientRect();
     const frac = Math.max(0, Math.min(1, (r.top + r.height/2 - cardRect.top) / cardH));
     return { sel, frac };
   });
   ```
2. **Slow the lime scan to span the whole morph window** so the bar is actually over each
   section as it rewrites. Replace the quick `scanDur` (0.3 fast / 0.5 slow) with a longer
   sweep — e.g. `morphScanDur = isSlow ? 2.6 : 1.7`. Feed that to `scanSweep`:
   ```javascript
   const scanT = clickT + 0.30;
   const morphScanDur = isSlow ? 2.6 : 1.7;
   tl.set("#scan-bar", { background: "linear-gradient(180deg, rgba(201,242,77,0) 0%, rgba(201,242,77,0.22) 40%, rgba(201,242,77,0.34) 50%, rgba(201,242,77,0.22) 60%, rgba(201,242,77,0) 100%)" }, scanT - 0.01);
   scanSweep(tl, "#scan-bar", [], scanT, morphScanDur, 0.4, "power1.inOut", "power1.in");
   ```
3. **Fire each morph at `scanT + morphScanDur * frac`** instead of `m + gap*n`:
   ```javascript
   morphFrac.forEach(({ sel, frac }, i) => {
     const mt = scanT + morphScanDur * frac;
     if (sel === "#skills-row")      morphSkills(tl, mt, tailor.skills, d);
     else if (sel === "#cv-role")    morphSection(tl, mt, sel, tailor.role, d, false);
     else if (sel === "#cv-resumen") morphSection(tl, mt, sel, tailor.resumen, d, false);
     else {
       const bulletIdx = ["#bullet-1","#bullet-1b","#bullet-2","#bullet-2b","#bullet-3","#bullet-3b"].indexOf(sel);
       morphSection(tl, mt, sel, tailor.bullets[bulletIdx], d, true);
     }
   });
   ```
4. **`scoreT` (line ~365) currently `= m + gap*9`.** Re-anchor it to after the scan completes:
   `const scoreT = scanT + morphScanDur + 0.25;`. The Scene 6 score-break (idx===2) and the
   normal score rise both key off `scoreT`, so they follow automatically. Keep the reasoning
   fade-out (`scoreT - 0.35`), ring pulse, and `tailor-score` reveal as-is.
5. **`endT` (line ~420)** still `= scoreT + scoreDur + hold` — leave it; it now sits after the
   longer scan, so the chain to the next tailor stays correct.
6. Delete the now-unused `gap`-based morph block (lines ~353–363) and the `m` constant.

**Watch-outs:**
- `frac` for `#cv-role` (top of card) will be small (bar arrives early); bottom bullets near
  1.0 (bar arrives late). That's the intended causality. Confirm in the contact sheet that the
  bar is visually *over* each section when it swaps — adjust `morphScanDur` if it leads/lags.
- Tailor 1 is `"slow"` (teach the mechanic), tailors 2–3 `"fast"`. The `morphScanDur` split
  (2.6 / 1.7) preserves that.
- This lengthens each tailor by roughly `(morphScanDur − old span)`. Expect total film +3–5s.
  Re-check `data-duration` (Fix 2 note).
- Keep the red-scan-bar restore at `endT` (line ~422) so the next tailor's lime `set` starts
  from a clean state.

---

## Fix 4 — Scene 7: hold the fan-out caption longer

**Symptom:** "Esto es lo que hacen los que sí consiguen entrevista." passes too quickly into
the human-consequence beat.

**Where:** Scene 7 offsets, lines ~548–550.
```javascript
const fanT      = t3end;
const demoFadeT = fanT + 2.4;
const humanT    = fanT + 3.0;
```

**Change:** Add ~1.0–1.2s of dwell. Push `humanT` (and `demoFadeT` with it) later:
```javascript
const demoFadeT = fanT + 3.4;   // was 2.4
const humanT    = fanT + 4.2;   // was 3.0
```
Everything after (`human_close` label, human lines, `ctaT`) is derived from `humanT`, so it
cascades. (See Fix 5 for what `demoFadeT` should now do.)

---

## Fix 5 — Scene 8: keep Andrés's CV faintly visible behind "Tú no cambiaste…"

**Symptom:** By the human-consequence beat the CV (`#demo-group`) is faded to opacity 0.10 —
effectively gone. The line "Tú no cambiaste. Tu historial tampoco." lands better with the
tailored CV still **dimly visible behind it** (the history literally didn't change — only its
visibility to the filter did). `#human-close` is a transparent layer (z-index 8, no
background), so whatever's behind shows through.

**Where:** the `demoFadeT` tween, line ~555:
```javascript
tl.to("#demo-group", { scale: 0.96, opacity: 0.10, duration: 0.5, ease: "power3.out" }, demoFadeT);
```

**Change:** Don't fade the CV out — **dim it to a ghost** and keep it there through the human
beat:
```javascript
tl.to("#demo-group", { scale: 0.97, opacity: 0.22, duration: 0.6, ease: "power3.out" }, demoFadeT);
```
Then fade it the rest of the way out only when the CTA arrives (Scene 9 has a solid `--bg`
`#cta-group` at z-index 10 that covers everything anyway, so an explicit fade is optional —
but cleaner to drop it just before `ctaT`):
```javascript
tl.to("#demo-group", { opacity: 0, duration: 0.4, ease: "none" }, ctaT - 0.3);
```
Tune the `0.22` by eye in the contact sheet — enough that the lime-scored tailored CV reads as
present, not so much it competes with the text. ~0.18–0.28 is the range.

**Watch-out:** `#human-close` text is `--ink` (light) over the dark CV — contrast is fine. The
lime `human-l2` sits over the CV too; confirm it's still legible against the (dimmed) card.

---

## Fix 6 — CTA: add "tailor your CV to any role in seconds"

**Symptom:** The CTA doesn't state the core promise the film just demonstrated (one CV,
retailored per vacancy, in seconds).

**Where:** CTA DOM (lines ~55–59) and CTA timeline (lines ~575–581).

**Change — option A (recommended): repurpose/extend the subline.** Current subline is
"Sube tu CV y descubre tu puntuación. Gratis." Add a second promise line above the button.
Either replace the subline copy or add a new `#cta-promise` element between headline and
subline:
```html
<div id="cta-promise" data-copy="Adapta tu CV a cada vacante en segundos.">Adapta tu CV a cada vacante en segundos.</div>
```
- Style it in CSS near `#cta-subline` (line ~233): slightly larger/brighter than subline, e.g.
  `font-size: 32px; color: var(--ink);` so it reads as the promise, with the existing subline
  as the smaller "Gratis." support line.
- Add to the `gsap.set(...opacity 0...)` init list (line ~270) and reveal it in the CTA
  stagger between headline and subline:
  ```javascript
  tl.to("#cta-promise", { opacity: 1, duration: 0.4, ease: "none" }, ctaT + 0.75);
  ```
  Then nudge `#cta-subline` / `#cta-btn` / `#cta-domain` reveal times a touch later so the
  stagger stays even.

**Copy note (`.claude/rules/anti-slop.md`):** keep it concrete, no banned words. "Adapta tu CV
a cada vacante en segundos." is fine. Avoid "potencia/transforma/desbloquea." Keep the source/
domain line present.

**Watch-out:** verify the new line fits the safe zone — the exporter's safe-zone check (Lock 6)
will FAIL the export if `#cta-promise` overflows. Keep it ≤ one line at the chosen size.

---

## Verification (run after ALL fixes)

1. **Preflight** (catches structural breaks):
   ```
   py scripts/motion_preflight.py motion/specs/<spec>.json
   ```
   (or skip if villain-v3 is template-only with no spec — the export's in-page checks cover it.)

2. **Draft pass first** (fast, 15fps) to eyeball timing of each fix:
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --draft --name villain_v3_fixes_draft --output export-video/
   ```
   Read the contact sheet. Specifically confirm:
   - Fix 1: l1/l2 gone when "No eres tú./Es el filtro." shows; punchline holds.
   - Fix 2: bad-CV (score 23) sits longer before the cheat-code turn.
   - Fix 3: lime bar is *over* each section as it rewrites, for all 3 tailors (no waterfall).
   - Fix 4: fan-out caption dwells.
   - Fix 5: tailored CV faintly visible behind "Tú no cambiaste…".
   - Fix 6: CTA promise line present, inside safe zone.

3. **Re-capture golden hashes** (timing changed, so the old baseline is stale — this is
   expected, not a regression):
   ```
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --write
   py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --check --strict
   ```
   The `--check --strict` must print "All N frames match golden." If any label landed on a
   tween boundary and flickers (like the old `human_close` bug), nudge that **label** ±0.3–0.5s
   away from the boundary and re-write.

4. **Confirm `data-duration`** (line 2) ≥ actual timeline end (use `?dev=1` scrubber to read
   the end time). Bump if the film grew past 46s.

5. **Full quality export** (60fps):
   ```
   py scripts/motion_exporter.py --input templates/scenes/scene-launch-villain-v3.html --name villain_v3 --output export-video/
   ```
   Watch for the exporter's FAIL gates (safe-zone overflow, running CSS animation). Review the
   final contact sheet before shipping.

## Order of operations

Apply 1 → 2 → 3 first (they cascade timing forward and are the structural ones), then 4 → 5 → 6
(localized to the back third). Re-read each function before editing — earlier edits move the
line numbers cited here. Don't re-capture golden frames until all six are in.
