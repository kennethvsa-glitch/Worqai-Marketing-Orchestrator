# worqai Typography — LOCKED

> Status: **Decided** — April 2026.

---

## Font Decision

**One font family: Nunito.**

No display/serif split. Nunito at different weights handles everything — display, UI, body. Rounded letterforms match the brand personality (Outlaw + Everyman: bold but warm, never cold or corporate).

Google Fonts — free, open source, excellent Latin character set (Spanish diacritics: á é í ó ú ñ ü ¿ ¡).

---

## Font Stack

```css
--font-sans:    'Nunito', system-ui, -apple-system, sans-serif;
--font-display: 'Nunito', system-ui, -apple-system, sans-serif;
--font-mono:    'Courier New', ui-monospace, SFMono-Regular, monospace;
```

## Weights in Use

```css
--weight-regular: 400;   /* Body text, captions */
--weight-medium:  600;   /* Labels, UI elements, secondary headings */
--weight-bold:    700;   /* Headings, CTAs, strong emphasis */
--weight-black:   900;   /* Logo wordmark, hero display, maximum impact */
```

## Logo-Specific

```css
/* Wordmark */
font-family: 'Nunito', sans-serif;
font-weight: 900;
font-size: 64px;           /* Hero/brand use */
letter-spacing: -2.5px;    /* Tighten at display size */
text-transform: lowercase; /* always lowercase: "worqai" not "Worqai" */

/* "worq" portion: color #0F0F12 */
/* "ai" portion:   color #C7FF3A */
```

---

## Type Scale

```css
--text-xs:   0.75rem;    /* 12px — micro labels, legal */
--text-sm:   0.875rem;   /* 14px — captions, helper text */
--text-base: 1rem;       /* 16px — body copy */
--text-lg:   1.125rem;   /* 18px — lead paragraphs */
--text-xl:   1.25rem;    /* 20px — card titles, small headings */
--text-2xl:  1.5rem;     /* 24px — section headings */
--text-3xl:  1.875rem;   /* 30px — page headings */
--text-4xl:  2.25rem;    /* 36px — hero subheadings */
--text-5xl:  3rem;       /* 48px — hero headings */
--text-6xl:  3.75rem;    /* 60px — display / campaign headlines */
```

## Usage Rules

| Element | Size | Weight | Letter-spacing |
|---|---|---|---|
| Hero headline | `text-5xl` / `text-6xl` | 900 | `-0.04em` |
| Page heading (H1) | `text-4xl` | 800 | `-0.03em` |
| Section heading (H2) | `text-3xl` | 700 | `-0.02em` |
| Card title (H3) | `text-xl` | 700 | `normal` |
| Body copy | `text-base` | 400 | `normal` |
| UI labels / caps | `text-xs` | 700 | `+0.1em` |
| CTA button | `text-sm` / `text-base` | 700 | `normal` |

## Line Heights

```css
--leading-display:  1.1;   /* Headlines, hero */
--leading-heading:  1.2;   /* H2, H3 */
--leading-body:     1.6;   /* Body copy — critical for Spanish readability */
--leading-caption:  1.4;   /* Captions, labels */
```

## Spanish-Specific Rules

- Line height for body copy: never below 1.55 — Spanish sentences run longer than English
- Diacritics (á, é, í, ó, ú, ñ) render correctly in Nunito — confirmed
- Inverted punctuation (¿, ¡) — Nunito includes them, use them correctly
- Avoid `text-transform: uppercase` on long Spanish strings — loses readability with diacritics

---

## What NOT to use

- No serif fonts — Fraunces, Instrument Serif, Georgia — wrong archetype for this brand
- No thin/light weights (100–300) — too luxury/cold for Everyman accessibility
- No Helvetica/Arial as primary — too corporate, too generic
- No Inter as primary — works fine as fallback but lacks the warmth Nunito carries

---

## Google Fonts import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
```

```css
/* Tailwind v4 */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
```
