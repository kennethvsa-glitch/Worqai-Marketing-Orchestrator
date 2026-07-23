---
# Carousel Visual QA Log
version: 1.1 | updated: 2026-05-07
owner: kenneth-valverde
scope: All HTML carousels — WorqAI + Profile Pro LATAM
---

## HOW TO REPORT A BUG

Paste this template into chat. One bug per entry. Short and specific.

```
BUG REPORT
CAROUSEL: [filename without extension, e.g. carousel_ats-tips_worqai]
SLIDE: [number, e.g. 3 — or "all" if it's a global problem]
SYMPTOM: [one sentence — exactly what you see that looks wrong]
GUESS: [optional — what you think caused it, or "no idea"]
PRIORITY: [P1 = kills the post / P2 = degrades quality / P3 = minor / cosmetic]
```

Example:
```
BUG REPORT
CAROUSEL: carousel_ats-tips_worqai
SLIDE: 5
SYMPTOM: Body text is overflowing the slide boundary on the right side, clipped at export.
GUESS: Font size too large for the Two-Column layout on 1080px.
PRIORITY: P1
```

---

## SCORECARD — BATCH 01 (Target: 10 carousels)

Score each carousel after exporting PNGs. 1–5 scale per metric. Manual Cleanup: 0 = none needed / 1 = minor / 2 = significant.

| ID  | File                              | System         | Hook Type  | Visual Rhythm | Copy Trust | <10s Clarity | Brand Fit | Manual Cleanup | Total /22 |
|-----|-----------------------------------|----------------|------------|:---:|:---:|:---:|:---:|:---:|---:|
| C01 |                                   |                |            |     |     |     |     |     |    |
| C02 |                                   |                |            |     |     |     |     |     |    |
| C03 |                                   |                |            |     |     |     |     |     |    |
| C04 |                                   |                |            |     |     |     |     |     |    |
| C05 |                                   |                |            |     |     |     |     |     |    |
| C06 |                                   |                |            |     |     |     |     |     |    |
| C07 |                                   |                |            |     |     |     |     |     |    |
| C08 |                                   |                |            |     |     |     |     |     |    |
| C09 |                                   |                |            |     |     |     |     |     |    |
| C10 |                                   |                |            |     |     |     |     |     |    |

### Scoring Rubric

**Visual Rhythm** — Does the layout change at least once? Does it feel designed, not templated?
- 5: Layout break is surprising and intentional. You'd think a human designer made it.
- 3: At least one break, but it feels formulaic.
- 1: Every slide looks identical. Fatal Signal 4 is present.

**Copy Trust** — Would a real person on LATAM Instagram stop, read, and believe this?
- 5: Pain is named precisely. Stat is real. Proof is specific. CTA has a clear reward.
- 3: Mostly correct but has at least one vague line or a weak hook.
- 1: Sounds like an AI wrote it. Forbidden phrases or slop detected.

**<10s Clarity** — Without reading body text, does the headline + visual communicate the core idea?
- 5: Instantly clear. Slide 1 hook forces a swipe decision without needing to read anything else.
- 3: Main idea readable but requires effort.
- 1: Confusing without reading body text.

**Brand Fit** — Does this look like WorqAI / Profile Pro LATAM, or like a generic AI carousel?
- 5: You'd recognize the brand without the handle being visible.
- 3: On-brand but interchangeable with any competitor.
- 1: Wrong tone, wrong energy, wrong system.

**Manual Cleanup** — How much editing was needed before the file was postable?
- 0: Post it as-is. Zero retouching.
- 1: One or two small fixes (a word, a font size).
- 2: Needed major rework before posting.

---

## ACTIVE ISSUES — Batch 01

> Fill this section as you generate Batch 01. One row per confirmed bug. Bugs move to FIXED when resolved.

| # | Carousel | Slide | Symptom | Priority | Status |
|---|----------|-------|---------|----------|--------|
|   |          |       |         |          |        |

---

## FIXED ISSUES

> Log what was fixed and why. This is the institutional memory.

| # | Carousel | Slide | Symptom | Root Cause | File Edited | Fixed |
|---|----------|-------|---------|------------|-------------|-------|
| 01 | ALL 5 (Batch 01) | all | Export ZIP button overlapping slide nav arrows and dots | `controls` + `hint` divs were inside the scaled `preview-cage` div. At `transform: scale(0.5)`, the 1080px content collapsed to 540px, colliding with the zip button below. | All 5 `.html` files (moved `</div>` to close preview-cage before controls); `workflow.md` (added explicit nesting diagram + critical warning) | 2026-05-07 |
| 02 | carousel_consejo-cv-esta-mal_brutalist | 6 (shows "03" deco-num) | Text and numbers overflowing into brand anchor / WorqAI logo at bottom | Ranked List numbers at 130px font + 60px section headline too tall for 3 items in 870px content area. Overflow into `bottom: 38px` brand anchor zone. | Brutalist HTML (num: 130→90px, headline: 60→46px, padding: 22→12px, gap: 22→14px, body: 17→15px); `anti-slop.md` (added Ranked List ceiling rule) | 2026-05-07 |
| 03 | carousel_linkedin-optimizado_boutique | all | Carousel used Profile Pro LATAM branding (handle, brand-mark, service copy) despite being briefed as WorqAI | Agent associated System 48 BRIGHT BOUTIQUE EDITORIAL with premium service brands and defaulted to Profile Pro LATAM identity. No explicit brand identity rule in workflow. | Boutique HTML (brand-mark, handle, title, CTA copy all corrected to WorqAI); `workflow.md` (added brand identity rule under Brand overrides) | 2026-05-07 |

---

## RECURRING PATTERNS — 3+ Appearances

> When the same defect appears 3 or more times across different carousels, it goes here. This is the only trigger for editing a system file.

| Pattern | Times seen | Root file to fix | Status |
|---------|-----------|-----------------|--------|
| `controls` div placed inside scaled `preview-cage`, causing nav/zip button overlap | 5/5 carousels (100%) | `workflow.md` — body structure section | ✅ Fixed + rule added 2026-05-07 |

---

## GOLD STANDARDS — Reference Carousels

> After Batch 01, pick the top 2–3 carousels that score highest. These become the benchmark — future outputs are compared to them, not to abstract rules.

| ID  | File | Score | Why it's the gold standard |
|-----|------|-------|---------------------------|
|     |      |       |                           |

---

## SINGLE-VARIABLE TEST LOG

> When you suspect a specific cause for a defect, test ONE variable change and log the result. This prevents guessing.

| Date | Variable Changed | Before Score | After Score | Finding |
|------|-----------------|:---:|:---:|---------|
|      |                 |     |     |         |

---

## POST-BATCH DECISION RULE

After scoring all 10 carousels in Batch 01:
1. Identify the 3 lowest-scoring defects from the RECURRING PATTERNS table.
2. Make EXACTLY 3 changes to system files — one per pattern. Not more.
3. Run Batch 02 (5 carousels) and compare average scores.
4. If average improves ≥ 0.5 points per metric: the change was valid. Keep it.
5. If average does not improve: revert the change. The defect has a different root cause.
