# worqai Brand Colors — LOCKED

> Status: **Decided** — April 2026. Direction: Verde Eléctrico.

---

## Primary Palette

```css
--worqai-lime:    #C7FF3A;   /* Primary brand color — logo mark, "ai" wordmark accent, CTAs */
--worqai-ink:     #0F0F12;   /* Near-black — body text, wordmark "worq" portion */
--worqai-circle:  #1A1A18;   /* Logo circle background — warm dark, not pure black */
--worqai-paper:   #FFF8E7;   /* Warm cream — page background, light surfaces */
```

## Accent

```css
--worqai-coral:   #FF5C3C;   /* Pop accent — CTAs on dark bg, hover states, "i" dot in wordmark */
```

## Neutrals

```css
--worqai-muted:   #6B6B66;   /* Secondary text, labels, captions */
--worqai-border:  #E8E8E3;   /* Dividers, card borders */
--worqai-surface: #F5EDD9;   /* Warm parchment — cards, section backgrounds */
```

## Semantic Colors

```css
--worqai-success: #C7FF3A;   /* Use lime — success is on-brand */
--worqai-warning: #FFD93D;   /* Warm yellow — soft alert */
--worqai-error:   #FF5C3C;   /* Coral — doubles as error */
```

---

## Usage Rules

| Color | Use on | Never use on |
|---|---|---|
| `#C7FF3A` lime | Logo mark, "ai" text, CTA buttons (dark bg), success states, icon accents | Body text, large background areas, light surfaces (fails contrast) |
| `#0F0F12` ink | All body text, "worq" portion of wordmark, headings | Anything where lime is background (use cream instead) |
| `#FFF8E7` paper | Page backgrounds, light card surfaces, text on dark bg | Primary CTA buttons |
| `#1A1A18` circle | Logo circle bg, dark section backgrounds, nav | Body text areas |
| `#FF5C3C` coral | CTAs on dark backgrounds, hover states, "i" dot accent | Large fills — accent only |

## Accessibility

- Lime `#C7FF3A` on dark `#1A1A18` → contrast ratio **10.4:1** ✓ AAA
- Ink `#0F0F12` on paper `#FFF8E7` → contrast ratio **18.7:1** ✓ AAA
- Lime `#C7FF3A` on paper `#FFF8E7` → contrast ratio **1.5:1** ✗ — never use lime text on cream
- Coral `#FF5C3C` on dark `#1A1A18` → contrast ratio **5.1:1** ✓ AA

## Logo Color Rules

**Wordmark:** "worq" in `#0F0F12`, "ai" in `#C7FF3A`. Always on `#FFF8E7` paper or white. Never on lime background.

**Circle mark:** W letterform in `#C7FF3A` on `#1A1A18` circle. Optional "worqai" label below in `#FFF8E7`. The circle sits on `#FFF8E7` or `#F5EDD9` backgrounds.

---

## Profile Pro LATAM (Separate brand — do not mix)

Profile Pro LATAM uses a distinct premium palette — warm neutrals, no lime, no coral. TBD when that brand identity is formalized. Never apply worqai lime or coral to Profile Pro LATAM materials.
