# Villain-v3 — Animation Uplift Plan

**Goal:** raise the animation of every scene to the sophistication of the Scene 9 CTA,
**without flattening the energy arc.** Copy and scene structure stay byte-for-byte
identical — this is a *motion* replan only.

**Scope guard:** the CTA is the only **5**. The villain (Scene 2) must get *colder and
more mechanical*, not warmer — that contrast is what makes the alive resolution land.
The arc is a temperature arc: ease (mech→settle), color (red→lime), and "life"
(static→breathing) all rise together. Raise the floor; do not flatten the climb.

Reference block: [scene-launch-villain-v3.html:651-694](../templates/scenes/scene-launch-villain-v3.html#L651-L694).

> **Reviewed against the code (Claude, 2026-06-14).** Central diagnosis confirmed: the
> post-processing toolkit (`initPostLayer`/`vignetteUp`/`bloomPulse`/`caFlash`) is **never
> called anywhere** in the scene — genuinely dormant. `particleField`/`draw` underused.
> Scene 8 is uniform `luxe` slide+fade as described. **One real defect found and corrected:
> `weightShift` is a no-op** — the copy renders in *static* Archivo (vendor/fonts has
> Archivo-400/500/600 + ArchivoBlack-400, no `wght` axis), so the Scene 1 and Scene 8
> weight-tween prescriptions are replaced below with font-safe emphasis. Two minor fixes:
> `vignetteUp` is a *pulse*, not a sustained level (Scenes 2–3), and the Scene 8 breathing
> bloom must be killed at the CTA cut. All edits marked ⚠️ inline.

---

## STEP 1 — The CTA's grammar (confirmed in the code)

Each rubric item, verified against the shipped CTA. This is the bar.

| # | Grammar rule | Where it lives in the CTA | Line |
|---|---|---|---|
| a | **A hero gesture that DRAWS/BUILDS** (not fades) | `cta-trail` `strokeDashoffset` draws the lime trail bottom→star, `power2.inOut` | [663-664](../templates/scenes/scene-launch-villain-v3.html#L663-L664) |
| b | **Continuous life** — nothing that lands stays dead | `cta-star` pops `back.out(2)`, then twinkles forever `yoyo, repeat:-1` | [667-668](../templates/scenes/scene-launch-villain-v3.html#L667-L668) |
| c | **Ambient depth** — seeded field rising behind content | `particleField` 46 lime motes, `opacityMax:0.26`, seeded `"v3-cta"` | [672-675](../templates/scenes/scene-launch-villain-v3.html#L672-L675) |
| d | **Eases carry emotion** — NOT luxe on everything | `power2.inOut`, `back.out(2)`, `sine.inOut`, `settle`, `back.out(1.8)` — zero luxe | [664-690](../templates/scenes/scene-launch-villain-v3.html#L664-L690) |
| e | **Uneven, orchestrated cadence** — not one stagger | beats at +0.2/+0.7/+1.1/+1.3/+1.5/+1.8/+2.1/+2.6/+3.1/+3.7/+4.2 | [671-692](../templates/scenes/scene-launch-villain-v3.html#L671-L692) |
| f | **A metaphor the motion embodies** | trail+star = the filter (a scan line) turned into *your* wand, drawing toward your brand | — |

**The body scenes under-use the library.** Everything above is one `tl.to` and a
motion-lib call away. The gap is reach, not capability.

---

## STEP 2 — Audit of Scenes 1–8 against that grammar

| Scene | Current hero gesture | What lands & freezes | Depth layer | Eases vary? | Metaphor it COULD embody |
|---|---|---|---|---|---|
| **1 Wound** [514-542](../templates/scenes/scene-launch-villain-v3.html#L514-L542) | per-word mask slide (`luxe`) | every line freezes static | none (just `#bg-grid` fade) | luxe + mech, but luxe dominates | the **fog of self-doubt** resolving into one cold word |
| **2 Villain** [548-582](../templates/scenes/scene-launch-villain-v3.html#L548-L582) | RECHAZADO **stamp** (`verdict` + impact) + ring fill | flags/warnings freeze | none | mech/verdict/power3 — **good already** | the machine's **verdict slamming** — the cold the film needs |
| **3 Cheat Code** [588-606](../templates/scenes/scene-launch-villain-v3.html#L588-L606) | none — overlay fade + slide (`luxe`) | three turn-lines freeze | none | mostly luxe | a **curtain lifting** on the secret; the warm arriving |
| **4–6 Tailors** [613-619](../templates/scenes/scene-launch-villain-v3.html#L613-L619), [389-503](../templates/scenes/scene-launch-villain-v3.html#L389-L503) | lime scan + 9-step morph + score spring | chips cycle out (good); ring holds | none | settle/back.out/power3 — varied | the **cheat code in motion**; warmth climbing with the score |
| **7 Fan-out** [625-632](../templates/scenes/scene-launch-villain-v3.html#L625-L632), [568-577](../templates/scenes/scene-launch-villain-v3.html#L568-L577) | **ghost-card fan** (superposition) | fanned cards freeze, then fade | none | power3 + back.out | **one person, N tailored selves** — the climax insight |
| **8 Human** [638-645](../templates/scenes/scene-launch-villain-v3.html#L638-L645) | **none** — 4 lines slide (`luxe` ×4) | all four freeze, then fade | none | **uniform luxe — the rubric's exact warning** | the **inversion**: the human takes the algorithm back |

**Findings:**
- **Scene 8 is the flattest in the film** — pure `luxe` slide+fade, no depth, no life, the
  doctrine's "close on the human" beat reduced to the most generic motion in the cut.
- **Scenes 1, 3, 8 are all fade/slide** with no build gesture and no depth layer.
- **Score events (4–6) have no `bloomPulse`** — the doctrine's textbook use
  ([SKILL.md:148](../.claude/skills/motion-builder/SKILL.md)) — and the Tailor-3
  hesitation ([459-470](../templates/scenes/scene-launch-villain-v3.html#L459-L470))
  re-implements a dim where `worq-breathe` (the ease built *for* that beat,
  [SKILL.md:102](../.claude/skills/motion-builder/SKILL.md)) exists unused.
- **Scene 2 is correctly cold** — but its impact can be *sharpened* (CA flash, vignette)
  without adding any warmth or life. Colder = better here.
- **`initPostLayer` is never called anywhere.** The whole vignette/bloom/CA toolkit —
  which adds **zero HTML** — is dormant across all eight scenes.

---

## Structure-safety tiers (the hard constraint)

> "Copy and structure stay byte-for-byte identical."

Every upgrade below is tagged:

- **[A] Zero structure change.** JS-injected post layer, or a swap of ease/reveal on an
  existing element. Ship freely — no DOM touched, no copy touched.
  → `initPostLayer`, `vignetteUp`, `bloomPulse`, `caFlash`, `blurInChars`, `weightShift`,
  `worq-breathe`, `landWith`.
- **[B] One additive decorative node, no copy/beat change.** A `<div>` particle container,
  a `<canvas>`, or an `<svg>` underline — exactly the kind of node the CTA itself added
  ([49-64](../templates/scenes/scene-launch-villain-v3.html#L49-L64)). No text, no
  re-sequencing. **Needs your explicit OK** that "structure identical" permits decorative
  layers (the CTA precedent says yes).
  → `particleField`, `canvasParticles`, `draw` on new SVG.

The plan is built so **Tier A alone clears the floor** on every scene. Tier B is the
flourish, gated on your call.

---

## STEP 3 — Per-scene replan

### Scene 1 — The Wound · **intensity 2 / life ~1**
- **Hero gesture (build):** `blurInChars` on `#intro-l1/2/3` — each line *assembles from
  4px blur*, the fog of self-doubt resolving, instead of the mask-slide. **[A]**
  `blurInChars(tl, "#intro-l1", 0.4, { duration: 0.6, stagger: 0.03 })`
- **The turn:** keep the `morphSection` → "Nada.", then emphasize the turn with a `scale`
  lift (1.0→1.04, `settle`) as `.turned` applies the lime — a smooth "claiming" beat that
  survives the static font. **[A]**
  ⚠️ **Correction — not `weightShift`.** `--font-body` is **static Archivo** (no `wght`
  axis), so `font-variation-settings` animates nothing. Forcing `font-family:'Inter Variable'`
  on one line *would* animate weight but render that line in a **different typeface** than its
  neighbours. Use scale/color for the "thicken" feel here, OR move the whole copy system to
  Inter Variable as a separate, deliberate decision.
- **Continuous life:** none by design — the void should feel empty. One slow
  `vignetteUp(tl, 8.3, 0.06, 0.14, 0.7)` as the kicker "El filtro te descartó" lands. **[A]**
- **Depth:** `initPostLayer()` (called once, here) — vignette only. **No particles** (they'd
  fill an emptiness that is the point).
- **Ease / temp:** luxe→mech, **neutral/hollow** (white on black). Cold-leaning, not red.
- **Metaphor:** *the fog of self-doubt resolves into one cold word — "Nada."*

### Scene 2 — Meet the Villain · **intensity 4 / life 0 (frozen)**
> The pit. High impact, **zero** continuous life. Do **not** add `repeat:-1` anywhere here.
- **Hero gesture:** keep the stamp ([572-573](../templates/scenes/scene-launch-villain-v3.html#L572-L573))
  — sharpen the *cut* with `caFlash(tl, 14.16, 2)` on the impact frame. **[A]**
- **Continuous life:** **none.** The machine doesn't breathe. This absence is the design.
- **Depth:** deepen the vignette on the RECHAZADO verdict and **hold it** through the pit —
  raw `tl.to("#_post-vignette", { opacity: 0.18, duration: 0.5, ease:"power2.inOut" }, 14.0)`.
  **[A]** ⚠️ Not `vignetteUp` — that helper is a *pulse* (up-and-back over 2×dur); it would
  release the close-in immediately. Use a raw level change so the walls stay shut until Scene 3
  lifts them. Optional **[B]:** red `scan-sparks` under the red bar —
  `canvasParticles(tl, "#villain-canvas", 11.9, 0.9, "v3-villain", "scan-sparks", { color:[224,89,59], y0:..., y1:..., sweepDur:0.9 })`
  (override the lime default to red).
- **Ease / temp:** mech / verdict, **coldest, red.** No `back.out`, no settle here.
- **Metaphor:** *the verdict slams like a door — the frame itself flinches, the room darkens.*

### Scene 3 — The Cheat Code · **intensity 3 / life ~1 (first breath)**
- **Hero gesture (build):** `blurInChars` on `#turn-l1/2/3` instead of slide — the secret
  *assembles*. **[A]**
- **Continuous life:** faint warmth arriving — `bloomPulse(tl, 23.8, 0.4, 0.08, 0.6)` as the
  overlay lifts to the clean CV (the lime starts to live). **[A]**
- **Depth:** vignette eases *off* during the lift — raw
  `tl.to("#_post-vignette", { opacity: 0.06, duration: 0.7, ease:"power2.out" }, 23.8)`
  (releases the Scene-2 close-in). ⚠️ `vignetteUp` has no "reversed" mode — it always pulses
  up-and-back; use a raw tween to change the held level.
  Optional **[B]:** `draw()` a lime underline under `#turn-l3` ("el idioma que el filtro
  entiende") — plants the underline motif the CTA pays off. Needs a small `<svg>` node.
- **Ease / temp:** luxe→settle, **warming** (first lime hint).
- **Metaphor:** *the curtain lifts; the cold room is now warm and legible.*

### Scenes 4–6 — Three Tailors · **intensity 3, Tailor-3 → 4 / life 2 (pulsing)**
- **Hero gesture:** the morph + score spring already builds — reinforce the *payoff* with
  `bloomPulse` on each score land: `bloomPulse(tl, scoreT, 0.6, 0.12, 0.35)`. **[A]**
- **Continuous life:** the ring pulse already exists; the new life is the bloom breathing
  with each score.
- **The break (Tailor 3):** replace the manual color-dim
  ([461-464](../templates/scenes/scene-launch-villain-v3.html#L461-L464)) with
  `ease:"worq-breathe"` on the held ring — the *built-for-this* micro-oscillation
  ([SKILL.md:102](../.claude/skills/motion-builder/SKILL.md)). **[A]**
- **Depth / [B]:** `canvasParticles(... "score-burst" ...)` one-shot on the **final** score
  only (Tailor 3 → 93), centered on the ring — the realization sparks. Don't burst all three
  (monotone → keep the asymmetry).
- **Ease / temp:** settle / back.out, **warm, lime rising.**
- **Metaphor:** *the cheat code in motion; the score is the warmth made numeric.*

### Scene 7 — Fan-out · **intensity 4 / life 3 (burst)**
- **Hero gesture:** the fan is already a build — add anticipation with `landWith` on the
  caption pop so it settles instead of stopping. **[A]**
- **Continuous life:** `bloomPulse(tl, fanT+0.5, 0.6, 0.12, 0.4)` as the cards spread — the
  energy of the realization.
- **Depth / [B]:** a short lime `particleField` *or* `score-burst` puff from the card stack
  as it fans (cards leave negative space — particles don't sit over text here).
  `particleField(tl, "#s7-particles", fanT, { count:30, seed:"v3-fan", color:"201,242,77", opacityMax:0.2, duration:2.5 })`.
- **Ease / temp:** back.out / power3, **warm, energetic.**
- **Metaphor:** *one person split into every version that gets seen.*

### Scene 8 — The Human Consequence · **intensity 3, hero line → 4 / life 4 (breathing)**
> Where "static → breathing" must visibly cross over. Currently the deadest scene; make it
> the most *alive* pre-CTA without out-shouting the CTA.
- **Hero gesture (build):** `blurInChars` on the four lines, **varied cadence** (don't reuse
  one stagger): l1 0.5s, l2 0.45s, l3 0.5s, **l4 hero** 0.6s with a beat of held air before it. **[A]**
- **The hero line:** emphasize "Ahora tú también" with a `scale` lift (1.0→1.05, `settle`)
  + the existing lime turn + the bloom behind it (below) — the power transferring as it claims
  the algorithm. **[A]** ⚠️ **Not `weightShift`** — static Archivo has no `wght` axis (see the
  Scene 1 correction). An animated weight here would require committing `#human-*` to Inter
  Variable, a typeface change to decide separately.
- **Continuous life:** a slow lime **bloom breathing** behind the stack —
  `tl.to("#_post-bloom", { opacity:0.22, duration:2.2, ease:"sine.inOut", yoyo:true, repeat:-1 }, humanT)`
  (repeat:-1 + yoyo → excluded by the Lock 9 preflight). The warmth is now *alive*. **[A]**
  ⚠️ This loop **never stops** — it keeps breathing under the Scene 9 CTA. Kill it at the cut
  so the CTA starts clean: `tl.to("#_post-bloom", { opacity: 0, duration: 0.4 }, ctaT)`
  (the CTA builds its own warmth via the particle field).
- **Depth:** **bloom, not particles** — the scene is full-width centered text; the restraint
  rule ("never over text") rules particles out here. Bloom (blurred, screen-blend, behind)
  is the safe warmth.
- **Ease / temp:** luxe→settle, **warmest pre-climax, lime hero lines.** Vignette fully off.
- **Metaphor:** *the human picks the weapon up — and the screen starts to breathe.*

---

## The arc, as a table (the thing we must not break)

| Scene | Intensity | Temp | Continuous life | Hero gesture |
|---|:--:|---|---|---|
| 1 Wound | 2 | hollow / neutral | ~none (1 vignette breath) | chars resolve from blur |
| 2 Villain | **4** | **coldest / red** | **0 — frozen** | stamp + CA flash + vignette close |
| 3 Cheat Code | 3 | warming | first faint bloom | secret assembles from blur |
| 4–6 Tailors | 3 → 4 | warm / lime↑ | bloom pulses w/ score | morph + score spring |
| 7 Fan-out | 4 | warm | bloom + fan burst | ghost-card fan |
| 8 Human | 3 → 4 | warmest pre-climax | **breathing bloom (repeat:-1)** | chars + scale-emphasis hero |
| **9 CTA** | **5 (only 5)** | **full lime, alive** | **trail draws, star twinkles forever** | strokeDashoffset trail + star |

Intensity and life are tracked separately on purpose: **Scene 2 is high-intensity,
zero-life.** That is the whole trick — the cold maximal pit makes the warm breathing
resolution land.

---

## Determinism + restraint guardrails (every upgrade obeys these)

- All motion GSAP-owned (Lock 3) — `blurInChars`, `bloomPulse`, `caFlash`, `scale`/`landWith`
  are all tween-driven; zero CSS transitions. (`weightShift` is **not used** — static Archivo
  has no variable axis; see the Scene 1/8 corrections.)
- Every continuous loop is `repeat:-1 + yoyo` so the duration preflight excludes it (Lock 9).
  New loops: Scene 8 breathing bloom. (CTA star already complies.)
- Any particle/canvas is seeded (Lock 8/10): seeds `v3-villain`, `v3-fan`, plus the existing
  `v3-cta`. Opacity ≤ 0.2 in body scenes (stricter than the 0.35 ceiling), **never over text.**
- Post layer is z-9000, JS-injected by `initPostLayer()` once — no HTML, no safe-zone risk
  (it carries no `data-copy`).
- Exporter gates unchanged: safe-zone FAIL (Lock 6), no running CSS animation (Lock 7) —
  nothing here introduces a CSS `@keyframes`.

---

## Ship as a hypothesis

**Falsifier — this is *worse* if:**
1. The added depth/life reads as **busy, not richer** — if the Scene 8 pilot's contact sheet
   is more crowded but the words are *harder* to read, kill it.
2. The early warmth **deflates the CTA** — if Scenes 7–8 start to feel like a 5, the CTA
   stops being the only payoff and the arc goes flat. The CTA must still feel like a *lift*.
3. Raising the floor **flattens the climb** — if every scene now feels equally alive, the
   cold-villain contrast is lost.

**Cheapest test first — pilot Scene 8 (Tier A only).**
Scene 8 is the flattest now *and* the hardest taste call (where life must cross over) *and*
fully achievable with **zero structure change** (bloom + `blurInChars` + `scale` emphasis +
vignette-off). It is the maximum-signal, minimum-cost probe: if Tier-A Scene 8 reads as a
clear step up *and the CTA still feels bigger after it*, the thesis holds and we roll the
pattern to the rest. If it muddies the copy or pre-empts the CTA, we've spent one re-render
to learn it.

Test loop: edit Scene 8 → `golden_frames`/exporter gates → contact sheet (watch, not glance)
→ compare the Scene 8 frames and the CTA frames side by side. Decide before touching 1–7.

---

## Blocking decision before any edit

Editing `scene-launch-villain-v3.html` invalidates the golden baseline at
`export-video/golden/scene-launch-villain-v3.json`. Two paths:

- **Fork** to `scene-launch-villain-v3-1.html` (or `-v4`) — v3 goldens preserved, new
  baseline written for the fork. Safe, reversible, two files to carry.
- **Edit v3 in place** — regenerate goldens after. One file, but the shipped v3 baseline
  is gone.

**Do not proceed to the Scene 8 pilot until this is answered.**
