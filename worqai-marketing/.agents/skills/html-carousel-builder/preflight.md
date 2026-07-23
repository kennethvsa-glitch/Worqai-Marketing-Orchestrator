# Preflight Reference — preflight.py

Deterministic pre-flight validator for carousel HTML files. Runs after every render.

## Command

```bash
py scripts/preflight.py production/carousel_topic_s17.html
py scripts/preflight.py production/carousel_topic_s17.html --aspect 4:5
```

Exit codes: `0` = score ≥ 90 (READY TO EXPORT), `1` = issues found.

---

## Scoring Formula

```
score = int((checks_passed / 10) * 100) - bloat_penalty
```

- 10 checks total, each worth 10 points
- `bloat_penalty` is currently only applied by check 10 (decorative density): max 5 points
- File size (check 3) over 55 KB adds no penalty — it's informational only (NOTE)
- Score ≥ 90 → READY TO EXPORT
- Score ≥ 70 → GOOD — fix warnings before export
- Score < 70 → NEEDS WORK

---

## The 10 Checks

### Check 1: Text Overflow (heuristic)

Classifies every text node in each slide by tag/class, then checks char count and word count against budgets.

**Selector → text type mapping (first match wins):**

| CSS pattern matched | Text type | Max chars | Max words |
|--------------------|-----------|-----------|-----------|
| `h1`, `h2`, `[class*=headline]`, `[class*=display]`, `[class*=title]`, `[class*=stat]` | headline | 55 | 10 |
| `p`, `[class*=body]`, `[class*=txt]`, `[class*=text]`, `[class*=context]` | body | 140 | 22 |
| `[class*=label]`, `[class*=tag]`, `[class*=lbl]` | label | 40 | 6 |
| `[class*=keyword]` | cta_keyword | 18 | 2 |

**Aspect multipliers:** `1:1 = ×1.0`, `4:5 = ×1.15`, `9:16 = ×1.3` (applied to both char and word budgets)

**Known selector side-effects (gotchas):**
- `stat-context` class matches `[class*=stat]` → classified as headline (55 char / 10 word budget, not body)
- `tip-blk-label` class matches `[class*=lbl]` → classified as label (40 char / 6 word budget)
- `chk-title` class matches `[class*=title]` → classified as headline (55 char / 10 word budget)
- Em dash `—` counts as a word (Python's `split()` on whitespace)

Word counter: `len(text.split())` — splits on whitespace only.

---

### Check 2: VAR_ Placeholder Check

Scans entire HTML for `VAR_\w+` patterns. Any match = FAIL. Ensures no unfilled template placeholders reached the file.

---

### Check 3: File Size

| Size range | Tier | Result |
|------------|------|--------|
| < 20 KB | generic | CRITICAL — too generic, rebuild |
| 20–35 KB | good | PASS |
| 35–55 KB | very_good | PASS — ideal range |
| > 55 KB | bloat | NOTE — informational only, no score penalty |

File size > 55 KB still counts as `checks_passed += 1`. No penalty applied. The NOTE is advisory.

---

### Check 4: Layout Diversity

Detects slides by matching `class="slide"` (excludes `class="slides"` container via negative lookahead). Compares sorted class-name signatures of adjacent slides. Two consecutive slides with identical signatures = FAIL.

---

### Check 5: Anti-Slop

Scans each line for 3 patterns:

| Name | Pattern | What it catches |
|------|---------|----------------|
| `COLORED_LEFT_BORDER` | `border-left: Npx solid <color>` | Overused card left-border styling |
| `PILL_BADGE` | `border-radius: 999px` + `border: 1px solid` | Generic pill badges |
| `DECORATIVE_BG_NUMBER` | `deco-num` + `opacity: 0.0[0-8]` | Faint decorative background numbers |

**Exception:** Lines containing `::before` or `::after` are skipped for `COLORED_LEFT_BORDER`. This prevents false positives from `.sub-download-card .dl-icon::before` (corner-fold triangle in the shell) and any other pseudo-element decorative uses of border-left.

---

### Check 6: Mock UI

Looks for any of these strings anywhere in the HTML:
`terminal-panel`, `mock-cv`, `mock-app`, `mock-form`, `mock-checklist`, `mock-display`, `mock-metric`, `message-chat`, `message-email`, `ecom-product`, `ecom-pricing`, `icon-avatar`, `code-syntax`, `cmd`, `>$ `

If none found → FAIL. At least one slide must contain a mock UI element.

---

### Check 7: CTA Completeness

Inspects the last detected slide only. Requires all three:
1. `keyword-box` or `keyword-text` class present
2. A `?` or `¿` character present
3. Any of these words (case-insensitive): `template`, `gratis`, `free`, `auditoria`, `audit`, `reporte`, `guia`, `checklist`

Missing any one = FAIL.

---

### Check 8: html2canvas Compatibility

Two risk checks:

| Risk | Pattern | Logic |
|------|---------|-------|
| `conic-gradient` | `conic-gradient(` | Only flags if `<div class="geo-conic-rays"` exists in the HTML body. CSS definitions alone are safe. |
| `backdrop-filter` | `backdrop-filter:` (without `-webkit-` prefix) | Skipped entirely if `-webkit-backdrop-filter` appears anywhere in the file. |

The `-webkit-` check is file-wide, not line-level, which avoids false positives from minified CSS.

---

### Check 9: Grid Divider Bug

Looks for `<div class="...divider/separator..."></div>` (empty div) inside flex/grid containers. These cause rendering artifacts — should be replaced with `border-right` on an adjacent element instead.

---

### Check 10: Decorative Density (heuristic — never fails)

Counts `position: absolute` occurrences in the entire HTML. Compares against `len(slides) * 4` threshold (16 for a 4-slide carousel). If exceeded: WARN + `bloat_penalty = 5`. The check always passes (`checks_passed += 1`) — it only applies a score penalty.

---

## Known False Positives (fixed in current version)

- `COLORED_LEFT_BORDER` — triggered by `.sub-download-card .dl-icon::before` (download card corner fold). Fixed: pseudo-element lines are excluded.
- `conic-gradient` — triggered by `.geo-conic-rays` CSS rule in the shell even when the layer wasn't activated. Fixed: only flags when the div actually exists in body HTML.
- `backdrop-filter` — triggered by `.swipe-pill` which correctly uses `-webkit-backdrop-filter`. Fixed: file-wide `-webkit-` check skips the entire check if prefix is present.
