# Plan v2 — WorqAI Video v4 (scene-launch-villain): fix the instrument, then run the test

> **North star (unchanged):** *a demo that feels like a manifesto and functions as an initiation.*
> **Operating rule (new):** *the gate only measures the story if the instrument is clean — orthography, motion language, and iteration speed come before the scenes, not after.*

## What changed from the previous plan, and why

The previous plan's discipline survives intact: build Scenes 1–2 only, export a partial, run the 5-person second-5 gut-check head-to-head against the v2 open, Cesar owns the call, revert cheaply if the manifesto frame fails. None of that moves.

Three things are restructured:

1. **Phase 0 exists now.** Diacritics + an orthography preflight gate, a dev scrubber, and draft/partial render flags come before any scene work. Rationale: (a) the v2 export shipped "Andres / Puntuacion / Bilingue / espanol e ingles" — if v3's gate render has the same defect, the test audience (Spanish-speaking job seekers, i.e., exactly the people who notice) reacts to the typos and the exhale signal is contaminated; (b) the wound open is a timing-precision build (a deliberate 1s dead-air hold, a morph at an exact emotional beat) and authoring it blind through full exports is why polish has been capped. Phase 0 is ~1 day and makes Phase 1 both faster and valid.

2. **The villain gets a motion identity before the villain gets built.** The previous plan reuses v1's entrance pattern (`y+opacity, power3.out`) for the wound lines and `back.out(2)` for the RECHAZADO stamp. That is the hero's friendly motion language applied to the antagonist — the motion contradicts the story the copy is telling. Phase 0.5 defines a two-family easing palette (filter = mechanical; WorqAI/human = luxe) and Scenes 1–2 are authored in it. This is the single cheapest "expensive team" upgrade available and it is *load-bearing for the v3 thesis specifically*, not generic polish.

3. **The motion-lib extraction is scheduled, deliberately, between the gate and Scenes 3–9.** Copying the honest pair for the gate build is correct (don't refactor before the creative hypothesis is validated). But Scenes 3–9 must NOT be built by copying again — `runTailor`, `morphSection`, the ring, and the cursor get extracted into `motion-lib.js` first, with golden-frame hashes protecting the refactor. Copy once for speed, never twice.

Everything else from the previous plan — the scene tables, the indict-the-machine copy, the honesty lock, the Lock-compliance work (including the `data-copy` fix), the deferred audio spec — is carried forward below, amended where the audit applies.

---

## Phase 0 — Fix the instrument (~1 day, no scene work)

### 0.1 Diacritics, structurally (BLOCKER)

- Sweep every copy string destined for v3 (and patch the honest base you're copying from): `Así, Puntuación, Bilingüe, español, inglés, genérico, línea, débil, Diagnóstico, encontró, entendió, ignoró, coincidió`, first-person preterites (`Atendí, Gestioné, Monitoreé, Mantuve…` — verify each), `tú` vs `tu` per register.
- Add `check_orthography()` to `motion_preflight.py` **and** to the exporter's pre-frame-loop checks (same place as Lock 6): scan all `[data-copy]` text content plus any `tailors`/copy JS objects for a wordlist of known unaccented forms (`puntuacion, bilingue, espanol, ingles, generico, linea, debil, asi, diagnostico, encontro, entendio…`) → **FAIL with the corrected form printed.** This is the same FAIL-not-WARN culture as Lock 6, applied to the brand's core competence.
- Maintain the wordlist in `.claude/rules/anti-slop.md` so it grows as misses are found.

### 0.2 Dev scrubber (~half a day, multiplies everything after it)

Add a `?dev=1` block to the scene template (stripped or inert in export since the exporter never passes the param):

```html
<div id="dev-bar"><!-- only rendered when location.search includes dev=1 -->
  <input type="range" id="dev-scrub" min="0" max="46" step="0.0166" value="0">
  <span id="dev-time">0.00</span>
  <div id="dev-labels"><!-- one button per MOTION_LABELS entry, onclick seeks --></div>
</div>
<script>
if (new URLSearchParams(location.search).has("dev")) {
  // after motionReady: wire range → gsap.globalTimeline.time(v);
  // ArrowLeft/ArrowRight = ±1/60s; clicking a label seeks to it.
}
</script>
```

Author the wound timing live in a browser tab. This replaces ~80% of gate-build exports.

### 0.3 Draft + partial render flags in `motion_exporter.py` (~2 hours)

- `--from S --to S`: offset the frame loop (`t = from + frame/fps`), trim `total_frames`. Checking the 4.0s morph = a 3-second render, not a 13-second one.
- `--draft`: 30fps, 540×960 viewport (scene CSS is fixed 1080×1920 — render at full viewport but pass `device_scale_factor=0.5`, or screenshot with `clip` + downscale in ffmpeg), `-preset ultrafast -crf 28`. Draft is for timing/judgment; the gate render is always full quality.
- While in the file: fix the stem logic (strip a leading `video_` and a trailing `\d{4}-\d{2}-\d{2}` from `--name` before formatting — kills the `video_video_…_2026-06-08_2026-06-08.mp4` class of bug), and move the hardcoded ffmpeg path into `scripts/_config.py` (it's currently triplicated across exporter/add_sounds/split_voiceover).

### 0.4 Label-frame contact sheet (~1 hour)

`motion_contact_sheet.py`: grid at 1 frame/second **plus** a captioned frame at every `MOTION_LABELS` time (resolve labels from the HTML exactly as `add_sounds.py` already does). Five frames cannot QA a 13s emotional open; the label frames are precisely the beats the gate checklist inspects.

### 0.5 The easing palette — motion as characterization (~2 hours to define, applied during Phase 1)

In `motion-lib.js` (CustomEase ships in GSAP's free tier):

```javascript
// WorqAI / the human — generous, warm
CustomEase.create("luxe",   "0.22, 1, 0.36, 1");    // hero text, card reveals, lime actions
CustomEase.create("settle", "0.34, 1.4, 0.44, 1");  // gentle overshoot: chips, the 92 landing

// The filter — mechanical, indifferent, no mercy
CustomEase.create("mech",    "0.7, 0, 0.84, 0");    // accelerating IN: the red scan, the ring draining to 23
CustomEase.create("verdict", "0.9, 0, 1, 1");       // the stamp: hard arrival, zero bounce
```

Rule for v3: **every red/filter element animates in the mech family; every lime/human element in the luxe family.** `power3.out` raw strings become a preflight WARN. This is where "indict the machine" stops being only copy.

---

## Phase 1 — Build Scenes 1–2 (the gate build)

Files: copy `scene-launch-honest.{html,css}` → `scene-launch-villain-v3.{html,css}` (honest pair untouched — it's the A/B control). Namespacing (`*-v3`, `*_v3_*`) unchanged from the previous plan. All reused primitives per the previous plan's line-reference table.

### Scene 1 — The Wound (0.0 – 6.0s)

Beat sheet unchanged (kill the kicker; 0.4 / 1.6 / 2.7 / 4.0-morph / 4.7 / 5.8). Three amendments:

**a) Per-word masked reveals, not block slides.** `motion-lib.js` already contains `splitWords()` with overflow-hidden mask wrappers — the wound lines use it. Words rise out of their own masks, `luxe` ease, ~0.05s word stagger; on l3 ("…el problema eras tú.") let **"tú"** arrive last with a slightly longer duration — the line literally lands on the viewer. Block-level slides are the #1 template tell on 52px headlines, and this open is nothing but 52px headlines.

**b) The morph at 4.0 is the only block-level move in the scene — by design.** `morphSection(tl, 4.0, "#intro-l3", "No eres tú.", 0.4, false)` + the `.turned` class toggle at the blurred midpoint, exactly as planned. Contrast between the word-mask texture of the setup lines and the full-block dissolve of the reversal is what makes the reversal feel like a different *kind* of event. (Risk note from the previous plan stands: verify the post-4.0 frame on the contact sheet — now trivially via `--from 3.8 --to 4.6 --draft`.)

**c) Designed exit at 5.8.** Not fade-and-drift: the masks **close back over the words** (clip the `word-wrap` spans shut, slight stagger, `mech` ease — the filter's world is arriving). Inverse-of-entrance exits are the cheapest "a studio did this" signal, and using the mech family here foreshadows Scene 2 before the viewer sees anything red.

Color arc (dark/heavy open) carried forward from the previous plan, with one implementation amendment: **crossfade two stacked bg layers** (charcoal/navy layer above the brand off-white layer, GSAP-tweened opacity) rather than animating `--bg-*` custom properties — same Lock-3 cleanliness, no custom-property interpolation edge cases, and the eventual cheat-code "lift" becomes a single opacity tween. WhatsApp-notification cue: keep, static, one cue only.

`tl.addLabel("wound", 0.4)` unchanged. Every text node gets `data-copy` (and now also feeds the orthography gate).

### Scene 2 — Meet the Villain (6.0 – 12.0s)

Beat sheet structurally unchanged (6.0 card wipe / 6.8 panel / 7.4 red scan / 8.2 bleed / 9.0 ring / 9.5 stamp / 10.2 flags / 11.2 button; diagnostic panel never revealed; indict-the-machine flag copy verbatim from the previous plan, honesty lock intact). Four amendments:

**a) The scan CAUSES the bleed — position-driven, not DOM-order stagger.** The previous plan staggers `.kw-bad` at 0.06s in DOM order, which approximates top-to-bottom but is uncoupled from the bar. Couple them: after `fonts.ready`, measure each `.kw-bad` span's `getBoundingClientRect().top`, convert to a fraction of the card's height, and schedule each highlight tween at `scanStart + scanDuration * fraction` (`duration ~0.18`, `mech`). The viewer's eye rides the bar and watches it *find* each weak word — the filter visibly doing the damage, which is the entire point of the scene. (~15 lines; the cursor-targeting code already establishes the measure-after-fonts pattern. The `!important` removal from `.cv-clean-mode .kw-bad` per the previous plan still applies — Lock 3.)

**b) The stamp is a verdict, not a celebration.** Replace the badge-spring (`scale 1.6→1, back.out(2)` — friendly, bouncy, the *score badge's* personality) with: `scale 1.35→1, opacity 0→1, duration 0.16, ease "verdict"`, then a 2-frame impact on the card — `gsap.to("#cv-card", { x: 3, duration: 0.033, ease: "none" })` → back to 0 (deterministic, GSAP-owned, reads as the stamp physically hitting the page) — and the card's `box-shadow` deepens ~10% for the rest of the scene. Same DOM, same rotation, opposite emotional read.

**c) The ring drains, it doesn't bloom.** `pATS` 0→23 keeps the existing proxy mechanics (Lock 4) but the ease moves from `power1.out` to `mech` — the value accelerates *into* 23 and stops dead. Cold arithmetic, not a friendly progress indicator.

**d) Camera: one slow push.** `#demo-group` (or a wrapper with `will-change: transform`) scales 1.000 → 1.020 across 6.0–12.0, `ease: "none"`. Sub-perceptual; the frame feels alive and the scene gains quiet pressure toward the stamp. Verify text doesn't shimmer under frame-stepping via a `--from 7 --to 9` draft; if it does, push the bg layers instead and leave the card static.

Document grain on the card: keep, static (Lock 7). `tl.addLabel("score_low", 9.0)` unchanged.

### Lock compliance

The previous plan's Lock section carries forward whole (Locks 1/2 verbatim from honest; new effects GSAP-owned; `!important` removal; `data-copy` on everything; no `@keyframes`). Additions: the impact shake and camera push are GSAP tweens (Lock 3 clean); the position-scheduled bleed is computed once after `fonts.ready` (deterministic — same fonts, same layout, same times); the orthography check now runs alongside Lock 6 in the exporter.

---

## Phase 1.5 — Gate export + the gut-check (procedure hardened)

```powershell
py scripts/motion_exporter.py `
  --input templates/scenes/scene-launch-villain-v3.html `
  --duration 13 --name villain_v3_open_gate `
  --output export-video/
```

(Iterate with `--draft` and `--from/--to`; the gate render itself is full quality, 60fps. Silent, per the previous plan — copy carries the test.)

**Gate protocol (Kenneth runs the human part; previous plan's steps 1–3 plus):**

1. Contact sheet check — now against the label-frame sheet: clean "No eres tú." after 4.0; villain line on-screen and in safe zone; bleed reads as a sweep; stamp legible/rotated; dark palette holds. Orthography gate passed mechanically before this point.
2. **Test conditions match the medium:** on a phone, vertical, sound off, ideally embedded in a scroll context — not full-screened on a laptop. The product decision this gate informs is a feed decision.
3. Head-to-head vs the v2 open, ~5 real job seekers, watch faces at second 5 — unchanged. Capture two additional cheap signals: did they look away before second 3 (hook), and ask afterward, in their words, *who the video says is at fault* (the indictment landing is the actual hypothesis; the exhale is its symptom).
4. **Exhale / v3 wins → Phase 2. v3 underperforms v2 → revert toward the demo.** Cesar owns the call on the data. Unchanged.

**Determinism check unchanged:** re-export once, byte-identical output expected — and now also store SHA-256 hashes of the label frames (`wound`, `score_low`, stamp frame) as the first golden set for Phase 2.

---

## Phase 2 — Extract before extending (only after the gate passes; ~1–2 days)

**Do not build Scenes 3–9 by copying a third time.** Before continuing:

- Move into `motion-lib.js`: `morphSection`, `morphSkills`, `scoreRing` (proxy + applyRing), `cursorClick(target)` (with the measure-after-fonts pattern), `scanSweep(color, schedule)` (taking the position-causality callback from Phase 1), `stamp(opts)`, `fanOut`, `resetUnderCover`, the easing palette, and the standard init/`MOTION_LABELS` boilerplate. Scene files shrink to markup + a timeline script.
- Re-render the gate cut and the honest film; **golden-frame hash diff** (the Phase 1.5 hashes + label frames of honest) proves the refactor changed nothing. Ten lines in the exporter; this is what makes the refactor safe instead of brave.
- Port `scene-launch-villain-v3.html` onto the extracted lib. From here, every craft improvement lands once and upgrades all films.

---

## Phase 3 — Scenes 3–9 (deferred scope, carried forward with amendments)

The previous plan's scene table stands — windows, reuse, copy, the ★ threshold-crossing centerpiece, the Scene 6 two-stage score break, the superposition fan-out read, the Scene 8 human close, the scrubbed CTA ("Ver mi puntuación", no overpromise). Amendments from the audit:

- **Scene 4 (slow tailor):** the first **lime** scan uses the same position-causality machinery as Scene 2's red one — sections rewrite *as the lime bar passes them*. Red found the weaknesses top-to-bottom; lime heals them top-to-bottom. The mirroring is the villain device completing itself, and it's free once `scanSweep(color, schedule)` exists.
- **Easing families throughout:** tailors and score landings = `luxe`/`settle`; any residual filter beats = `mech`. The Scene 6 held beat at ~68 is a *timeline gap*, not a slow tween — silence in motion as well as sound.
- **Per-rep texture variation:** rep 1 slow + causality (teach the mechanic), rep 2 a tight cascading wave (mastery), rep 3 the break (the brief's human hand). Optionally, rep 1's bullets rewrite with a per-word settle rather than a block swap — it reads as *writing*, which is the product.
- **Camera:** the 1.02 push resets under the threshold overlay (reset-under-cover, already the mechanism) and runs again per segment; the cheat-code "lift" pairs the bg-layer crossfade (dark→light) with a slightly faster push release — the initiation felt physically.
- **Designed exits** for the three big seams: demo→threshold (overlay **wipes** up, `mech`, the last thing the filter's world does), threshold→tailors (the lift), fan-out→CTA (ghost cards exit along their fan vectors, not via fade).

## Phase 4 — Audio + finishing (deferred, carried forward with amendments)

The previous plan's audio spec stands (label-keyed VO JSON with `wound/score_low/cheat_code/…`, real human voice over generic TTS, weighty SFX map, no SFX in the held beats, music spec'd but not baked for the organic master). Additions:

- **Loudness + ducking in one orchestrator pass:** `scripts/make_film.py --film films/villain-v3.json` runs export → `add_sounds` → `split_voiceover` → music (for ad/demo deliverables) with automated ducking windows computed from the VO segment times (you already know them from the labels) and a final `-af loudnorm=I=-14:TP=-1.5:LRA=11`. Organic master stays silent per the convention.
- **Burned captions from the VO JSON:** the line text + label time you already maintain *is* a caption file. Render brand-styled caption elements on the GSAP timeline at label times (deterministic, designed) for the ad variants. Majority of feed viewing is sound-off; this moves retention more than any Phase 3 refinement.
- **Label-range cutdowns:** once the master passes, export 6s (wound→stamp→CTA card) and 15s (wound→tailor 1→CTA) variants by rendering only the frame ranges between chosen labels. The deterministic master makes length variants nearly free — use them for the paid tests Cesar will want next.

---

## Guardrails (unchanged + one addition)

- **Honesty lock** — verbatim from the previous plan. Mechanical filter, no malice, no "te van a leer," fan-out = three possible futures, never a confirmed outcome.
- **Determinism** — every new effect GSAP-owned; glitch/threshold = proxy tweens, never CSS transitions; grain and cues static.
- **Scope** — director's cut of the same 9 scenes; no mythology project; the gate decides whether Scenes 3–9 exist at all.
- **New: orthography is a FAIL gate, permanently.** No render leaves the pipeline with unaccented Spanish again — not for the gate, not for drafts shown to anyone outside the team.

## Verification

- Phase 0: orthography preflight FAILs on a seeded bad string, passes on the corrected copy; scrubber seeks and label-jumps correctly; `--from/--to` output frame-matches the same range of a full export.
- Phase 1: exporter preflight (Lock 6 + 7 + orthography) passes; label-frame contact sheet inspection per the gate checklist; double-export byte-identical; golden hashes recorded.
- Phase 1.5: the real test — the v3 open beats the v2 open on the 5-person second-5 exhale under phone/sound-off conditions. Functional ≠ pass; the open has to land.
- Phase 2: golden-frame diffs clean across the refactor before any Scene 3–9 work begins.
