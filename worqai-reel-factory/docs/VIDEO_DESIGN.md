# VIDEO_DESIGN.md — WorqAI Reel Design Contract (Pipeline V2)

Single source of truth for how a WorqAI reel is allowed to look and move.
Applies to the footage-first lane (`FootageFirstReel`). Supersedes the visual
decisions embedded in the legacy scene system (`SpecDrivenReel`), which is kept
only for audit comparison.

Sources fused into this contract, all inspected and pinned in `vendor-lock.json`:

- `nutlope/hallmark` — slop-test gates and motion language (audit-only, never a renderer)
- `Laith0003/ux-skill` — deterministic anti-pattern detections (152-entry catalog, regex subset)
- `rohitg00/awesome-claude-design` — cinematic / data-dense DESIGN.md patterns (reference only)
- `docs/CESAR_REEL_PIPELINE_V2_PLAN.md` — creative direction (footage-first, Cesar-first)
- Repo `CLAUDE.md` brand contract and `.claude/rules` anti-slop copy rules

## 1. The one-sentence philosophy

A person explaining something real, supported by real evidence — never a
software promo template. If a frame could belong to a generic SaaS ad, it fails.

## 2. Footage-first rules (hard walls)

1. Cesar opens the reel full-frame for at least the first 3–5 seconds.
2. Real footage (Cesar, real screen recordings, real documents, sourced stills)
   occupies ≥ 75% of the runtime. Designed graphics are the seasoning, not the meal.
3. Every cutaway maps to the exact sentence being spoken. No orphan visuals.
4. Real WorqAI screens only. Never invent product UI.
5. The reel ends on Cesar full-frame unless the approved CTA requires a real product screen.
6. One designed overlay at a time. Motion never competes with the spoken explanation.

## 3. Design tokens (locked)

Every color and font in a composition references these tokens. Introducing any
other hex, gradient, or family mid-render is a build failure (linter rule `HEX-OFF-TOKEN`).

| Token | Value | Use |
|---|---|---|
| `bg` | `#080a10` | Background, full-bleed only |
| `ink` | `#F5F7F2` | Primary text |
| `muted` | `#8D96A8` | Secondary text, source labels |
| `lime` | `#C9F24D` | Accent — emphasis only |
| `--font-display` | Archivo Black (local woff2) | Captions, titles |
| `--font-body` | Inter (local woff2) | Source labels, small supporting text only |
| Grain | 0.11 opacity | Full-frame overlay |

Token discipline rules:

- **Accent footprint ≤ 8% of any frame** (hallmark gate 23, adapted). Lime is for
  the emphasis word, one underline, one marker. Never a panel fill.
- **No zero-context neutrals.** If a panel surface is ever needed, derive it from
  `bg` by lightness shift, never by inventing a new navy/gray hex (gate 22 / 48).
- **Inter is never display type.** Inter above 24 px is a build failure
  (ux-skill `inter-as-display`). Display work belongs to Archivo Black.
- **No pure `#000` or `#fff`** as a surface (gate 7).

## 4. Motion language (adapted from hallmark `motion.md` to 30 fps)

Three duration buckets. Name them, use them, nothing in between:

| Token | ms | frames @30 | Use |
|---|---|---|---|
| `durMicro` | 120 | 4 | Caption beat reveal, highlight tick |
| `durShort` | 220 | 7 | Cutaway enter, label reveal, title fade-up |
| `durLong` | 420 | 13 | Scene transition, document settle |

Easing tokens (the only three allowed):

```
easeOut    cubic-bezier(0.16, 1, 0.3, 1)   — elements entering
easeIn     cubic-bezier(0.7, 0, 0.84, 0)   — elements leaving
easeInOut  cubic-bezier(0.65, 0, 0.35, 1)  — state toggles
```

Rules:

- Animate **only transform and opacity**.
- **Exits run at 75% of the enter duration** with `easeIn`.
- **One orchestrated moment per scene.** A cutaway enters once; nothing loops idly.
- **No overshoot/bounce easings** on designed elements (linter `OVERSHOOT-EASING`).
  Springs are reserved for at most one physical gesture per reel, if any.
- Push-ins on Cesar: 3–5% scale over the scene, linear or `easeInOut`. Never faster.
- Ken Burns on stills: ≤ 5% scale drift over the still's full duration.
- Total designed-motion stagger in any moment caps at ~500 ms.

## 5. Captions

- Burned-in, transcript-timed, Archivo Black, `ink` on real footage.
- Two lines maximum, 2–5 words per beat.
- At most one emphasis word per beat in `lime`.
- Machine transcripts are drafts: a reel renders only with reviewed caption
  tokens (existing `scripts/caption-corrections.json` rule stands).
- Verbatim speech is exempt from copy rules; **designed text is not** — all
  on-screen designed copy obeys `.claude/rules/anti-slop.md` (no "hoy en día",
  no "desbloquea", no invented numbers).

## 6. Banned composition (build failures)

From the V2 plan plus hallmark/ux-skill tells, enforced by
`scripts/lint_reel_source.py` and the keyframe audit:

- Persistent corner picture-in-picture of Cesar.
- Dashboard/card grids, generic SaaS panels, fake analytics, floating UI, decorative diagrams.
- Any CSS gradient (`linear-gradient` / `radial-gradient` / `conic-gradient`).
- Glows (`box-shadow: 0 0 Npx …`), glowing status dots, neon.
- Pill chips (`border-radius: 99/999`) as designed elements.
- Emoji as icons (✨ 🚀 ⚡ 🔥 🎯 ✅).
- Italic display type.
- Re-drawn browser/phone/IDE chrome — use real screenshots.
- Invented metrics. A number appears on screen only if Cesar says it or a cited source shows it.
- Generated images containing readable text, logos, CVs, emails, or fake product screens.

## 7. Contrast (hallmark gates 40–41, applied per keyframe)

- Caption text vs. its computed background: **WCAG ≥ 4.5:1** (APCA Lc ≥ 60).
  On busy footage this means the caption zone must carry a scrim derived from `bg`
  (solid or blur, no gradient) sufficient to clear the threshold.
- Source labels and small designed text: same threshold (they are < 24 px).
- Lime-on-bg and ink-on-bg both pass; **lime is never text-on-light**.

## 8. Pre-emit self-critique (hallmark, adapted)

Before submitting any storyboard or render for human review, score 1–5:

| Axis | Question |
|---|---|
| Philosophy | Does this reel take a position, or is it just clips in order? |
| Hierarchy | In any 2 seconds, is it obvious what to look at? |
| Execution | Tokens, timing, contrast all in spec? |
| Specificity | Does it look like *this* argument by *this* person — or any career-advice reel? |
| Restraint | Has everything not earning its place been removed? |
| Variety | Does it share a structural fingerprint with a previous reel? |

Any axis < 3 → revise before requesting review. Record scores in the render's QA JSON.

## 9. Review gates (unchanged from V2 plan §9)

Design contract → timestamp storyboard → still-frame review → 12–15 s opening
proof → full draft → release candidate. No later reel enters production until
R01 passes the full-draft gate.

## 10. Transcript-native semantic cutaway

`ats_filter_mechanism` is the only approved designed cutaway for the spoken
ATS-filter explanation in R01. It is a full-screen editorial mechanism, not a
product interface: vacancy requirements form the governing spine and CV
evidence aligns from the opposite side. It may run for at most 4.5 seconds and
does not count as real footage.

- Use only the locked token set and motion buckets above.
- Leave the lower caption band visually quiet.
- Show no score, pass/fail state, ranking, invented field, or product chrome.
- Include the qualifier that systems and criteria vary.
- The cutaway must resolve one functional relationship, then leave; it must not
  become a persistent layout or picture-in-picture treatment.
